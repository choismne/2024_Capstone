from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from pydantic import BaseModel
from database import SessionLocal, engine
from login.models import User, Mood, Pose
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os

SECRET_KEY = os.environ['AUTH_SECRET_KEY']
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login')

router = APIRouter()
class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str

class LoginForm(BaseModel):
    username : str
    password : str  

def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close() 

db_dependency = Annotated[Session, Depends(get_db)]

#bcrypt로 패스워드 해싱
def get_password_hash(password):  
    return bcrypt_context.hash(password)

#패스워드 확인 bcrypt_context.verify(입력받은 패스워드, 해싱된 패스워드)
def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)

# 이 유저가 맞는지 확인하는 함수 
def authenticate_user(username : str, password : str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#jwt토큰(액세스 토큰) 생성 함수
def create_access_token(username : str, user_id : int, role : str, expires_delta : timedelta): 
    encode = {'sub' : username, 'id' : user_id, 'role' : role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


#로그인 엔드포인트
#로그인 성공하면 jwt토큰을 생성해서 반환, LoginForm pydantic모델로 유효성 검증
@router.post('/login', status_code=status.HTTP_200_OK)
#안드로이드 올릴때는 Form으로 안받고, LoginForm으로 받아서 쓰자.
async def login(db : db_dependency, login_form : LoginForm):
    #유저 인증 함수 호출
    user = authenticate_user(login_form.username, login_form.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
    #jwt토큰 생성 함수
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=24*60))

    return {'access_token' : token, 'token_type' : 'bearer'}
    

#토큰을 받는 코드 쪽, http로 토큰을 받고 유효성을 검사한다. 
#Request객체에는 헤더에서 전송된 모든 정보가 포함되어있어요. 그래서 추출해서 쓰면 됩니다. 
#Splash 에서 여기로 토큰을 보내주면 여기서 토큰을 검사하고 유효하면 토큰이 유효하다는 메시지를 반환합니다.
#토큰이 유효하면 자동로그인 처리해서 바로 main fragment로 이동하고, 토큰이 유효하지 않으면 로그인 화면으로 이동합니다.
async def verify_token(request : Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token',
        )
    
@router.post("/check_token", status_code=status.HTTP_200_OK)
async def check_token(token : Annotated[str, Depends(oauth2_bearer)]):
    return {"message": "Token is valid"}


#유저 생성 엔드포인트, 회원가입
#Swagger UI 용
@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency, create_user_request : CreateUserRequest):
    #models.py에서 Users 클래스를 이용해 유저 생성
    create_user_model = User(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = get_password_hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)

    create_mood_model = Mood(username=create_user_request.username)
    create_pose_model = Pose(username=create_user_request.username)

    db.add(create_mood_model)
    db.add(create_pose_model)

    db.commit()