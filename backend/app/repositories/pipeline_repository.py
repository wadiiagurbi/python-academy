from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.data_pipeline import DataPipeline, PipelineStatus


class DataPipelineRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, pipeline: DataPipeline) -> DataPipeline:
        self.session.add(pipeline)
        await self.session.flush()
        await self.session.refresh(pipeline)
        return pipeline

    async def get_by_id(self, pipeline_id: int, owner_id: int) -> Optional[DataPipeline]:
        result = await self.session.execute(
            select(DataPipeline).where(
                DataPipeline.id == pipeline_id, DataPipeline.owner_id == owner_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_owner(self, owner_id: int) -> list[DataPipeline]:
        result = await self.session.execute(
            select(DataPipeline)
            .where(DataPipeline.owner_id == owner_id)
            .order_by(DataPipeline.updated_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, pipeline: DataPipeline) -> DataPipeline:
        await self.session.flush()
        await self.session.refresh(pipeline)
        return pipeline

    async def delete(self, pipeline_id: int, owner_id: int) -> bool:
        result = await self.session.execute(
            delete(DataPipeline).where(
                DataPipeline.id == pipeline_id, DataPipeline.owner_id == owner_id
            )
        )
        return result.rowcount > 0

    async def update_status(self, pipeline_id: int, owner_id: int, status: PipelineStatus) -> bool:
        pipeline = await self.get_by_id(pipeline_id, owner_id)
        if not pipeline:
            return False
        pipeline.status = status
        await self.session.flush()
        return True

    async def update_result(
        self, pipeline_id: int, owner_id: int, result: dict, status: PipelineStatus
    ) -> bool:
        pipeline = await self.get_by_id(pipeline_id, owner_id)
        if not pipeline:
            return False
        pipeline.last_result = result
        pipeline.status = status
        await self.session.flush()
        return True