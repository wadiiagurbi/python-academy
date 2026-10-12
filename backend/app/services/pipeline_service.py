import asyncio
import time
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PipelineNotFoundException, PipelineExecutionException
from app.models.data_pipeline import DataPipeline, PipelineStatus
from app.repositories.pipeline_repository import DataPipelineRepository
from app.schemas.pipeline import (
    DataPipelineCreate,
    DataPipelineRead,
    DataPipelineUpdate,
    PipelineExecutionRequest,
    PipelineExecutionResult,
    PipelineStepConfig,
)


class PipelineService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DataPipelineRepository(session)

    async def create(self, owner_id: int, data: DataPipelineCreate) -> DataPipelineRead:
        pipeline = DataPipeline(
            owner_id=owner_id,
            name=data.name,
            description=data.description,
            config=data.config,
            status=PipelineStatus.DRAFT,
        )
        pipeline = await self.repo.create(pipeline)
        await self.session.commit()
        return DataPipelineRead.model_validate(pipeline)

    async def get(self, pipeline_id: int, owner_id: int) -> DataPipelineRead:
        pipeline = await self.repo.get_by_id(pipeline_id, owner_id)
        if not pipeline:
            raise PipelineNotFoundException(pipeline_id)
        return DataPipelineRead.model_validate(pipeline)

    async def list(self, owner_id: int) -> list[DataPipelineRead]:
        pipelines = await self.repo.get_by_owner(owner_id)
        return [DataPipelineRead.model_validate(p) for p in pipelines]

    async def update(self, pipeline_id: int, owner_id: int, data: DataPipelineUpdate) -> DataPipelineRead:
        pipeline = await self.repo.get_by_id(pipeline_id, owner_id)
        if not pipeline:
            raise PipelineNotFoundException(pipeline_id)

        if data.name is not None:
            pipeline.name = data.name
        if data.description is not None:
            pipeline.description = data.description
        if data.config is not None:
            pipeline.config = data.config

        pipeline = await self.repo.update(pipeline)
        await self.session.commit()
        return DataPipelineRead.model_validate(pipeline)

    async def delete(self, pipeline_id: int, owner_id: int) -> None:
        deleted = await self.repo.delete(pipeline_id, owner_id)
        if not deleted:
            raise PipelineNotFoundException(pipeline_id)
        await self.session.commit()

    async def execute(self, pipeline_id: int, owner_id: int, request: PipelineExecutionRequest) -> PipelineExecutionResult:
        pipeline = await self.repo.get_by_id(pipeline_id, owner_id)
        if not pipeline:
            raise PipelineNotFoundException(pipeline_id)

        await self.repo.update_status(pipeline_id, owner_id, PipelineStatus.RUNNING)
        await self.session.commit()

        start_time = time.time()
        steps_executed = []
        output = None
        error = None

        try:
            config = request.config_override or pipeline.config
            steps = config.get("steps", [])

            data = None
            for i, step_config in enumerate(steps):
                step = PipelineStepConfig(**step_config)
                step_start = time.time()

                data = await self._execute_step(step, data)

                steps_executed.append({
                    "step_index": i,
                    "name": step.name,
                    "type": step.type,
                    "success": True,
                    "execution_time_ms": int((time.time() - step_start) * 1000),
                    "output_shape": self._get_data_shape(data),
                })

            output = {"result": data} if data is not None else {"message": "Pipeline completed"}
            final_status = PipelineStatus.COMPLETED

        except Exception as e:
            error = str(e)
            final_status = PipelineStatus.FAILED

        finally:
            exec_time = int((time.time() - start_time) * 1000)
            await self.repo.update_result(pipeline_id, owner_id, output or {}, final_status)
            await self.session.commit()

        return PipelineExecutionResult(
            success=error is None,
            output=output,
            error=error,
            execution_time_ms=exec_time,
            steps_executed=steps_executed,
        )

    async def _execute_step(self, step: PipelineStepConfig, data: Any) -> Any:
        step_type = step.type
        config = step.config

        if step_type == "ingest":
            return await self._step_ingest(config)
        elif step_type == "clean":
            return await self._step_clean(data, config)
        elif step_type == "transform":
            return await self._step_transform(data, config)
        elif step_type == "analyze":
            return await self._step_analyze(data, config)
        elif step_type == "visualize":
            return await self._step_visualize(data, config)
        elif step_type == "export":
            return await self._step_export(data, config)
        else:
            raise PipelineExecutionException(f"Unknown step type: {step_type}")

    async def _step_ingest(self, config: dict) -> Any:
        source = config.get("source", "sample")
        if source == "sample":
            return {"type": "dataframe", "rows": 100, "columns": 5, "source": "sample_data"}
        elif source == "csv":
            return {"type": "dataframe", "path": config.get("path"), "rows": 0, "columns": 0}
        elif source == "json":
            return {"type": "dataframe", "path": config.get("path"), "rows": 0, "columns": 0}
        else:
            return {"type": "dataframe", "rows": 0, "columns": 0}

    async def _step_clean(self, data: Any, config: dict) -> Any:
        if not data:
            return data
        return {**data, "cleaned": True, "rows_after": data.get("rows", 0)}

    async def _step_transform(self, data: Any, config: dict) -> Any:
        if not data:
            return data
        operations = config.get("operations", [])
        return {**data, "transformed": True, "operations": operations}

    async def _step_analyze(self, data: Any, config: dict) -> Any:
        if not data:
            return {"statistics": {}, "insights": []}
        return {
            "statistics": {"mean": 0, "std": 0, "correlations": {}},
            "insights": ["Sample insight from analysis"],
        }

    async def _step_visualize(self, data: Any, config: dict) -> Any:
        chart_type = config.get("chart_type", "bar")
        return {"charts": [{"type": chart_type, "data": data}]}

    async def _step_export(self, data: Any, config: dict) -> Any:
        format_type = config.get("format", "json")
        return {"exported": True, "format": format_type, "data": data}

    def _get_data_shape(self, data: Any) -> dict:
        if isinstance(data, dict):
            return {k: (len(v) if isinstance(v, list) else type(v).__name__) for k, v in data.items()}
        return {"type": type(data).__name__}