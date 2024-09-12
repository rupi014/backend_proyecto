from sqlalchemy.orm import Session
from models import *
from schemas import *

def get_blog(db: Session):
    return db.query(Blog).all()

def get_blog_by_id(db: Session, blog_id: int):
    return db.query(Blog).filter(Blog.id == blog_id).first()

def create_blog(db: Session, blog: BlogData):
    db_blog = Blog(title=blog.title, content=blog.content, image=blog.image, date=blog.date, author_id=blog.author_id)
    db.add(db_blog)
    db.commit()
    db.flush(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return True
    return False

def update_blog(db: Session, blog_id: int, blog: BlogData):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if db_blog:
        db_blog.title = blog.title
        db_blog.content = blog.content
        db_blog.image = blog.image
        db_blog.date = blog.date    
        db.commit()
        db.flush(db_blog)
        return db_blog
    return False            


