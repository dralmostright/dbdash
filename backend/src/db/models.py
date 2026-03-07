from sqlmodel import SQLModel, Field, Column, Relationship, BigInteger, ForeignKey
import sqlalchemy.dialects.postgresql as pg 
from sqlalchemy import Boolean
from datetime import datetime, date
import uuid
from typing import Optional, List

"""
_summary_ 
DB model for storing user information

Returns:
    _type_: _description_
"""
class User(SQLModel, table=True):
    __tablename__= 'apiusers'
    uid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    display_pic:str = Field(sa_column=Column(pg.VARCHAR, server_default="/img/profile-imp.jpg"))
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False,server_default="user" ))
    is_verified: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            default=False,          
            server_default="false"  
        )
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now)) 
    
    def __repr__(self):
        return f"<User {self.email}>"

"""
_summary_
DB model for storing aws account information

"""
class AwsAccount(SQLModel, table=True):
    __tablename__ = "awsaccounts"

    aid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    account_number: str = Field(
        max_length=50, 
        nullable=False,
        unique=True
    )
    account_alias:str = Field(max_length=100, nullable=False)
    account_org: str
    account_az: str 
    account_status: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))     
    description: Optional[str] = Field(default=None)
    """
    rds_aws_maps: List["RdsAWSMap"] = Relationship(
        back_populates="aws_accounts",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    rds_inst_list: List["RdsInstance"] = Relationship(
        back_populates="aws_accounts",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )  
    """


class RdsInstance(SQLModel, table=True):
    __tablename__ = "rdsinstances"

    riid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )

    rds_aws_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    rds_identifier:str = Field(nullable=True)
    rds_instanceclass:str = Field(nullable=True)
    rds_engine:str = Field(nullable=True)
    rds_inststatus:str = Field(nullable=True)
    rds_instcreatetime:datetime = Field(nullable=True)
    rds_allocstorage: str = Field(nullable=True)
    rds_paramgroup: str = Field(nullable=True)
    rds_az:str = Field(nullable=True)
    rds_enginever: str = Field(nullable=True)
    rds_lisencemodel: str = Field(nullable=True)
    rds_copytagsnapshot:str = Field(nullable=True)
    rds_storagetype:str = Field(nullable=True)
    rds_multiaz: str = Field(nullable=True)
    rds_storageencrypted: str = Field(nullable=True)
    rds_deleteprotection: str = Field(nullable=True)
    rds_clusteridentifier: str = Field(nullable=True)
    rds_masteruser: str = Field(nullable=True)
    rds_dbinstrole: str = Field(nullable=True)
    rds_clusterendpoint: str = Field(nullable=True)
    rds_endpoint: str = Field(nullable=True)
    rds_port: str = Field(nullable=True)
    rds_vpc: str = Field(nullable=True)
    rds_secgroup: str = Field(nullable=True)
    rds_subnetgrp: str = Field(nullable=True)
    rds_subnets: str = Field(nullable=True)
    rds_backupretention : str = Field(nullable=True)
    rds_taglist: str
    rds_datacollectiondate: int =  Field(
        sa_column=Column(BigInteger, nullable=True)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    """
    aws_accounts: AwsAccount = Relationship(back_populates="rds_inst_list")
    rds_aws_maps: List["RdsAWSMap"] = Relationship(back_populates="rds_inst_map")    
    """

    
class RdsAWSMap(SQLModel, table=True):
    __tablename__ = "rdsawsmap"

    raid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    aws_aid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("awsaccounts.aid"),
            nullable=False
        )
    )
    rds_riid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )  
    map_rds_identifier:str = Field(nullable=True)  
    map_rds_az:str = Field(nullable=True) 
    """
    rds_riid: uuid.UUID = Field(
        foreign_key="rdsinstances.riid",
        nullable=False    
    )
    """
    last_collection_at: int =  Field(
        sa_column=Column(BigInteger, nullable=True)
    )
    """
    aws_accounts: AwsAccount = Relationship(back_populates="rds_aws_maps")
    rds_inst_map: RdsInstance = Relationship(back_populates="rds_aws_maps")
    """
    
class RdsHWDetail(SQLModel, table=True):
    __tablename__ = "rdshwdetail"
    rds_hw_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    ) 
    rds_hw_model  :str = Field(nullable=True)
    rds_hw_type :str = Field(nullable=True)
    rds_hw_vcpu :str = Field(nullable=True)
    rds_hw_core :str = Field(nullable=True)
    rds_hw_mem :str = Field(nullable=True)
    rds_hw_storage :str = Field(nullable=True)
    rds_hw_ebs_mbps :str = Field(nullable=True)
    rds_hw_ebs_gbps :str = Field(nullable=True)    
    rds_hw_net_gbps :str = Field(nullable=True)
    url_raw: Optional[str] = None
    
