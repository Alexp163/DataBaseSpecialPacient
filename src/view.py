from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from patients.models import Patient
from templates import render_template

router = APIRouter(tags=["index"])


@router.get("/")
async def index(request: Request):
    return render_template(request, "index.html")


@router.get("/add_review", response_class=HTMLResponse, name="add_review")
async def add_review_form(request: Request):
    return render_template(
        request,
        "add_review.html",
        form={},
        errors={},
    )

# @router.post("/add_review", response_class=HTMLResponse)
# async def add_review_post(request: Request):   # те же Form-параметры, что обсуждали
#     return RedirectResponse(url="/patients/success", status_code=303)


@router.get("/reviews")
async def reviews(request: Request):
    return render_template(request, "reviews.html")


@router.get("/patient/success", response_class=HTMLResponse, name="patient_success")
async def patient_success(request: Request):
    return render_template(request, "patient_success.html")
