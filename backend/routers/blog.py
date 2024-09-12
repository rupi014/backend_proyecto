from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import BlogData
import crud.blog_crud as blog_crud
from database import engine, SessionLocal
from models import Base

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
            db.close()

router = APIRouter(prefix="/blog", tags=["Blog"], responses={404: {"description": "No encontrado"}})  

Base.metadata.create_all(bind=engine)

@router.post("/", response_model=BlogData)
async def create_blog(blog: BlogData, db: Session = Depends(get_db)):
    check_blog = blog_crud.get_blog_by_id(db, blog_id=blog.id)
    if check_blog:
        raise HTTPException(status_code=400, detail="El blog ya existe")
    return blog_crud.create_blog(db=db, blog=blog)

@router.get("/", response_model=list[BlogData])
async def get_blog(db: Session = Depends(get_db)):
    blog = blog_crud.get_blog(db)
    if not blog:
        raise HTTPException(status_code=404, detail="No se encontraron blogs")
    return blog

@router.get("/{blog_id}", response_model=BlogData)
async def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = blog_crud.get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog no encontrado")
    return blog

@router.get("/user/{user_id}/blogs", response_model=list[BlogData])
async def get_blogs_by_user(user_id: int, db: Session = Depends(get_db)):
    blogs = blog_crud.get_blogs_by_user(db, user_id)
    if not blogs:
        raise HTTPException(status_code=404, detail="No se encontraron blogs para este usuario")
    return blogs

@router.delete("/{blog_id}", response_model=dict)
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    success = blog_crud.delete_blog(db, blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blog no encontrado")
    return {"message": f"Blog con ID {blog_id} eliminado correctamente"}

@router.put("/{blog_id}", response_model=BlogData)
async def update_blog(blog_id: int, blog: BlogData, db: Session = Depends(get_db)):
    db_blog = blog_crud.update_blog(db, blog_id, blog)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog no encontrado")
    return db_blog

         
