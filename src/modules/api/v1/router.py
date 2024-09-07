from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.modules.db.services import (
    get_db_session, create_table, insert_region_info, 
    get_all_region_info, delete_region_info, delete_all_region_info
)
from src.modules.api.v1.schemas import RegionInfoCreate, RegionInfo


router = APIRouter(prefix="/v1")


@router.post(path="/collect_info")
async def generate_pipeline_response():
    return await service.get_pipeline_response()

@router.post("/create_table")
async def create_region_info_table(db: AsyncSession = Depends(get_db_session)):
    await create_table(db)
    return {"message": "Table created successfully"}

@router.post("/region_info")
async def add_region_info(region_info: RegionInfoCreate, db: AsyncSession = Depends(get_db_session)):
    result = await insert_region_info(db, region_info)
    return {"message": "Region info inserted", "id": result}

@router.get("/region_info", response_model=List[RegionInfo])
async def get_region_info(db: AsyncSession = Depends(get_db_session)):
    return await get_all_region_info(db)

@router.delete("/region_info/{region_id}")
async def remove_region_info(region_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await delete_region_info(db, region_id)
    if result:
        return {"message": f"Region info with id {region_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Region info not found")

@router.delete("/region_info")
async def delete_all_region_info_route(db: AsyncSession = Depends(get_db_session)):
    try:
        await delete_all_region_info(db)
        return {"message": "All region info deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")