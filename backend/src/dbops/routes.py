from fastapi import APIRouter, Depends, status, BackgroundTasks
from typing import Optional, List
from .schemas import ExecLogCreate, ExecLogRead, JiraMetaCreate, JiraMetaRead, JiraTicketCreate, JiraTicketRead, ExecJobCreate , ExecJobResponse , \
    MSDBServerCreateWithMounts, MSDBServerReadWithMounts, MSDBServersRead, MSDBServerUpdateWithMounts, JiraTicketDetailBase, ProvisionData, ExecJobLogBase
from .service import DbopsService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.config import Config
from src.errors import JiraMetaNameAlreadyExists, JiraMetaDataNotFound,InvalidParameters, ServerAlreadyExists, ServerNotFound 
from src.auth.dependencies import AccessTokenBearer

dbops_router = APIRouter()
dbops_service = DbopsService()
access_token_bearer = AccessTokenBearer()

@dbops_router.post("/jira/meta/create", response_model=JiraMetaRead, status_code=status.HTTP_201_CREATED)
async def create_jira_meta(data : JiraMetaCreate, session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jira_meta = await dbops_service.create_jira_meta(data, session)
    if jira_meta is None:
        raise JiraMetaNameAlreadyExists
    return jira_meta

@dbops_router.get("/jira/meta/get", response_model=list[JiraMetaRead])
async def get_jira_meta(jira_dbdash_uid: str, jira_id: Optional[str] = None, session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jira_meta = await dbops_service.get_jira_meta(jira_dbdash_uid = jira_dbdash_uid, jira_id = jira_id, session = session)
    return jira_meta

@dbops_router.get("/jira/meta/getbyid/{jira_id}", response_model=JiraMetaRead)
async def get_jira_meta_by_jira_id(jira_id: str, session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jira_meta = await dbops_service.get_jira_meta_by_jira_id(jira_id = jira_id, session = session) 
    return jira_meta

@dbops_router.patch('/jira/meta/update/{jira_id}', response_model=JiraMetaRead)
async def update_jira_meta(jira_id: str, jira_meta_data:JiraMetaCreate,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)) -> dict:
    jira_meta = await dbops_service.update_jira_meta(jira_id, jira_meta_data, session)
    if jira_meta:
        return jira_meta
    else:
        raise JiraMetaDataNotFound 

@dbops_router.delete('/jira/meta/delete/{jira_id}',status_code= status.HTTP_204_NO_CONTENT)
async def delete_jira_meta(jira_id:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jira_meta = await dbops_service.delete_jira_meta(jira_id,session)
    if jira_meta is None:
        raise JiraMetaDataNotFound
    else:
        return {}

@dbops_router.post('/msserver/create', response_model=MSDBServerReadWithMounts, status_code=status.HTTP_201_CREATED)
async def create_mssql_server(data:MSDBServerCreateWithMounts, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    #print(data)
    msserver = await dbops_service.create_mssql_server(data,session)
    if msserver is None:
        raise ServerAlreadyExists
    return msserver

@dbops_router.get('/msserver/server/get', response_model=list[MSDBServersRead])
async def get_msserver(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    msserver = await dbops_service.get_msserver(session)
    return msserver

@dbops_router.get('/msserver/server/get/snm', response_model=list[MSDBServerReadWithMounts])
async def get_msserver(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    msserver = await dbops_service.get_msserver_mounts_all(session)
    return msserver

@dbops_router.get('/msserver/server/mount/{msdbs_id}',response_model=MSDBServerReadWithMounts)
async def get_msserver_mounts(msdbs_id:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    msserver = await dbops_service.get_msserver_mounts(msdbs_id,session)
    if msserver is None:
        raise ServerNotFound
    else:
        return msserver

@dbops_router.patch('/msserver/server/update/{msdbs_id}',response_model=MSDBServerReadWithMounts)
async def update_msserver_mounts(msdbs_id: str, data : MSDBServerUpdateWithMounts ,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    msserver = await dbops_service.update_msserver_mounts(msdbs_id, data, session)
    if msserver is None:
        raise JiraMetaDataNotFound
    else:
        return msserver

@dbops_router.delete('/msserver/server/delete/{msdbs_id}',status_code= status.HTTP_204_NO_CONTENT)
async def delete_msserver_mounts(msdbs_id:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    msserver = await dbops_service.delete_msserver(msdbs_id,session)
    if msserver is None:
        raise JiraMetaDataNotFound
    else:
        return {}

@dbops_router.delete('/msserver/server/mount/delete/{msdbsm_id}',status_code= status.HTTP_204_NO_CONTENT)
async def delete_msserver_mpoint(msdbsm_id:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    print(msdbsm_id)
    msserver = await dbops_service.delete_msserver_mpoint(msdbsm_id,session)
    if msserver is None:
        raise JiraMetaDataNotFound
    else:
        return {}

@dbops_router.get('/jira/ticket/details/{jira_id}/{jira_ticket}', response_model=JiraTicketDetailBase)
async def get_jira_ticket_details(jira_id:str,jira_ticket : str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jiradetails = await dbops_service.get_jira_ticket_details(jira_id,jira_ticket,session)
    if jiradetails is None:
        raise ServerNotFound
    else:
        return jiradetails

@dbops_router.post('/msserver/provision/database', status_code=status.HTTP_201_CREATED)
async def provision_database(runmode:str,data : ProvisionData,bg_tasks:BackgroundTasks, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jiradetails = await dbops_service.create_provision_database_job(runmode,data,token_details,session,bg_tasks)
    if jiradetails is None:
        raise None
    else:
        return jiradetails
    
@dbops_router.get('/msserver/provision/database/jobs', response_model=list[ExecJobResponse])
async def get_jira_ticket_details(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jobs = await dbops_service.get_all_local_jobs(session)
    if jobs is None:
        raise ServerNotFound
    else:
        return jobs

@dbops_router.get('/msserver/provision/database/jobs/{job_id}', response_model=ExecJobResponse)
async def get_all_local_job_by_id(job_id:str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jobs = await dbops_service.get_all_local_job_by_id(job_id,session)
    if jobs is None:
        raise ServerNotFound
    else:
        return jobs     

@dbops_router.get('/msserver/provision/database/job/logs/{job_id}', response_model=list[ExecJobLogBase])
async def get_local_job_logs_by_id(job_id:str, sincetime: Optional[datetime] = None, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jobs = await dbops_service.get_local_job_logs_by_id(job_id,sincetime, session)
    if jobs is None:
        raise ServerNotFound
    else:
        return jobs      
"""
@dbops_router.post('/msserver/provision/database/runtype=?{runmode}', response_model=MSDBServerReadWithMounts, status_code=status.HTTP_201_CREATED)
async def provision_database(runmode:str,data : ProvisionData, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    jiradetails = await dbops_service.provision_database(runmode,data,session)
    if jiradetails is None:
        raise ServerNotFound
    else:
        return jiradetails
"""