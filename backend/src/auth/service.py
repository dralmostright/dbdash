from src.db.models import User
from .schemas import UserCreateModel,UserUpdateModel
from .utils import generate_passwd_hash, generate_unique_filename, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import os
import shutil
from fastapi import UploadFile, HTTPException
from src.config import Config

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement=select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def get_user_verified_by_email(self, email: str, session: AsyncSession):
        statement = select(User) \
            .where((User.email == email)  & (User.is_verified == True))
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user  
    
    async def get_user_by_uid(self, uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == uid)
        result = await session.exec(statement)
        user = result.first()
        return user    
    
    async def user_exsits(self, email:str, session: AsyncSession):
        useremail = await self.get_user_by_email(email, session)
        username = await self.get_user_by_email(email, session)
        return useremail is not None or username is not None
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User (
            **user_data_dict
        )
        new_user.password_hash=generate_passwd_hash(user_data_dict['password_hash'])
        if new_user.role is None or new_user.role == "":
            new_user.role = "user"
        if new_user.is_verified is None or new_user.is_verified == "":
            new_user.is_verified = False           
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def list_all_users(self, session: AsyncSession):
        statement = select(User).where(1==1)
        results = await session.exec(statement)
        users = results.all()
        return users

    async def update_dbash_user(
        self, uid: str, update_data: UserUpdateModel, session: AsyncSession
    ):
        user_to_update = await self.get_user_by_uid(uid, session)
        if user_to_update:
            update_data_dict = update_data.model_dump()
            password_hash = update_data_dict.get("password_hash")
            if password_hash is None or password_hash == "":
                update_data_dict.pop("password_hash", None)
            else:
                password_hash=generate_passwd_hash(update_data_dict['password_hash'])
                update_data_dict["password_hash"] = password_hash
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            await session.commit()
            return user_to_update
        else:
            return None
        
    async def delete_user(self, uid: str, session: AsyncSession):
        account_to_delete = await self.get_user_by_uid(uid, session)
        if account_to_delete is not None:
            await session.delete(account_to_delete)
            await session.commit()
            return {}
        else:
            return None
        
    async def update_profile_photo(self, uid : str, file: UploadFile, session: AsyncSession):

        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(Config.FILE_DIRECTORY,'dpicture', filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        user = await self.get_user_by_uid(uid, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.display_pic = f"{file_path}"  
        await session.commit()
    
        return f"/static/profile/{file.filename}"
    
    async def update_password(self, uid : str, user_data, session: AsyncSession):
        user_to_update = await self.get_user_by_uid(uid, session)
        
        if user_to_update:
            update_data_dict = user_data.model_dump()
            if verify_password(update_data_dict['password_hash'], user_to_update.password_hash):
                new_password_hash = generate_passwd_hash(update_data_dict['new_password_hash'])
                update_data_dict["password_hash"] = new_password_hash
                update_data_dict.pop("new_password_hash", None)
                for k, v in update_data_dict.items():
                    setattr(user_to_update, k, v)
                await session.commit() 
                return user_to_update               
            else:
                return None
        else:
            return None        
        
    async def update_profile_info(self, uid : str, user_data, session: AsyncSession):
        user_to_update = await self.get_user_by_uid(uid, session)
        
        if user_to_update:
            update_data_dict = user_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            await session.commit() 
            return user_to_update               
        else:
            return None   
