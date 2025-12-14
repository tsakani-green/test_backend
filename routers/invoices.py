# routers/invoices.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId
from datetime import date

from db import invoices_collection
from auth import get_current_admin

router = APIRouter(prefix="/invoices", tags=["invoices"])


class InvoiceCreate(BaseModel):
    siteId: str
    invoiceNumber: str
    periodStart: date
    periodEnd: date
    totalKwh: float
    totalAmount: float
    taxInvoice: str | None = None


class InvoiceOut(BaseModel):
    id: str
    siteId: str
    invoiceNumber: str
    periodStart: date
    periodEnd: date
    totalKwh: float
    totalAmount: float
    taxInvoice: str | None = None


def invoice_doc_to_out(doc: dict) -> InvoiceOut:
    return InvoiceOut(
        id=str(doc["_id"]),
        siteId=str(doc["siteId"]),
        invoiceNumber=doc["invoiceNumber"],
        periodStart=doc["periodStart"],
        periodEnd=doc["periodEnd"],
        totalKwh=doc["totalKwh"],
        totalAmount=doc["totalAmount"],
        taxInvoice=doc.get("taxInvoice"),
    )


@router.get("/", response_model=list[InvoiceOut])
async def list_invoices(admin=Depends(get_current_admin)):
    docs = invoices_collection.find({})
    return [invoice_doc_to_out(doc) async for doc in docs]


@router.post("/", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
async def create_invoice(payload: InvoiceCreate, admin=Depends(get_current_admin)):
    try:
        site_id = ObjectId(payload.siteId)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid site id")

    new_doc = payload.dict()
    new_doc["siteId"] = site_id
    res = await invoices_collection.insert_one(new_doc)
    created = await invoices_collection.find_one({"_id": res.inserted_id})
    return invoice_doc_to_out(created)
