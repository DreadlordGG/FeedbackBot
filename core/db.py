import os
import sys
import asyncio
import datetime
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.logging import getLogger
from core.models import Base
from core.models import General
from core.settings import Config

conf=Config()
logger=getLogger(__name__)

class async_pgsql():
    def __init__(self, database):
        self.database = database
        self.engine = None

    async def create_engine(self):
        connection_string = f"postgresql+asyncpg://{conf.DATABASE_USER}:{conf.DATABASE_PASSWORD}@{conf.DATABASE_HOST}/{conf.DATABASE}"
        self.engine = create_async_engine(
            connection_string, 
            poolclass=AsyncAdaptedQueuePool,
            echo=True,
            pool_size=int(conf.DATABASE_POOLSIZE),
            isolation_level=conf.DATABASE_ISOLATION_LEVEL
        )
        async with self.engine.begin() as conn:
            #await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async with self.engine.connect() as conn:
            stmt = (
                insert(General).
                values(start_time=datetime.datetime.now(), id=1)
            )
            on_duplicate_key_stmt = stmt.on_conflict_do_update(
                index_elements=['id'],
                set_=dict(start_time=datetime.datetime.now())
            )
            result = await conn.execute(on_duplicate_key_stmt)
            logger.info(f"Uptime updated.")
        logger.info(f"Database pool created. Ready for connections")
        return self.engine

    async def test_db(self, engine):
        try:
            async with engine.connect() as conn:
                stmt = (
                    select(General)
                )
                result = await conn.execute(stmt)
            logger.info("Database test successfully passed.")
            return True
        except Exception as e:
            logger.error(f"Database test failed {e}")
            return False