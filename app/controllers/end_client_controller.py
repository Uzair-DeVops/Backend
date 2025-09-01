"""
End Client controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.end_client_model import (
    EndClientCreate, EndClientUpdate, EndClientResponse, EndClient
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.end_client_service import (
    create_end_client_service,
    get_end_client_by_email_service,
    get_end_client_by_id_service,
    get_all_end_clients_service,
    get_end_clients_by_enterprise_service,
    get_end_clients_by_creator_service,
    update_end_client_service,
    delete_end_client_service,
    activate_end_client_service,
    deactivate_end_client_service,
    update_end_client_settings_service
)

logger = get_logger("END_CLIENT_CONTROLLER")


def create_end_client(client_data: EndClientCreate, db: Session) -> EndClientResponse:
    """Create a new end client"""
    try:
        return create_end_client_service(client_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_end_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_end_client_by_email(email: str, db: Session) -> Optional[EndClientResponse]:
    """Get end client by email"""
    try:
        return get_end_client_by_email_service(email, db)
    except Exception as e:
        logger.error(f"Controller error in get_end_client_by_email: {e}")
        return None


def get_end_client_by_id(client_id: str, db: Session) -> Optional[EndClientResponse]:
    """Get end client by ID"""
    try:
        return get_end_client_by_id_service(client_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_end_client_by_id: {e}")
        return None


def get_all_end_clients(db: Session) -> List[EndClientResponse]:
    """Get all end clients"""
    try:
        return get_all_end_clients_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_end_clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_end_clients_by_enterprise(enterprise_client_id: str, db: Session) -> List[EndClientResponse]:
    """Get end clients by enterprise client ID"""
    try:
        return get_end_clients_by_enterprise_service(enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_end_clients_by_enterprise: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_end_clients_by_creator(created_by: str, db: Session) -> List[EndClientResponse]:
    """Get end clients created by a specific enterprise admin"""
    try:
        return get_end_clients_by_creator_service(created_by, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_end_clients_by_creator: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_end_client(client_id: str, client_data: EndClientUpdate, db: Session) -> EndClientResponse:
    """Update end client"""
    try:
        return update_end_client_service(client_id, client_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_end_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_end_client(client_id: str, db: Session) -> bool:
    """Delete end client"""
    try:
        return delete_end_client_service(client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_end_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_end_client(client_id: str, db: Session) -> EndClientResponse:
    """Activate an end client"""
    try:
        return activate_end_client_service(client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_end_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_end_client(client_id: str, db: Session) -> EndClientResponse:
    """Deactivate an end client"""
    try:
        return deactivate_end_client_service(client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_end_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_end_client_settings(client_id: str, settings: dict, db: Session) -> EndClientResponse:
    """Update end client settings"""
    try:
        return update_end_client_settings_service(client_id, settings, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_end_client_settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