class Ec2HWDetail(SQLModel, table=True):
    
    __tablename__ = "ec2hwdetail"
    ec2_hw_type_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    ec2_hw_model :str = Field(nullable=True)
    ec2_hw_type :str = Field(nullable=True)
    ec2_hw_basebandwm :str = Field(nullable=True)
    ec2_hw_maxbandwm :str = Field(nullable=True)
    ec2_hw_basethroputm :str = Field(nullable=True)
    ec2_hw_maxthroputm :str = Field(nullable=True)
    ec2_hw_baseiopsm :str = Field(nullable=True)
    ec2_hw_maxiopswm :str = Field(nullable=True)
    url_raw: Optional[str] = None
    
class RdsEngineMajor (SQLModel, table = True):
    __tablename__ = "rdsmajoreol"

    rds_ma_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )   
    
    rds_ma_type :str = Field(nullable=True)
    rds_ma_ver :str = Field(nullable=True)
    rds_ma_cm_release_date :str = Field(nullable=True)
    rds_ma_release_date :str = Field(nullable=True)
    rds_ma_cm_eol :str = Field(nullable=True)
    rds_ma_rds_seol :str = Field(nullable=True)
    rds_ma_ex_eol :str = Field(nullable=True)
    rds_ma_1y_ex_eol :str = Field(nullable=True)
    rds_ma_3y_ex_eol :str = Field(nullable=True)
    rds_ma_lts :str = Field(nullable=True)
    ma_row_created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    url_raw: Optional[str] = None

class RdsEngineMinor(SQLModel, table= True):
    
    __tablename__ = "rdsminoreol"
    rds_mi_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )  
    rds_mi_type :str = Field(nullable=True)
    rds_mi_ma_ver :str = Field(nullable=True)
    rds_mi_ver :str = Field(nullable=True)
    rds_mi_cr_date :str = Field(nullable=True)
    rds_mi_release_date :str = Field(nullable=True)
    rds_mi_seol :str = Field(nullable=True)
    rds_mi_lts :str = Field(nullable=True)
    mi_row_created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    url_raw: Optional[str] = None
    
    
class RdsSecRules(SQLModel, table=True):
    __tablename__ = "rdssecrules"
    sec_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )  
    sec_group_name :str = Field(nullable=True)
    sec_gpid  :str = Field(nullable=True)
    sec_riid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )     
    """
    sec_riid  : uuid.UUID = Field(
        foreign_key="rdsinstances.riid",   
        nullable=False
    )    
    """
    #sec_rule_name  :str = Field(nullable=True)
    sec_rule_type  :str = Field(nullable=True)
    sec_port_range  :str = Field(nullable=True)
    sec_ip_ranges  :str = Field(nullable=True)
    sec_row_created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    sec_row_updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))      
    
class RdsInstParams(SQLModel, table=True):
    __tablename__ = "rdsinstparams"
    param_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    ) 
    param_type :str = Field(nullable=True)
    param_groupname :str = Field(nullable=True)
    param_name :str = Field(nullable=True)
    param_value :str = Field(nullable=True)
    param_riid: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    ) 
    """    
    param_riid : uuid.UUID = Field(
        foreign_key="rdsinstances.riid",   
        nullable=False
    )
    """
    param_row_created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
class RdsSnapShots(SQLModel, table=True):
    __tablename__ = "rdssnapshots"
    snap_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )   
    snap_aws_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )      
    snap_identifier :str = Field(nullable=True)
    snap_rds_identifier :str = Field(nullable=True)
    snap_type :str = Field(nullable=True)
    snap_inst_type :str = Field(nullable=True)
    snap_status :str = Field(nullable=True)
    snap_created_time :datetime = Field(nullable=True)
    snap_engine :str = Field(nullable=True)
    snap_allocated_storage :str = Field(nullable=True)
    snap_az :str = Field(nullable=True)
    snap_region :str = Field(nullable=True)
    snap_engine_ver :str = Field(nullable=True)
    snap_progress : str = Field(nullable=True)
    snap_ipos :str = Field(nullable=True)
    snap_throughtput :str = Field(nullable=True)
    snap_taglist :str = Field(nullable=True)
    snap_arn   :str = Field(nullable=True)
    snap_srcregion :str = Field(nullable=True)
    snap_srcidentifier :str = Field(nullable=True)
    snap_row_created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))    
    
class SnapAwsRdsMap(SQLModel, table=True):
    __tablename__ = "snapawsrdsmap"

    sar_id: uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    sar_created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    sar_snap_id : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )  
    sar_aws_aid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    sar_snap_identifier:str = Field(nullable=True)  
    sar_rds_az:str = Field(nullable=True) 
    sar_last_collection_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))   

