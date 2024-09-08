from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.modules.db.services import (
    get_db_session, create_region_table, create_user_request_table,insert_region_info, 
    get_all_region_info, delete_region_info, delete_all_region_info
)
from src.modules.api.v1.schemas import RegionInfoCreate, RegionInfo


router = APIRouter(prefix="/v1")


@router.post(path="/collect_info")
async def generate_pipeline_response():
    return await service.get_pipeline_response()

# db routes
@router.post("/create_region_table")
async def create_region_info_table(table_name: str = "region_info", db: AsyncSession = Depends(get_db_session)):
    await create_region_table(db, table_name)
    return {"message": "Table created successfully"}

@router.post("/create_requests_table")
async def create_requests_info_table(table_name: str = "requests_info", db: AsyncSession = Depends(get_db_session)):
    await create_user_request_table(db, table_name)
    return {"message": "Table created successfully"}

@router.post("/region_info")
async def add_region_info(region_info: RegionInfoCreate, table_name: str = "region_info", db: AsyncSession = Depends(get_db_session)):
    result = await insert_region_info(db, table_name, region_info)
    return {"message": "Region info inserted", "id": result}

@router.get("/region_info", response_model=List[RegionInfo])
async def get_region_info(table_name: str = "region_info", db: AsyncSession = Depends(get_db_session)):
    return await get_all_region_info(db, table_name)

@router.delete("/region_info/{region_id}")
async def remove_region_info(region_id: int = 1, table_name: str = "region_info", db: AsyncSession = Depends(get_db_session)):
    result = await delete_region_info(db, table_name, region_id)
    if result:
        return {"message": f"Region info with id {region_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Region info not found")

@router.delete("/region_info")
async def delete_all_region_info_route(table_name: str = "region_info", db: AsyncSession = Depends(get_db_session)):
    try:
        await delete_all_region_info(db, table_name)
        return {"message": "All region info deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")