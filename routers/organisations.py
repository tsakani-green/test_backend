# routers/organisations.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId

from db import organisations_collection
from auth import get_current_admin

router = APIRouter(prefix="/organisations", tags=["organisations"])


class OrganisationCreate(BaseModel):
    name: str
    country: str | None = None
    sector: str | None = None


class OrganisationOut(BaseModel):
    id: str
    name: str
    country: str | None = None
    sector: str | None = None


def org_doc_to_out(doc: dict) -> OrganisationOut:
    return OrganisationOut(
        id=str(doc["_id"]),
        name=doc.get("name"),
        country=doc.get("country"),
        sector=doc.get("sector"),
    )


@router.get("/", response_model=list[OrganisationOut])
async def list_organisations(admin=Depends(get_current_admin)):
    docs = organisations_collection.find({})
    return [org_doc_to_out(doc) async for doc in docs]


@router.post("/", response_model=OrganisationOut, status_code=status.HTTP_201_CREATED)
async def create_organisation(
    payload: OrganisationCreate,
    admin=Depends(get_current_admin),
):
    new_doc = payload.dict()
    res = await organisations_collection.insert_one(new_doc)
    created = await organisations_collection.find_one({"_id": res.inserted_id})
    return org_doc_to_out(created)


@router.get("/{org_id}", response_model=OrganisationOut)
async def get_organisation(org_id: str, admin=Depends(get_current_admin)):
    try:
        _id = ObjectId(org_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid organisation id")

    doc = await organisations_collection.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Organisation not found")

    return org_doc_to_out(doc)
