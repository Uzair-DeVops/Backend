"""
End Client Service - Business logic layer for end client operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.end_client_model import (
    EndClient, EndClientCreate, EndClientUpdate, EndClientResponse
)
from ..utils.my_logger import get_logger

logger = get_logger("END_CLIENT_SERVICE")


def create_end_client_service(client_data: EndClientCreate, db: Session) -> EndClientResponse:
    """Create a new end client"""
    try:
        # Check if email already exists
        existing_client = get_end_client_by_email_service(client_data.email, db)
        if existing_client:
            logger.warning(f"End client creation failed: email {client_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Convert settings dict to JSON string
        settings_json = json.dumps(client_data.settings) if client_data.settings else "{}"
        
        # Create client object
        client = EndClient(
            name=client_data.name,
            email=client_data.email,
            contact_person=client_data.contact_person,
            phone=client_data.phone,
            address=client_data.address,
            company_size=client_data.company_size,
            industry=client_data.industry,
            settings=settings_json,
            enterprise_client_id=client_data.enterprise_client_id,
            created_by=client_data.created_by
        )
        
        # Save to database
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"End client created successfully: {client.name}")
        
        return EndClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            company_size=client.company_size,
            industry=client.industry,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at,
            settings=client_data.settings,
            enterprise_client_id=client.enterprise_client_id,
            created_by=client.created_by
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End client creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating end client"
        )


def get_end_client_by_email_service(email: str, db: Session) -> Optional[EndClient]:
    """Get end client by email"""
    try:
        statement = select(EndClient).where(EndClient.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting end client by email: {e}")
        return None


def get_end_client_by_id_service(client_id: str, db: Session) -> Optional[EndClientResponse]:
    """Get end client by ID"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EndClient).where(EndClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            return None
        
        # Convert JSON settings back to dict
        settings = json.loads(client.settings) if client.settings else {}
        
        return EndClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            company_size=client.company_size,
            industry=client.industry,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at,
            settings=settings,
            enterprise_client_id=client.enterprise_client_id,
            created_by=client.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting end client by ID: {e}")
        return None


def get_all_end_clients_service(db: Session) -> List[EndClientResponse]:
    """Get all end clients"""
    try:
        statement = select(EndClient)
        clients = db.exec(statement).all()
        
        return [
            EndClientResponse(
                id=client.id,
                name=client.name,
                email=client.email,
                contact_person=client.contact_person,
                phone=client.phone,
                address=client.address,
                company_size=client.company_size,
                industry=client.industry,
                is_active=client.is_active,
                created_at=client.created_at,
                updated_at=client.updated_at,
                settings=json.loads(client.settings) if client.settings else {},
                enterprise_client_id=client.enterprise_client_id,
                created_by=client.created_by
            )
            for client in clients
        ]
        
    except Exception as e:
        logger.error(f"Error getting all end clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving end clients"
        )


def get_end_clients_by_enterprise_service(enterprise_client_id: str, db: Session) -> List[EndClientResponse]:
    """Get end clients by enterprise client ID"""
    try:
        enterprise_uuid = UUID(enterprise_client_id)
        statement = select(EndClient).where(EndClient.enterprise_client_id == enterprise_uuid)
        clients = db.exec(statement).all()
        
        return [
            EndClientResponse(
                id=client.id,
                name=client.name,
                email=client.email,
                contact_person=client.contact_person,
                phone=client.phone,
                address=client.address,
                company_size=client.company_size,
                industry=client.industry,
                is_active=client.is_active,
                created_at=client.created_at,
                updated_at=client.updated_at,
                settings=json.loads(client.settings) if client.settings else {},
                enterprise_client_id=client.enterprise_client_id,
                created_by=client.created_by
            )
            for client in clients
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting end clients by enterprise: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving end clients"
        )


def get_end_clients_by_creator_service(created_by: str, db: Session) -> List[EndClientResponse]:
    """Get end clients created by a specific enterprise admin"""
    try:
        creator_uuid = UUID(created_by)
        statement = select(EndClient).where(EndClient.created_by == creator_uuid)
        clients = db.exec(statement).all()
        
        return [
            EndClientResponse(
                id=client.id,
                name=client.name,
                email=client.email,
                contact_person=client.contact_person,
                phone=client.phone,
                address=client.address,
                company_size=client.company_size,
                industry=client.industry,
                is_active=client.is_active,
                created_at=client.created_at,
                updated_at=client.updated_at,
                settings=json.loads(client.settings) if client.settings else {},
                enterprise_client_id=client.enterprise_client_id,
                created_by=client.created_by
            )
            for client in clients
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid creator ID format"
        )
    except Exception as e:
        logger.error(f"Error getting end clients by creator: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving end clients"
        )


def update_end_client_service(client_id: str, client_data: EndClientUpdate, db: Session) -> EndClientResponse:
    """Update end client"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EndClient).where(EndClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="End client not found"
            )
        
        # Check if new email already exists (if email is being updated)
        if client_data.email and client_data.email != client.email:
            existing_client = get_end_client_by_email_service(client_data.email, db)
            if existing_client:
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
        
        logger.info(f"End client updated successfully: {client.name}")
        
        return EndClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            company_size=client.company_size,
            industry=client.industry,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at,
            settings=json.loads(client.settings) if client.settings else {},
            enterprise_client_id=client.enterprise_client_id,
            created_by=client.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid end client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End client update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating end client"
        )


def delete_end_client_service(client_id: str, db: Session) -> bool:
    """Delete end client"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EndClient).where(EndClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="End client not found"
            )
        
        db.delete(client)
        db.commit()
        
        logger.info(f"End client deleted successfully: {client.name}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid end client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End client deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting end client"
        )


def activate_end_client_service(client_id: str, db: Session) -> EndClientResponse:
    """Activate an end client"""
    try:
        client_uuid = UUID(client_id)
        statement = select(EndClient).where(EndClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="End client not found"
            )
        
        client.is_active = True
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"End client activated: {client.name}")
        
        return EndClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            company_size=client.company_size,
            industry=client.industry,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at,
            settings=json.loads(client.settings) if client.settings else {},
            enterprise_client_id=client.enterprise_client_id,
            created_by=client.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid end client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End client activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating end client"
        )


def deactivate_end_client_service(client_id: str, db: Session) -> EndClientResponse:
    """Deactivate an end client"""
    try:
        client_uuid = UUID(client_id)
        statement = select(EndClient).where(EndClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="End client not found"
            )
        
        client.is_active = False
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"End client deactivated: {client.name}")
        
        return EndClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            company_size=client.company_size,
            industry=client.industry,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at,
            settings=json.loads(client.settings) if client.settings else {},
            enterprise_client_id=client.enterprise_client_id,
            created_by=client.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid end client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End client deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating end client"
        )


def update_end_client_settings_service(client_id: str, settings: dict, db: Session) -> EndClientResponse:
    """Update end client settings"""
    try:
        client_uuid = UUID(client_id)
        statement = select(EndClient).where(EndClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="End client not found"
            )
        
        # Update settings
        client.settings = json.dumps(settings)
        client.updated_at = datetime.now()
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"End client settings updated for: {client.name}")
        
        return EndClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            company_size=client.company_size,
            industry=client.industry,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at,
            settings=settings,
            enterprise_client_id=client.enterprise_client_id,
            created_by=client.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid end client ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End client settings update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating end client settings"
        )
