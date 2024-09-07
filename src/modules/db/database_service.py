from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.modules.api.v1.schemas import RegionInfoCreate

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@db/mydatabase"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"server_settings": {"timezone": "UTC"}}
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        # Add any initialization logic here if needed
        pass


async def create_table(db: AsyncSession):
    await db.execute(text("""
    CREATE TABLE IF NOT EXISTS region_info (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100),
        explosion BOOLEAN,
        num_of_explosions INT,
        damage BOOLEAN,
        victims BOOLEAN,
        num_of_victims INT
    )
    """))
    await db.commit()

async def insert_region_info(db: AsyncSession, region_info: RegionInfoCreate):    
    result = await db.execute(text("""
    INSERT INTO region_info (city, explosion, num_of_explosions, damage, victims, num_of_victims)
    VALUES (:city, :explosion, :num_of_explosions, :damage, :victims, :num_of_victims)
    RETURNING id
    """), region_info.dict())
    await db.commit()
    return result.scalar_one()

async def get_all_region_info(db: AsyncSession):
    result = await db.execute(text("SELECT * FROM region_info"))
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]  # Convert Row objects to dictionaries

async def delete_region_info(db: AsyncSession, region_id: int):
    result = await db.execute(text("DELETE FROM region_info WHERE id = :id"), {"id": region_id})
    await db.commit()
    return result.rowcount > 0

async def delete_all_region_info(db: AsyncSession):
    await db.execute(text("DELETE FROM region_info"))
    await db.commit()

async def create_region_info(db: AsyncSession, region_info: RegionInfoCreate):
    return await insert_region_info(db, region_info)