class ExecLog(SQLModel, table=True):
    __tablename__ = "execlog"
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

class JiraMeta(SQLModel, table=True):
    __tablename__ = "jirameta"
    jira_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    jira_meta_name : str = Field(nullable=False)
    jira_api_url :str = Field(nullable=True)
    jira_dbdash_uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    jira_user : str = Field(nullable=True)
    jira_token : str = Field(nullable=True)
    jirameta_created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

class JiraTicket(SQLModel, table=True):
    __tablename__ = "jiraticket"
    jirat_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    jirat_meta_id : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    jirat_ticket :str = Field(nullable=True)
    jirat_summary : str = Field(nullable=True)
    jirat_status : str = Field(nullable=True)
    jirat_created : str = Field(nullable=True)
    jirat_issue_type : str = Field(nullable=True)
    jirat_assignee : str = Field(nullable=True)
    jirat_num_sites : str = Field(nullable=True)
    jirat_desktop_licenses : str = Field(nullable=True)
    jirat_mobile_licenses : str = Field(nullable=True)
    jirat_db_name : str = Field(nullable=True)
    jirat_src_app_type : str = Field(nullable=True)
    jirat_company_name : str = Field(nullable=True)
    jirat_company_address : str = Field(nullable=True)   
    jirat_reporter : str = Field(nullable=True)       
    jirat_created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

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
    job_mode: str = Field(nullable=False)
    job_parameters : str = Field(nullable=False)
    job_progress : str = Field(nullable=True)
    job_status : str = Field(nullable=True)
    job_current_step : str = Field(nullable=True)
    job_current_log : str = Field(nullable=True)
    job_created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    job_updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    
class MSDBServers(SQLModel, table=True):
    __tablename__="msdbservers"
    msdbs_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )   
    msdbs_user : str = Field(nullable=True)
    msdbs_password : str = Field(nullable=True)
    msdbs_database : str = Field(nullable=True)
    msdbs_host : str = Field(nullable=True)
    msdbs_port : str = Field(nullable=True)
    msdbs_name : str = Field(nullable=True)
    msdbs_status : str = Field(nullable=True)
    msdbs_created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    msdbs_updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))    


class MSDBSmounts(SQLModel, table=True):
    __tablename__="msdbsmounts"
    msdbsm_id : uuid.UUID = Field (
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    msdbms_mds_id : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    msdbsm_path : str = Field(nullable=True)
    msdbsm_usage : str = Field(nullable=True)  
    msdbsm_updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  

"""
PENDING
VALIDATING
PROVISIONING
CLOSING_TICKET
SENDING_EMAIL
COMPLETED
FAILED

CREATE TABLE execlog (
exec_id UUID NOT NULL,
exec_user_id UUID NOT NULL,
exec_module VARCHAR,
exec_action VARCHAR,
exec_status VARCHAR,
exec_detail VARCHAR,
exec_datetime TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (exec_id)
)


2026-01-16 17:07:08,166 INFO sqlalchemy.engine.Engine [no key 0.00007s] ()
2026-01-16 17:07:08,179 INFO sqlalchemy.engine.Engine
CREATE TABLE jirameta (
jira_id UUID NOT NULL,
jira_api_url VARCHAR,
jira_dbdash_uid UUID NOT NULL,
jira_user VARCHAR,
jira_token VARCHAR,
"JiraMeta_created_at" TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (jira_id)
)


2026-01-16 17:07:08,179 INFO sqlalchemy.engine.Engine [no key 0.00009s] ()
2026-01-16 17:07:08,181 INFO sqlalchemy.engine.Engine
CREATE TABLE jiraticket (
jirat_id UUID NOT NULL,
jirat_meta_id UUID NOT NULL,
jira_ticket VARCHAR,
jirat_src_db VARCHAR,
jirat_src_tar VARCHAR,
jirat_src_app_type VARCHAR,
jirat_num_sites VARCHAR,
jirat_desktop_licenses VARCHAR,
jirat_mobile_licenses VARCHAR,
jirat_company_address VARCHAR,
jirat_description VARCHAR,
"Jirat_created_at" TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (jirat_id)
)


2026-01-16 17:07:08,181 INFO sqlalchemy.engine.Engine [no key 0.00006s] ()
2026-01-16 17:07:08,182 INFO sqlalchemy.engine.Engine
CREATE TABLE execjob (
job_id UUID NOT NULL,
job_jirat_id UUID NOT NULL,
job_env_id UUID NOT NULL,
job_progress VARCHAR,
job_status VARCHAR,
job_current_step VARCHAR,
job_current_log VARCHAR,
job_created_at TIMESTAMP WITHOUT TIME ZONE,
job_updated_at TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (job_id)
)

"""