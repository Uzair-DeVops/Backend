"""
End Client routes for end client management by enterprise admins
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Dict
from ..controllers.end_client_controller import (
    create_end_client,
    get_end_client_by_id,
    get_all_end_clients,
    get_end_clients_by_enterprise,
    get_end_clients_by_creator,
    update_end_client,
    delete_end_client,
    activate_end_client,
    deactivate_end_client,
    update_end_client_settings
)
from ..models.end_client_model import (
    EndClientCreate, EndClientUpdate, EndClientResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("END_CLIENT_ROUTES")

router = APIRouter(prefix="/end-clients", tags=["End Clients"])

@router.post("/", response_model=EndClientResponse)
async def create_end_client_endpoint(
    client_data: EndClientCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new end client"""
    return create_end_client(client_data, db)

@router.get("/", response_model=List[EndClientResponse])
async def get_end_clients_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all end clients"""
    return get_all_end_clients(db)

@router.get("/{client_id}", response_model=EndClientResponse)
async def get_end_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get end client by ID"""
    client = get_end_client_by_id(client_id, db)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="End client not found"
        )
    return client

@router.get("/by-enterprise/{enterprise_client_id}", response_model=List[EndClientResponse])
async def get_end_clients_by_enterprise_endpoint(
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get end clients by enterprise client ID"""
    return get_end_clients_by_enterprise(enterprise_client_id, db)

@router.get("/by-creator/{created_by}", response_model=List[EndClientResponse])
async def get_end_clients_by_creator_endpoint(
    created_by: str,
    db: Session = Depends(get_database_session)
):
    """Get end clients created by a specific enterprise admin"""
    return get_end_clients_by_creator(created_by, db)

@router.put("/{client_id}", response_model=EndClientResponse)
async def update_end_client_endpoint(
    client_id: str,
    client_data: EndClientUpdate,
    db: Session = Depends(get_database_session)
):
    """Update end client"""
    return update_end_client(client_id, client_data, db)

@router.delete("/{client_id}")
async def delete_end_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete end client"""
    success = delete_end_client(client_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="End client not found"
        )
    return {"message": "End client deleted successfully"}

@router.patch("/{client_id}/activate", response_model=EndClientResponse)
async def activate_end_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session)
):
    """Activate an end client"""
    return activate_end_client(client_id, db)

@router.patch("/{client_id}/deactivate", response_model=EndClientResponse)
async def deactivate_end_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session)
):
    """Deactivate an end client"""
    return deactivate_end_client(client_id, db)

@router.patch("/{client_id}/settings", response_model=EndClientResponse)
async def update_end_client_settings_endpoint(
    client_id: str,
    settings: Dict,
    db: Session = Depends(get_database_session)
):
    """Update end client settings"""
    return update_end_client_settings(client_id, settings, db)
