"""
Enterprise Client controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.enterprise_client_model import (
    EnterpriseClientCreate, EnterpriseClientUpdate, EnterpriseClientResponse, EnterpriseClient
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.enterprise_client_service import (
    create_enterprise_client_service,
    get_enterprise_client_by_name_service,
    get_enterprise_client_by_email_service,
    get_enterprise_client_by_id_service,
    get_all_enterprise_clients_service,
    update_enterprise_client_service,
    delete_enterprise_client_service,
    activate_enterprise_client_service,
    deactivate_enterprise_client_service,
    update_client_settings_service
)

logger = get_logger("ENTERPRISE_CLIENT_CONTROLLER")


def create_enterprise_client(client_data: EnterpriseClientCreate, db: Session) -> EnterpriseClientResponse:
    """Create a new enterprise client"""
    try:
        return create_enterprise_client_service(client_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_enterprise_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_client_by_email(email: str, db: Session) -> Optional[EnterpriseClientResponse]:
    """Get enterprise client by email"""
    try:
        return get_enterprise_client_by_email_service(email, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_client_by_email: {e}")
        return None


def get_enterprise_client_by_id(client_id: str, db: Session) -> Optional[EnterpriseClientResponse]:
    """Get enterprise client by ID"""
    try:
        return get_enterprise_client_by_id_service(client_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_client_by_id: {e}")
        return None


def get_all_enterprise_clients(db: Session) -> List[EnterpriseClientResponse]:
    """Get all enterprise clients"""
    try:
        return get_all_enterprise_clients_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_enterprise_clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_enterprise_client(client_id: str, client_data: EnterpriseClientUpdate, db: Session) -> EnterpriseClientResponse:
    """Update enterprise client"""
    try:
        return update_enterprise_client_service(client_id, client_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_enterprise_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_enterprise_client(client_id: str, db: Session) -> bool:
    """Delete enterprise client"""
    try:
        return delete_enterprise_client_service(client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_enterprise_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_enterprise_client(client_id: str, db: Session) -> EnterpriseClientResponse:
    """Activate an enterprise client"""
    try:
        return activate_enterprise_client_service(client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_enterprise_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_enterprise_client(client_id: str, db: Session) -> EnterpriseClientResponse:
    """Deactivate an enterprise client"""
    try:
        return deactivate_enterprise_client_service(client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_enterprise_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_client_settings(client_id: str, settings: dict, db: Session) -> EnterpriseClientResponse:
    """Update client settings"""
    try:
        return update_client_settings_service(client_id, settings, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_client_settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
