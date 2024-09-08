from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.modules.api.v1.schemas import RegionInfoCreate

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@db/mydatabase"

engine = create_async_engine(
    DATABASE_URL
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        print("Initializing database...")
        # Add any initialization logic here if needed
        pass


async def create_region_table(db: AsyncSession, table_name: str):
    await db.execute(text(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100),
        explosion BOOLEAN,
        num_of_explosions INT,
        damage BOOLEAN,
        victims BOOLEAN,
        num_of_victims INT
    )
    """))
    print(f"Table '{table_name}' created successfully")
    await db.commit()


async def create_user_request_table(db: AsyncSession, table_name: str):
    # for later
    await db.execute(text(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100),
        explosion BOOLEAN,
        num_of_explosions INT,
        damage BOOLEAN,
        victims BOOLEAN,
        num_of_victims INT
    )
    """))
    print(f"Table '{table_name}' created successfully")
    await db.commit()

async def insert_region_info(db: AsyncSession, table_name: str, region_info: RegionInfoCreate):
    query = text(f"""
    INSERT INTO {table_name} (city, explosion, num_of_explosions, damage, victims, num_of_victims)
    VALUES (:city, :explosion, :num_of_explosions, :damage, :victims, :num_of_victims)
    RETURNING id
    """)
    result = await db.execute(query, region_info.dict())
    await db.commit()
    print(f"Data inserted successfully into {table_name}")
    return result.scalar_one()


async def get_all_region_info(db: AsyncSession, table_name: str):
    result = await db.execute(text(f"SELECT * FROM {table_name}"))
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]  # Convert Row objects to dictionaries


async def delete_region_info(db: AsyncSession, table_name: str, region_id: int):
    result = await db.execute(text(f"DELETE FROM {table_name} WHERE id = :id"), {"id": region_id})
    await db.commit()
    return result.rowcount > 0


async def delete_all_region_info(db: AsyncSession, table_name: str):
    await db.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
    await db.commit()


async def create_region_info(db: AsyncSession, table_name: str, region_info: RegionInfoCreate):
    return await insert_region_info(db, table_name, region_info)
