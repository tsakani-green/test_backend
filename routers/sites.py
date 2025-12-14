# routers/sites.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId

from db import sites_collection
from auth import get_current_admin

router = APIRouter(prefix="/sites", tags=["sites"])


class SiteCreate(BaseModel):
    organisationId: str
    name: str
    location: str | None = None


class SiteOut(BaseModel):
    id: str
    organisationId: str
    name: str
    location: str | None = None


def site_doc_to_out(doc: dict) -> SiteOut:
    return SiteOut(
        id=str(doc["_id"]),
        organisationId=str(doc.get("organisationId")),
        name=doc.get("name"),
        location=doc.get("location"),
    )


@router.get("/", response_model=list[SiteOut])
async def list_sites(admin=Depends(get_current_admin)):
    docs = sites_collection.find({})
    return [site_doc_to_out(doc) async for doc in docs]


@router.post("/", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
async def create_site(payload: SiteCreate, admin=Depends(get_current_admin)):
    try:
        org_id = ObjectId(payload.organisationId)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid organisation id")

    new_doc = {
        "organisationId": org_id,
        "name": payload.name,
        "location": payload.location,
    }
    res = await sites_collection.insert_one(new_doc)
    created = await sites_collection.find_one({"_id": res.inserted_id})
    return site_doc_to_out(created)
