from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field
import uuid

"""
class ExecLogBase(BaseModel):
    exec_user_id: uuid.UUID
    exec_module: Optional[str] = None
    exec_action: Optional[str] = None
    exec_status: Optional[str] = None
    exec_detail: Optional[str] = None
    exec_datetime: Optional[datetime] = None

class ExecLogCreate(ExecLogBase):
    pass

class ExecLogRead(ExecLogBase):
    exec_id: uuid.UUID
    model_config = {
        "from_attributes": True
    }
"""
class ExecLogBase(BaseModel):
    exec_user: Optional[str] = None
    exec_job_id : uuid.UUID
    exec_module: Optional[str] = None
    exec_action: Optional[str] = None
    exec_status: Optional[str] = None
    exec_detail: Optional[str] = None
    exec_datetime: Optional[datetime] = None

class ExecLogCreate(ExecLogBase):
    pass

class ExecLogRead(ExecLogBase):
    exec_id: uuid.UUID
    model_config = {
        "from_attributes": True
    }

class ExecJobLogBase(BaseModel):
    exec_module: Optional[str] = None
    exec_action: Optional[str] = None
    exec_status: Optional[str] = None
    exec_detail: Optional[str] = None
    job_status: Optional[str] = None
    exec_datetime: Optional[datetime] = None  

class JiraMetaBase(BaseModel):
    jira_api_url: Optional[str] = None
    jira_dbdash_uid: uuid.UUID
    jira_meta_name : str
    jira_user: Optional[str] = None
    jira_token: Optional[str] = None
    jirameta_created_at: Optional[datetime] = None

class JiraMetaCreate(JiraMetaBase):
    pass

class JiraMetaRead(JiraMetaBase):
    jira_id: uuid.UUID
    model_config = {
        "from_attributes": True
    }

class JiraTicketBase(BaseModel):
    jirat_meta_id: str
    jirat_ticket: Optional[str] = None
    jirat_summary: Optional[str] = None
    jirat_status: Optional[str] = None
    jirat_created: Optional[str] = None
    jirat_issue_type: Optional[str] = None
    jirat_assignee: Optional[str] = None
    jirat_num_sites: Optional[str] = None
    jirat_desktop_licenses: Optional[str] = None
    jirat_mobile_licenses: Optional[str] = None
    jirat_db_name: Optional[str] = None
    jirat_src_app_type: Optional[str] = None
    jirat_company_name: Optional[str] = None
    jirat_company_address: Optional[str] = None
    jirat_reporter: Optional[str] = None

class JiraTicketCreate(JiraTicketBase):
    pass

class JiraTicketRead(JiraTicketBase):
    jirat_id: uuid.UUID
    model_config = {
        "from_attributes": True
    }

class JiraTicketUpdate(BaseModel):
    jirat_ticket: Optional[str] = None
    jirat_summary: Optional[str] = None
    jirat_status: Optional[str] = None
    jirat_issue_type: Optional[str] = None
    jirat_assignee: Optional[str] = None
    jirat_num_sites: Optional[str] = None
    jirat_desktop_licenses: Optional[str] = None
    jirat_mobile_licenses: Optional[str] = None
    jirat_db_name: Optional[str] = None
    jirat_src_app_type: Optional[str] = None
    jirat_company_name: Optional[str] = None
    jirat_company_address: Optional[str] = None
    jirat_reporter: Optional[str] = None

class ExecJobBase(BaseModel):
    job_jirat_id: Optional[uuid.UUID] = None
    job_mode: Optional[str] = None
    job_parameters: Optional[str] = None
    job_progress: Optional[str] = None
    job_status: Optional[str] = None
    job_current_step: Optional[str] = None
    job_current_log: Optional[str] = None
    job_created_at: Optional[datetime] = None
    job_updated_at: Optional[datetime] = None


class ExecJobResponse(BaseModel):
    job_id: Optional[uuid.UUID] = None
    job_mode: Optional[str] = None
    job_parameters: Optional[str]
    job_status: Optional[str] = None
    job_current_step: Optional[str] = None
    job_updated_at: Optional[datetime] = None
    jirat_ticket: Optional[str] = None
    jira_user: Optional[str] = None

