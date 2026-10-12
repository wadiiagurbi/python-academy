from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.data_pipeline import PipelineStatus


class PipelineStepConfig(BaseModel):
    type: str  # "ingest", "clean", "transform", "analyze", "visualize", "export"
    name: str
    config: dict[str, Any] = {}


class DataPipelineBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    config: dict[str, Any] = Field(default_factory=dict)


class DataPipelineCreate(DataPipelineBase):
    pass


class DataPipelineUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    config: Optional[dict[str, Any]] = None


class DataPipelineRead(DataPipelineBase):
    id: int
    owner_id: int
    status: PipelineStatus
    last_result: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PipelineExecutionRequest(BaseModel):
    config_override: Optional[dict[str, Any]] = None


class PipelineExecutionResult(BaseModel):
    success: bool
    output: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: int
    steps_executed: list[dict[str, Any]] = []