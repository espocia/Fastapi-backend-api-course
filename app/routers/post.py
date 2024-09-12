from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/post", tags=["Post"])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = ""
    
):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        utils.raise_404(f"post with id {id} not found")
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    get_current_user = Depends(oauth2.get_current_user),
):

    new_post = models.Post(owner_id=get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user = Depends(oauth2.get_current_user),
):

    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    

    if post  == None:
        utils.raise_404(f"post with id {id} not found")
        
    if post.owner_id != get_current_user.id:
        utils.raise_403("Deleting post not associated to your account is prohibited")


    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post_data: schemas.PostCreate,
    db: Session = Depends(get_db),
    get_current_user = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        utils.raise_404(f"post with id {id} not found")
    
    if post.owner_id != get_current_user.id:
        utils.raise_403("Altering post not associated to your account is prohibited")
        
    post_query.update({**post_data.model_dump()}, synchronize_session=False)

    db.commit()
    updated_post = post_query.filter(models.Post.id == id).first()
    return updated_post
