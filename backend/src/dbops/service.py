#from datetime import timedelta, datetime
#from fastapi import BackgroundTasks
#import requests
from collections import defaultdict
from src.db.models import ExecLog, JiraMeta, JiraTicket, ExecJob, MSDBServers, MSDBSmounts
from sqlmodel.ext.asyncio.session import AsyncSession
#from sqlalchemy.orm import selectinload,joinedload,contains_eager
from sqlmodel import select, func, literal, case
from sqlalchemy import desc, text, tuple_, Date, String, union_all, delete
from typing import Optional
from .schemas import ExecLogCreate, ExecLogRead, JiraMetaCreate, JiraMetaRead, JiraTicketCreate, JiraTicketRead, ExecJobCreate , ExecJobRead, \
    MSDBServerCreateWithMounts , MSDBServerReadWithMounts, MSDBSmountsRead, MSDBServersRead , MSDBServerUpdateWithMounts, ProvisionData, ExecJobBase
from .jira import JiraTicketDetails, JiraClient
import base64, httpx, json
from src.errors import JiraAlreadyExists, JobAlreadyExits , JiraTicketStatusChange
from .utils import create_job_remote, get_job_status_remote

class DbopsService:
    async def update_job(self, session : AsyncSession):
        pass

    async def create_job(self, session : AsyncSession):
        pass

    async def log_event(self, session : AsyncSession):
        pass

    async def create_jira_meta(self,data: JiraMetaCreate,  session : AsyncSession):
        is_unique = await self.get_jira_meta_by_name(jira_meta_name=data.jira_meta_name, session=session)
        if is_unique:
            return None
        else:
            jira_meta_dict = data.model_dump()
            new_meta = JiraMeta(**jira_meta_dict)
            session.add(new_meta)
            await session.commit()
            return new_meta  

    async def update_jira_meta(self, jira_id : str, update_data : JiraMetaCreate,  session : AsyncSession):
        jirameta_to_update = await self.get_jira_meta_by_jira_id(jira_id=jira_id, session = session)
        if jirameta_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(jirameta_to_update, k, v)
            await session.commit()
            return jirameta_to_update
        else:
            return None

    async def get_jira_meta_by_name(self, jira_meta_name: str,  session : AsyncSession):
        statement = select(JiraMeta).where(JiraMeta.jira_meta_name == jira_meta_name)
        results = await session.exec(statement)
        jira_meta = results.first()
        return jira_meta

    async def get_jira_meta_by_jira_id(self, jira_id: str,  session : AsyncSession):
        statement = select(JiraMeta).where(JiraMeta.jira_id == jira_id)
        results = await session.exec(statement)
        jira_meta = results.first()
        return jira_meta

    async def get_jira_meta(self,  jira_dbdash_uid: str,  session : AsyncSession, jira_id : Optional[str] = None):
        statement = select(JiraMeta).where(JiraMeta.jira_dbdash_uid == jira_dbdash_uid)
        if jira_id:
            statement = statement.where(JiraMeta.jira_id == jira_id)
        results = await session.exec(statement)
        jira_meta = results.all()
        return jira_meta

    async def delete_jira_meta(self, jira_id: str, session: AsyncSession):
        jira_data = await self.get_jira_meta_by_jira_id(jira_id, session)
        if jira_data is not None:
            await session.delete(jira_data)
            await session.commit()
            return {}
        else:
            return None
    
    async def create_mssql_server(self, data: MSDBServerCreateWithMounts, session : AsyncSession):
        is_unique = await self.get_mssql_server_by_name(msdbs_name=data.server.msdbs_name, session=session)
        if is_unique:
            return None
        else:
            payload = data.model_dump()
            new_server = MSDBServers(**payload["server"])
            session.add(new_server)
            await session.flush()
            mounts_to_add = [
                MSDBSmounts(**mount, msdbms_mds_id=new_server.msdbs_id)
                for mount in payload.get("mounts", [])
            ]
            for mount_obj in mounts_to_add:
                session.add(mount_obj)

            await session.commit()  

            return {
                "server": new_server,
                "mounts": mounts_to_add
            }

    async def get_mssql_server_by_name(self, msdbs_name:str, session: AsyncSession):
        statement = select(MSDBServers).where(MSDBServers.msdbs_name == msdbs_name)
        results = await session.exec(statement)
        msdbs_name = results.first()
        return msdbs_name

    async def get_mssql_server_by_id(self, msdbs_id:str, session: AsyncSession):
        statement = select(MSDBServers).where(MSDBServers.msdbs_id == msdbs_id)
        results = await session.exec(statement)
        msdbs_name = results.first()
        return msdbs_name

    async def get_mssql_server_mounts_by_id(self, msdbsm_id:str, session: AsyncSession):
        statement = select(MSDBSmounts).where(MSDBSmounts.msdbsm_id == msdbsm_id)
        results = await session.exec(statement)
        msdbs_name = results.first()
        return msdbs_name

    async def get_msserver(self, session : AsyncSession):
        statement = select(MSDBServers)
        results = await session.exec(statement)
        msserver = results.all()
        return msserver

    async def get_msserver_mounts_all(self, session: AsyncSession):
        result = await session.execute(
            select(MSDBServers, MSDBSmounts)
            .outerjoin( 
                MSDBSmounts,
                MSDBSmounts.msdbms_mds_id == MSDBServers.msdbs_id
            )
            .order_by(MSDBServers.msdbs_id)
        )

        rows = result.all()

        server_mounts_map: dict[str, list[MSDBSmounts]] = defaultdict(list)
        servers: dict[str, MSDBServers] = {}

        for server, mount in rows:
            servers[server.msdbs_id] = server
            if mount:
                server_mounts_map[server.msdbs_id].append(mount)

        return [
            MSDBServerReadWithMounts(
                server=MSDBServersRead.model_validate(server),
                mounts=[
                    MSDBSmountsRead.model_validate(m)
                    for m in server_mounts_map[server.msdbs_id]
                ]
            )
            for server in servers.values()
        ]
        
    async def get_msserver_mounts(self, msdbs_id: str, session: AsyncSession) -> MSDBServerReadWithMounts | None:

        result = await session.execute(
            select(MSDBServers).where(MSDBServers.msdbs_id == msdbs_id)
        )
        server_obj = result.scalar_one_or_none()
        if not server_obj:
            return None

        result = await session.execute(
            select(MSDBSmounts).where(MSDBSmounts.msdbms_mds_id == server_obj.msdbs_id)
        )
        mounts_objs = result.scalars().all()

        server_pydantic = MSDBServersRead.model_validate(server_obj)
        mounts_pydantic = [
            MSDBSmountsRead.model_validate(m) for m in mounts_objs
        ]

        #server_pydantic = MSDBServersRead.from_orm(server_obj)
        #mounts_pydantic = [MSDBSmountsRead.from_orm(m) for m in mounts_objs]
                
        data = MSDBServerReadWithMounts(
            server=server_pydantic,
            mounts=mounts_pydantic
        )
        return data

    async def update_msserver_mounts(self, msdbs_id : str, update_data : MSDBServerUpdateWithMounts,  session : AsyncSession):
        serverstoupdate = await self.get_mssql_server_by_id(msdbs_id=msdbs_id, session = session)
        if serverstoupdate is not None:
            for field, value in update_data.server.model_dump(exclude_unset=True).items():
                setattr(serverstoupdate, field, value)  

            for mount in update_data.mounts:
                mount_obj = await self.get_mssql_server_mounts_by_id(mount.msdbsm_id, session)
                if not mount_obj:
                    new_mount = MSDBSmounts(
                        msdbms_mds_id=msdbs_id,
                        msdbsm_path=mount.msdbsm_path,
                        msdbsm_usage=mount.msdbsm_usage,
                    )
                    session.add(new_mount)
                else:
                    for field, value in mount.model_dump(exclude_unset=True).items():
                        if field != "msdbsm_id":
                            setattr(mount_obj, field, value)
      
            await session.commit()
            data = await self.get_msserver_mounts(msdbs_id, session)
            print(data)
            return data
        else:
            return None

    async def delete_msserver(self, msdbs_id: str, session: AsyncSession):
        msserver = await self.get_mssql_server_by_id(msdbs_id, session)
        if msserver is not None:
            await session.execute(
                delete(MSDBSmounts).where(
                    MSDBSmounts.msdbms_mds_id == msdbs_id
                )
            )
            await session.execute(
                delete(MSDBServers).where(
                    MSDBServers.msdbs_id == msdbs_id
                )
            )
            await session.commit()
            return {}
        else:
            return None

    async def delete_msserver_mpoint(self, msdbsm_id: str, session: AsyncSession):
        msserver = await self.get_mssql_server_mounts_by_id(msdbsm_id, session)
        print(msserver)
        if msserver is not None:
            await session.execute(
                delete(MSDBSmounts).where(
                    MSDBSmounts.msdbsm_id == msdbsm_id
                )
            )
            await session.commit()
            return {}
        else:
            return None
            
    async def get_jira_ticket_details(self, jira_id : str, jira_ticket : str, session: AsyncSession) -> JiraTicketDetails:
        jira_meta=await self.get_jira_meta_by_jira_id(jira_id, session)
        auth = base64.b64encode(f"{jira_meta.jira_user}:{jira_meta.jira_token}".encode()).decode()
        headers = {
                    "Authorization": f"Basic {auth}",
                    "Accept": "application/json",
                  }
        # need to remove verify later 
        jira_client = JiraClient(http_client=httpx.Client(verify=False),
                                 jira_url=jira_meta.jira_api_url,
                                 headers = headers
                        )
        jira_raw_data = jira_client.get_issue(jira_ticket)
        jira_issue = JiraTicketDetails(jira_raw_data)
        return jira_issue

    async def get_job_local(self, jirat_id:str, job_mode:str, session: AsyncSession):
        statement = select(ExecJob).join(JiraTicket, (JiraTicket.jirat_id==ExecJob.job_jirat_id)).where(JiraTicket.jirat_id == jirat_id, ExecJob.job_status.notin_(["COMPLETED","FAILED"]), ExecJob.job_mode==job_mode)
        results = await session.exec(statement)
        jira = results.first()
        return jira
    
    async def get_job_local_by_job_id(self, job_id:str, session: AsyncSession):
        statement = select(ExecJob).where(ExecJob.job_id == job_id)
        results = await session.exec(statement)
        job = results.first()
        return job

    async def create_job_local(self, data, session):
        localjob = await self.get_job_local(data["job_jirat_id"],data["job_mode"], session)
        if localjob:
            return None
        else:
            #data_dict = data.model_dump()
            data_dump = ExecJob(**data)
            session.add(data_dump)
            await session.commit()
            return data_dump  

    async def get_job_status_local(self, job_id):
        pass

    async def create_jira_ticket_details(self, data: JiraTicketCreate,runmode:str, session: AsyncSession):
        jira = await self.get_jira_ticket_local(data.jirat_ticket,runmode, session)
        if jira:
            return None
        else:
            data_dict = data.model_dump()
            data_dump = JiraTicket(**data_dict)
            session.add(data_dump)
            await session.commit()
            return data_dump  

    async def get_jira_ticket_local(self, jirat_ticket:str,job_mode:str, session: AsyncSession):
        statement = select(ExecJob).join(JiraTicket, (JiraTicket.jirat_id==ExecJob.job_jirat_id)).where(JiraTicket.jirat_ticket==jirat_ticket, ExecJob.job_status.notin_(["COMPLETED","FAILED"]), ExecJob.job_mode==job_mode)
        #statement = select(JiraTicket).where(JiraTicket.jirat_ticket == jirat_ticket, JiraTicket.jirat_status.notin_(["Closed", "Done"]))
        results = await session.exec(statement)
        jira = results.first()
        return jira

    async def update_job_status_local(self,job_id, data: ExecJobBase, session : AsyncSession):
        job2update = await self.get_job_local_by_job_id(job_id, session)
        if job2update is not None:
            #update_data_dict = data.model_dump()
            for k, v in data.items():
                setattr(job2update, k, v)
            await session.commit()
            return job2update
        else:
            return None
        
    async def create_job_log_local(self, data):
        pass

    async def provision_database(self, runmode: str, data : ProvisionData, token_details,  session: AsyncSession):
        try:
            status = data.jira_ticket_details.jirat_status.lower()
            if status in ("open"):
                await self.make_ticket_inprogress(data.jira_ticket_details.jirat_meta_id, data.jira_ticket_details.jirat_ticket,session)
        except Exception as e:
            print(e)
            raise JiraTicketStatusChange
        exec_user=token_details["user"]["email"]
        jiraticket = await self.create_jira_ticket_details(data.jira_ticket_details,runmode, session)
        if not jiraticket:
            raise JiraAlreadyExists
        job_payload = {
            "job_jirat_id": jiraticket.jirat_id,
            "job_parameters": json.dumps(data.model_dump()),
            "job_progress": "0",
            "job_mode" : runmode,
            "job_status": "STARTING",
            "job_current_step": "START",
            "job_current_log": None
        }
        job_local = await self.create_job_local(job_payload, session)
        if not job_local:
            raise JobAlreadyExits
        else:
            job_log_payload = {
                "exec_user" : exec_user,
                "exec_job_id" : job_local.job_id,
                "exec_module" : "create_job_local",
                "exec_action" : runmode,
                "exec_status" : "success",
                "exec_detail" : "Creating Job entries on local repo..",
            }
            await self.log_event(job_log_payload, session)
        remotejob = await create_job_remote(self, data,job_log_payload, session)
        if remotejob["action"] == "submitted":
            return job_log_payload

    async def create_provision_database_job(self, runmode: str, data : ProvisionData, token_details,  session: AsyncSession, bg_tasks):
        status = data.jira_ticket_details.jirat_status.lower()
        if status in ("open", "in progress"):
        #if data.jira_ticket_details.jirat_status == "Open":
            job_log_payload = await self.provision_database(runmode, data, token_details, session) 
            #async def get_job_status_remote(dbopsserv, data,job_log_payload, session):
            bg_tasks.add_task(get_job_status_remote,dbopsserv=self, data=data,job_log_payload=job_log_payload, session=session ) 
            return job_log_payload
        else:
            raise JiraTicketStatusChange
    
    async def log_event(self,data, session : AsyncSession):
        data_dump = ExecLog(**data)
        session.add(data_dump)
        await session.commit()
        return data_dump 

    async def get_all_local_jobs(self, session: AsyncSession):

        statement = ( select(
                ExecJob.job_id,
                ExecJob.job_mode,
                ExecJob.job_parameters,
                ExecJob.job_status,
                ExecJob.job_current_step,
                ExecJob.job_updated_at,
                JiraTicket.jirat_ticket,
                JiraMeta.jira_user,
            )
            .join(JiraTicket, ExecJob.job_jirat_id == JiraTicket.jirat_id)
            .join(JiraMeta, JiraTicket.jirat_meta_id == JiraMeta.jira_id)
            .order_by(desc(ExecJob.job_updated_at))
        )
        #statement = select(ExecJob).order_by(desc(ExecJob.job_updated_at))
        results = await session.exec(statement)
        jobs = results.all()
        return jobs

    async def get_all_local_job_by_id(self, job_id, session: AsyncSession):

        statement = ( select(
                ExecJob.job_id,
                ExecJob.job_mode,
                ExecJob.job_parameters,
                ExecJob.job_status,
                ExecJob.job_current_step,
                ExecJob.job_updated_at,
                JiraTicket.jirat_ticket,
                JiraMeta.jira_user,
            )
            .join(JiraTicket, ExecJob.job_jirat_id == JiraTicket.jirat_id)
            .join(JiraMeta, JiraTicket.jirat_meta_id == JiraMeta.jira_id)
            .where(ExecJob.job_id == job_id)
            .order_by(desc(ExecJob.job_updated_at))
        )
        #statement = select(ExecJob).order_by(desc(ExecJob.job_updated_at))
        results = await session.exec(statement)
        job = results.first()
        return job


    async def get_local_job_logs_by_id(self, job_id,starttime, session: AsyncSession):
        statement = ( select (
                ExecLog.exec_module,
                ExecLog.exec_action,
                ExecLog.exec_status,
                ExecLog.exec_detail,
                ExecLog.exec_datetime,
                ExecJob.job_status
            )
            .join(ExecLog, ExecJob.job_id == ExecLog.exec_job_id)
            .where(ExecLog.exec_job_id == job_id)
        )
        if starttime:
            statement = statement.where(ExecLog.exec_datetime > starttime) 
        statement = statement.order_by(desc(ExecLog.exec_datetime))
        results = await session.exec(statement)
        logs = results.all()
        return logs


    async def add_comment_to_jira(self, jira_id: str, jira_ticket: str, comment: str, session: AsyncSession):
        jira_meta = await self.get_jira_meta_by_jira_id(jira_id, session)
        auth = base64.b64encode(f"{jira_meta.jira_user}:{jira_meta.jira_token}".encode()).decode()

        headers = {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        jira_client = JiraClient(
            http_client=httpx.Client(verify=False),
            jira_url=jira_meta.jira_api_url,
            headers=headers
        )

        response = jira_client.add_comment(jira_ticket, comment)

        return response


    async def close_jira_ticket(self, jirat_meta_id: str, jira_ticket: str, transition_id: str, session: AsyncSession):
        jira_meta = await self.get_jira_meta_by_jira_id(jirat_meta_id, session)
        auth = base64.b64encode(f"{jira_meta.jira_user}:{jira_meta.jira_token}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        jira_client = JiraClient(
            http_client=httpx.Client(verify=False),
            jira_url=jira_meta.jira_api_url,
            headers=headers
        )

        response = jira_client.close_ticket(jira_ticket, "Closed By Automation")
        return response
    
    async def make_ticket_inprogress(self, jirat_meta_id: str, jira_ticket: str, session: AsyncSession):
        jira_meta = await self.get_jira_meta_by_jira_id(jirat_meta_id, session)
        auth = base64.b64encode(f"{jira_meta.jira_user}:{jira_meta.jira_token}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        jira_client = JiraClient(
            http_client=httpx.Client(verify=False),
            jira_url=jira_meta.jira_api_url,
            headers=headers
        )

        response = jira_client.move_to_inprogress(jira_ticket, "In progress - by db automation")
        return response

    async def get_jira_transitions(self, jira_id: str, jira_ticket: str, session: AsyncSession):
        jira_meta = await self.get_jira_meta_by_jira_id(jira_id, session)
        auth = base64.b64encode(f"{jira_meta.jira_user}:{jira_meta.jira_token}".encode()).decode()

        headers = {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "Content-Type": "application/json"            
        }

        jira_client = JiraClient(
            http_client=httpx.Client(verify=False),
            jira_url=jira_meta.jira_api_url,
            headers=headers
        )

        return jira_client.get(f"/issue/{jira_ticket}/transitions")


"""
ExecJobRead
    exec_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    exec_user : str = Field(nullable=True)
    exec_job_id : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )      
    exec_module :str = Field(nullable=True)
    exec_action :str = Field(nullable=True)
    exec_status :str = Field(nullable=True)
    exec_detail :str = Field(nullable=True)
    exec_datetime : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
class ExecJob(SQLModel, table=True):
    __tablename__= "execjob"
    job_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    job_jirat_id : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    job_parameters : str = Field(nullable=False)
    job_progress : str = Field(nullable=True)
    job_status : str = Field(nullable=True)
    job_current_step : str = Field(nullable=True)
    job_current_log : str = Field(nullable=True)
    job_created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    job_updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


auth = base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth}",
    "Accept": "application/json",
}

url = f"{JIRA_URL}/rest/api/3/issue/XWITO-43046"


| Step                | Status         | Progress |
| ------------------- | -------------- | -------- |
| Job created         | PENDING        | 0%       |
| Jira fetch          | VALIDATING     | 10%      |
| Validation success  | VALIDATING     | 20%      |
| MSSQL restore start | PROVISIONING   | 30%      |
| Restore complete    | PROVISIONING   | 70%      |
| Close Jira          | CLOSING_TICKET | 85%      |
| Send email          | SENDING_EMAIL  | 95%      |
| Done                | COMPLETED      | 100%     |
| Done                | FAILED      | 100%     |
"""