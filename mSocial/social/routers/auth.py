from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from . import oauth2
from ..database import get_db
router = APIRouter(
    tags=['Auth']
)


@router.post('/login', response_model=schemas.Token)
# credentials before. credentials:schemas.UserLogin
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == credentials.username).first()
    # OAuth2 uses username and password

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid details')

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, "token_type": "bearer"}
