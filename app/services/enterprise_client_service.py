"""
Enterprise Client Service - Business logic layer for enterprise client operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.enterprise_client_model import (
    EnterpriseClient, EnterpriseClientCreate, EnterpriseClientUpdate, EnterpriseClientResponse
)
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_CLIENT_SERVICE")


def create_enterprise_client_service(client_data: EnterpriseClientCreate, db: Session) -> EnterpriseClientResponse:
    """Create a new enterprise client"""
    try:
        # Check if client name already exists
        existing_client = get_enterprise_client_by_name_service(client_data.name, db)
        if existing_client:
            logger.warning(f"Client creation failed: name {client_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client name already exists"
            )
        
        # Check if email already exists
        if client_data.email:
            existing_email = get_enterprise_client_by_email_service(client_data.email, db)
            if existing_email:
                logger.warning(f"Client creation failed: email {client_data.email} already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Convert settings dict to JSON string
        settings_json = json.dumps(client_data.settings) if client_data.settings else "{}"
        
        # Create client object
        client = EnterpriseClient(
            name=client_data.name,
            email=client_data.email,
            phone=client_data.phone,
            address=client_data.address,
            contact_person=client_data.contact_person,
            settings=settings_json,
            is_active=client_data.is_active
        )
        
        # Save to database
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Enterprise client created successfully: {client.name}")
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            contact_person=client.contact_person,
            settings=client_data.settings,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating client"
        )


def get_enterprise_client_by_name_service(name: str, db: Session) -> Optional[EnterpriseClient]:
    """Get enterprise client by name"""
    try:
        statement = select(EnterpriseClient).where(EnterpriseClient.name == name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting client by name: {e}")
        return None


def get_enterprise_client_by_email_service(email: str, db: Session) -> Optional[EnterpriseClient]:
    """Get enterprise client by email"""
    try:
        statement = select(EnterpriseClient).where(EnterpriseClient.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting client by email: {e}")
        return None


def get_enterprise_client_by_id_service(client_id: str, db: Session) -> Optional[EnterpriseClientResponse]:
    """Get enterprise client by ID"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            return None
        
        # Convert JSON settings back to dict
        settings = json.loads(client.settings) if client.settings else {}
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            contact_person=client.contact_person,
            settings=settings,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting client by ID: {e}")
        return None


def get_all_enterprise_clients_service(db: Session) -> List[EnterpriseClientResponse]:
    """Get all enterprise clients"""
    try:
        statement = select(EnterpriseClient)
        clients = db.exec(statement).all()
        
        return [
            EnterpriseClientResponse(
                id=client.id,
                name=client.name,
                email=client.email,
                phone=client.phone,
                address=client.address,
                contact_person=client.contact_person,
                settings=json.loads(client.settings) if client.settings else {},
                is_active=client.is_active,
                created_at=client.created_at,
                updated_at=client.updated_at
            )
            for client in clients
        ]
        
    except Exception as e:
        logger.error(f"Error getting all clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving clients"
        )


def update_enterprise_client_service(client_id: str, client_data: EnterpriseClientUpdate, db: Session) -> EnterpriseClientResponse:
    """Update enterprise client"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if client_data.name and client_data.name != client.name:
            existing_client = get_enterprise_client_by_name_service(client_data.name, db)
            if existing_client:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Client name already exists"
                )
        
        # Check if new email already exists (if email is being updated)
        if client_data.email and client_data.email != client.email:
            existing_email = get_enterprise_client_by_email_service(client_data.email, db)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Update fields
        for field, value in client_data.dict(exclude_unset=True).items():
            if hasattr(client, field) and field != "id":
                if field == "settings" and value is not None:
                    value = json.dumps(value)
                setattr(client, field, value)
        
        # Update timestamp
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Enterprise client updated successfully: {client.name}")
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            contact_person=client.contact_person,
            settings=json.loads(client.settings) if client.settings else {},
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating client"
        )


def delete_enterprise_client_service(client_id: str, db: Session) -> bool:
    """Delete enterprise client"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        db.delete(client)
        db.commit()
        
        logger.info(f"Enterprise client deleted successfully: {client.name}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting client"
        )


def activate_enterprise_client_service(client_id: str, db: Session) -> EnterpriseClientResponse:
    """Activate an enterprise client"""
    try:
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        client.is_active = True
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Enterprise client activated: {client.name}")
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            contact_person=client.contact_person,
            settings=json.loads(client.settings) if client.settings else {},
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating client"
        )


def deactivate_enterprise_client_service(client_id: str, db: Session) -> EnterpriseClientResponse:
    """Deactivate an enterprise client"""
    try:
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        client.is_active = False
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Enterprise client deactivated: {client.name}")
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            contact_person=client.contact_person,
            settings=json.loads(client.settings) if client.settings else {},
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating client"
        )


def update_client_settings_service(client_id: str, settings: dict, db: Session) -> EnterpriseClientResponse:
    """Update client settings"""
    try:
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        # Update settings
        client.settings = json.dumps(settings)
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Client settings updated for: {client.name}")
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            contact_person=client.contact_person,
            settings=settings,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Client settings update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating client settings"
        )
