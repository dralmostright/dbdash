from fastapi import APIRouter, Depends, status, UploadFile, File
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserPasswordData, UserInfoData
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import (
    create_access_token,
    verify_password,
    decode_url_safe_token,
)
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.config import Config
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken,UserNotFound, PasswordIncorrect

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['user','admin'])
admin_checker = RoleChecker(['admin'])
access_token_bearer = AccessTokenBearer()

@auth_router.post('/register', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = user_service.user_exsits(email,session)
    if await user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login')
async def login_users(login_data: UserLoginModel,session: AsyncSession = Depends(get_session)):
    email=login_data.email
    password=login_data.password_hash
    
    user= await user_service.get_user_verified_by_email(email, session)
    #user= await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token=create_access_token(
                userdata ={
                    'email': user.email,
                    'user_uid':str(user.uid),
                    'role':str(user.role),
                    'first_name' : user.first_name,
                    'last_name' : user.last_name
                }
                ,expiry=timedelta(seconds=Config.ACCESS_TOKEN_EXPIRY)
            )
            refresh_token = create_access_token(
                userdata ={
                    'email': user.email,
                    'user_uid':str(user.uid),
                    'role':str(user.role),
                    'first_name' : user.first_name,
                    'last_name' : user.last_name
                },
                refresh=True,
                expiry=timedelta(days=Config.REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse (
                content={
                    "message": "Login Successful",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "user": {
                        "email" : user.email,
                        "uid": str(user.uid),
                        "first_name" : user.first_name,
                        "last_name" : user.last_name,
                        'role':str(user.role),
                        "display_pic": user.display_pic,
                    }
                }
            )
    raise InvalidCredentials()
    
@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(userdata=token_details['user'], expiry=None)
        return JSONResponse(content={"access_token": new_access_token})
    raise InvalidToken()

@auth_router.get('/logout')
async def revoke_token(token_details:dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']  
    revoke_token(jti)
    #await add_jti_to_blocklist (jti)
    return JSONResponse (
        content={
            "message":"Logged out Successfully"
        },
        status_code=status.HTTP_200_OK
    )
    
@auth_router.get('/me', response_model=UserModel)
async def get_current_user(user = Depends(get_current_user)):
    #print(user)
    return user

  
@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {"is_verified": True}, session)
        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    
@auth_router.get("/allusers", response_model=list[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    all_users = await user_service.list_all_users(session)
    return all_users


@auth_router.patch('/user/update', response_model=UserModel)
async def update_dbash_user(uid: str, user_up_data:UserCreateModel,session:AsyncSession = Depends(get_session),_:bool = Depends(admin_checker), token_details : dict =Depends(access_token_bearer)) -> dict:
    update_account = await user_service.update_dbash_user(uid, user_up_data, session)
    if update_account:
        return update_account
    else:
        raise UserNotFound 
    
@auth_router.get('/user/details', response_model=UserModel)
async def get_user_by_uid(uid: str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)) -> dict:
    user = await user_service.get_user_by_uid(uid, session)
    if user:
        return user
    else:
        raise UserNotFound 
    
@auth_router.delete('/user/remove',status_code= status.HTTP_204_NO_CONTENT)
async def delete_user(uid:str,session:AsyncSession = Depends(get_session),_:bool = Depends(admin_checker), token_details : dict =Depends(access_token_bearer)):
    delete_aws_account = await user_service.delete_user(uid,session)
    if delete_aws_account is None:
        raise UserNotFound
    else:
        return {}
    
@auth_router.post("/user/change/displaypic")
async def update_profile_photo(uid:str, file: UploadFile = File(...),session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    url = await user_service.update_profile_photo(uid, file,session)
    return {"message": "Photo uploaded", "url": url}

@auth_router.patch("/user/change/password", response_model=UserModel)
async def update_password(uid:str, user_data: UserPasswordData,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    url = await user_service.update_password(uid, user_data,session)
    if url:
        return url
    else:
        raise PasswordIncorrect
    
@auth_router.patch("/user/change/basicinfo", response_model=UserModel)
async def update_profile_info(uid:str, user_data: UserInfoData,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    url = await user_service.update_profile_info(uid, user_data,session)
    if url:
        return url
    else:
        raise UserNotFound
    
