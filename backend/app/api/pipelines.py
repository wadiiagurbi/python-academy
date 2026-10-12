from fastapi import APIRouter, Depends, status

from app.schemas.pipeline import (
    DataPipelineCreate,
    DataPipelineRead,
    DataPipelineUpdate,
    PipelineExecutionRequest,
    PipelineExecutionResult,
)
from app.services.auth_service import get_current_user
from app.services.pipeline_service import PipelineService
from app.core.dependencies import get_pipeline_service
from app.models.user import User

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.post("", response_model=DataPipelineRead, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    data: DataPipelineCreate,
    current_user: User = Depends(get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
):
    return await pipeline_service.create(current_user.id, data)


@router.get("", response_model=list[DataPipelineRead])
async def list_pipelines(
    current_user: User = Depends(get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
):
    return await pipeline_service.list(current_user.id)


@router.get("/{pipeline_id}", response_model=DataPipelineRead)
async def get_pipeline(
    pipeline_id: int,
    current_user: User = Depends(get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
):
    return await pipeline_service.get(pipeline_id, current_user.id)


@router.put("/{pipeline_id}", response_model=DataPipelineRead)
async def update_pipeline(
    pipeline_id: int,
    data: DataPipelineUpdate,
    current_user: User = Depends(get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
):
    return await pipeline_service.update(pipeline_id, current_user.id, data)


@router.delete("/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipeline(
    pipeline_id: int,
    current_user: User = Depends(get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
):
    await pipeline_service.delete(pipeline_id, current_user.id)


@router.post("/{pipeline_id}/execute", response_model=PipelineExecutionResult)
async def execute_pipeline(
    pipeline_id: int,
    request: PipelineExecutionRequest,
    current_user: User = Depends(get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
):
    return await pipeline_service.execute(pipeline_id, current_user.id, request)