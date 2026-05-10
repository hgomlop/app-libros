from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Book, User
from schemas import BookCreate, BookUpdate, BookOut
from routers.auth import get_current_user

router = APIRouter()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[BookOut])
def get_books(
    status: Optional[str] = Query(None, description="Filter: reading | finished | wishlist"),
    year: Optional[int] = Query(None, description="Filter by year read"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Book).filter(Book.user_id == current_user.id)
    if status:
        query = query.filter(Book.status == status)
    if year:
        query = query.filter(Book.year_read == year)
    return query.order_by(Book.created_at.desc()).all()


@router.get("/recent", response_model=List[BookOut])
def get_recent_books(
    limit: int = Query(5, description="Number of recent books to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Book)
        .filter(Book.user_id == current_user.id, Book.status == "finished")
        .order_by(Book.finish_date.desc(), Book.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/current", response_model=Optional[BookOut])
def get_current_book(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Book)
        .filter(Book.user_id == current_user.id, Book.status == "reading")
        .order_by(Book.start_date.desc())
        .first()
    )


@router.get("/recommended", response_model=List[BookOut])
def get_recommended_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Book)
        .filter(Book.user_id == current_user.id, Book.is_recommended == True)
        .order_by(Book.rating.desc())
        .all()
    )


@router.get("/{book_id}", response_model=BookOut)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = Book(**book_data.model_dump(), user_id=current_user.id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    for field, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == current_user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(book)
    db.commit()
