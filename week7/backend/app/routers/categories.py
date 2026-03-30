from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Category
from ..schemas import CategoryCreate, CategoryPatch, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[CategoryRead]:
    stmt = select(Category)
    if q:
        stmt = stmt.where(Category.name.contains(q))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Category, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Category, sort_field)))
    else:
        stmt = stmt.order_by(desc(Category.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [CategoryRead.model_validate(row) for row in rows]


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> CategoryRead:
    category = Category(name=payload.name)
    db.add(category)
    db.flush()
    db.refresh(category)
    return CategoryRead.model_validate(category)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryRead:
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryRead.model_validate(category)


@router.patch("/{category_id}", response_model=CategoryRead)
def patch_category(category_id: int, payload: CategoryPatch, db: Session = Depends(get_db)) -> CategoryRead:
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if payload.name is not None:
        category.name = payload.name
    db.add(category)
    db.flush()
    db.refresh(category)
    return CategoryRead.model_validate(category)