"""
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
    job_mode: str = Field(nullable=False)
    job_parameters : str = Field(nullable=False)
    job_progress : str = Field(nullable=True)
    job_status : str = Field(nullable=True)
    job_current_step : str = Field(nullable=True)
    job_current_log : str = Field(nullable=True)
    job_created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    job_updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
"""

class ExecJobCreate(ExecJobBase):
    pass


class ExecJobRead(ExecJobBase):
    job_id: uuid.UUID
    model_config = {
        "from_attributes": True
    }

class MSDBServersBase(BaseModel):
    msdbs_user: Optional[str] = None
    msdbs_host: Optional[str] = None
    msdbs_port: Optional[str] = None
    msdbs_name: Optional[str] = None
    msdbs_password : Optional[str] = None
    msdbs_database: Optional[str] = None
    msdbs_status: Optional[str] = None

class MSDBServersCreate(MSDBServersBase):
    pass

class MSDBServersRead(MSDBServersBase):
    msdbs_id: uuid.UUID
    msdbs_created_at: datetime
    msdbs_updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class MSDBSmountsBase(BaseModel):
    msdbsm_path: Optional[str] = None
    msdbsm_usage: Optional[str] = None

class MSDBSmountsCreate(MSDBSmountsBase):
    pass

class MSDBSmountsRead(MSDBSmountsBase):
    msdbsm_id: uuid.UUID
    msdbms_mds_id : uuid.UUID
    msdbsm_updated_at : Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class MSDBSmountsReadNested(MSDBSmountsRead):
    pass

class MSDBServersReadNested(MSDBServersRead):
    mounts: List[MSDBSmountsReadNested] = []

    model_config = {
        "from_attributes": True
    }

class MSDBServerCreateWithMounts(BaseModel):
    server: MSDBServersCreate
    mounts: list[MSDBSmountsCreate] = []
    model_config = {
        "from_attributes": True
    }

class MSDBServerReadWithMounts(BaseModel):
    server: MSDBServersRead
    mounts: list[MSDBSmountsRead]

    model_config = {
        "from_attributes": True
    }


class MSDBSmountsUpdate(BaseModel):
    msdbsm_id: uuid.UUID | None = None               
    msdbsm_path: str | None = None
    msdbsm_usage: str | None = None
    msdbsm_updated_at: datetime | None = None


class MSDBServerUpdateWithMounts(BaseModel):
    server: MSDBServersCreate
    mounts: list[MSDBSmountsUpdate]

class JiraTicketDetailBase(BaseModel):
    jirat_ticket: Optional[str] = None
    jirat_summary: Optional[str] = None
    jirat_status: Optional[str] = None
    jirat_issue_type: Optional[str] = None
    jirat_created: Optional[str] = None
    jirat_assignee: Optional[str] = None
    jirat_num_sites: Optional[str] = None
    jirat_desktop_licenses: Optional[str] = None
    jirat_mobile_licenses: Optional[str] = None
    jirat_db_name: Optional[str] = None
    jirat_src_app_type: Optional[str] = None
    jirat_company_name: Optional[str] = None
    jirat_company_address: Optional[str] = None
    jirat_reporter: Optional[str] = None

class JiraMetaD(BaseModel):
    jira_ticket: str
    jira_id: str

class MountDirD(BaseModel):
    datadir: str
    log_dir: str

class ServerD(BaseModel):
    mounts : MountDirD
    server : str

class ProvisionData(BaseModel):
    jira_ticket_details : JiraTicketCreate
    server_data : ServerD

"""
class ProvisionData(BaseModel):
    jira_meta : JiraMetaD
    jira_ticket_details : JiraTicketDetailBase
    server_data : ServerD

jira_meta
: 
{jira_ticket: 'XWITO-43475', jira_id: 'ebb79583-a2d7-4611-90bb-32958400775b'}
jira_ticket_details
: 
{jirat_ticket: 'XWITO-43475', jirat_summary: 'Provision Database - RestoPros of Lexington (USE RESTOPROSMASTERDB)', jirat_status: 'Done', jirat_issue_type: 'Database Provision', jirat_assignee: 'Romero Morilla, Daniel', …}
server_data
: 
{server: '576cdbf4-f771-4d29-9bd0-ccd391ea2319', mounts: {…}}
[[Prototype]]
: 
Object
"""