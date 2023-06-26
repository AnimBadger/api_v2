from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import models, schemas
from . import oauth2
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/',  response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 3):
    posts = db.query(models.Post).limit(limit).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.PostResponse)
def add_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}')
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {id} can not be found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    _post = post.first()

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {id} can not be found')
    if _post.owner_id != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized')

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    _post = post_query.first()

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The id {id} can not be found')

    if _post.owner_id != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
