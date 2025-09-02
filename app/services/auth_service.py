"""
Auth Service - Business logic layer for authentication operations (Functional approach)
"""
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
import jwt
from passlib.context import CryptContext

from datetime import datetime
from ..models.admin_user_model import AdminUser
from ..models.auth_model import  TokenData, TokenResponse
from ..utils.my_logger import get_logger
from ..utils.database_dependency import get_database_session
from .admin_user_service import get_admin_user_by_email_service, verify_user_password_service
from ..config.my_settings import settings

logger = get_logger("AUTH_SERVICE")

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token_service(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        logger.info(f"Access token created for user: {data.get('sub')}")
        return encoded_jwt
        
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating access token"
        )


def verify_token_service(token: str) -> Optional[TokenData]:
    """Verify JWT token and return token data"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        
        token_data = TokenData(email=email)
        return token_data
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"JWT error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return None


def authenticate_user_service(email: str, password: str, db: Session) -> Optional[AdminUser]:
    """Authenticate user with email and password"""
    try:
        user = get_admin_user_by_email_service(email, db)
        if not user:
            logger.warning(f"Authentication failed: user not found for email {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Authentication failed: user {email} is inactive")
            return None
        
        if not verify_user_password_service(user, password):
            logger.warning(f"Authentication failed: invalid password for user {email}")
            return None
        
        logger.info(f"User authenticated successfully: {email}")
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None


def get_current_user_service(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database_session)
) -> AdminUser:
    """Get current authenticated user from token"""
    try:
        token = credentials.credentials
        token_data = verify_token_service(token)
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = get_admin_user_by_email_service(token_data.email, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def login_user_service(email: str, password: str, db: Session) -> TokenResponse:
    """Login user and return access token"""
    try:
        user = authenticate_user_service(email, password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token_service(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"User logged in successfully: {email}")
        return TokenResponse(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )


def refresh_token_service(current_user: AdminUser) -> TokenResponse:
    """Refresh access token for current user"""
    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token_service(
            data={"sub": current_user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"Token refreshed for user: {current_user.email}")
        return TokenResponse(access_token=access_token, token_type="bearer")
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error refreshing token"
        )


def logout_user_service(current_user: AdminUser) -> dict:
    """Logout user (in a real implementation, you might want to blacklist the token)"""
    try:
        logger.info(f"User logged out: {current_user.email}")
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during logout"
        )


def get_current_admin_user_service(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database_session)
) -> AdminUser:
    """Get current authenticated admin user from Bearer token"""
    try:
        token = credentials.credentials
        payload = verify_token_service(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        email: str = payload.email
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = get_admin_user_by_email_service(email, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Current admin user authenticated: {email}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current admin user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_admin_user_service(current_user: AdminUser = Depends(get_current_admin_user_service)) -> AdminUser:
    """Dependency that requires an authenticated admin user"""
    return current_user


def change_password_service(
    current_user: AdminUser, 
    current_password: str, 
    new_password: str, 
    db: Session
) -> dict:
    """Change user password"""
    try:
        # Verify current password
        if not verify_user_password_service(current_user, current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        from ..utils.auth_utils import get_password_hash
        hashed_new_password = get_password_hash(new_password)
        
        # Update password
        current_user.password = hashed_new_password
        current_user.updated_at = datetime.utcnow()
        
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"Password changed successfully for user: {current_user.email}")
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error changing password"
        )
