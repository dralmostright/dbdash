from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field
import uuid

class AwsAccountBase(BaseModel):
    account_number: str
    account_alias: Optional[str] = None
    account_org: Optional[str] = None
    account_az: Optional[str] = None
    account_status: bool = False
    description: Optional[str] = None

class AwsAccountCreate(AwsAccountBase):
    pass

class AwsAccountRead(AwsAccountBase):
    aid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True
    }

class AwsAccountReadWithRelations(AwsAccountRead):
    rds_aws_maps: List["RdsAWSMapRead"] = []

class RdsAWSMapBase(BaseModel):
    aws_aid: uuid.UUID
    last_collection_at: int

class RdsAWSMapCreate(RdsAWSMapBase):
    pass

class RdsAWSMapRead(RdsAWSMapBase):
    raid: uuid.UUID

class RdsAWSMapReadWithRelations(RdsAWSMapRead):
    rdsinstances: List["RdsInstanceRead"] = []

class RdsInstanceBase(BaseModel):
    rds_aws_id: uuid.UUID
    rds_identifier: Optional[str] = None
    rds_instanceclass: Optional[str] = None
    rds_engine: Optional[str] = None
    rds_inststatus: Optional[str] = None
    rds_instcreatetime: Optional[datetime] = None
    rds_allocstorage: Optional[str] = None
    rds_paramgroup: Optional[str] = None
    rds_az: Optional[str] = None
    rds_enginever: Optional[str] = None
    rds_lisencemodel: Optional[str] = None
    rds_copytagsnapshot: Optional[str] = None
    rds_storagetype: Optional[str] = None
    rds_multiaz: Optional[str] = None
    rds_storageencrypted: Optional[str] = None
    rds_deleteprotection: Optional[str] = None
    rds_clusteridentifier: Optional[str] = None
    rds_masteruser: Optional[str] = None
    rds_dbinstrole: Optional[str] = None
    rds_clusterendpoint: Optional[str] = None
    rds_endpoint: Optional[str] = None
    rds_port: Optional[str] = None
    rds_vpc: Optional[str] = None
    rds_secgroup: Optional[str] = None
    rds_subnetgrp: Optional[str] = None
    rds_subnets: Optional[str] = None
    rds_backupretention: Optional[str] = None
    rds_taglist:  Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }

class RdsInstanceBaseSeed(BaseModel):
    rds_aws_id: uuid.UUID
    rds_identifier: Optional[str] = None
    rds_instanceclass: Optional[str] = None
    rds_engine: Optional[str] = None
    rds_inststatus: Optional[str] = None
    rds_instcreatetime: Optional[datetime] = None
    rds_allocstorage: Optional[str] = None
    rds_paramgroup: Optional[str] = None
    rds_az: Optional[str] = None
    rds_enginever: Optional[str] = None
    rds_lisencemodel: Optional[str] = None
    rds_copytagsnapshot: Optional[str] = None
    rds_storagetype: Optional[str] = None
    rds_multiaz: Optional[str] = None
    rds_storageencrypted: Optional[str] = None
    rds_deleteprotection: Optional[str] = None
    rds_clusteridentifier: Optional[str] = None
    rds_masteruser: Optional[str] = None
    rds_dbinstrole: Optional[str] = None
    rds_clusterendpoint: Optional[str] = None
    rds_endpoint: Optional[str] = None
    rds_port: Optional[str] = None
    rds_vpc: Optional[str] = None
    rds_secgroup: Optional[str] = None
    rds_subnetgrp: Optional[str] = None
    rds_subnets: Optional[str] = None
    rds_backupretention: Optional[str] = None
    rds_taglist:  Optional[str] = None
    created_at:  Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }

class RdsInstanceRead(RdsInstanceBase):
    riid: uuid.UUID
    created_at:  Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }

class RdsInstAwsAcctRead_DDDDDD(RdsInstanceBase):
    awsaccounts: List["AwsAccountBase"] = []
    
class RdsInstAwsAcctRead(AwsAccountRead, RdsInstanceRead):
    model_config = {
        "from_attributes": True
    }

class RdsInstAwsAcctFilterRead(BaseModel):
    aid: uuid.UUID
    account_alias: str
    riid: uuid.UUID
    rds_identifier:str
    rds_engine:str
    rds_instcreatetime:datetime
    rds_enginever: str
    model_config = {
        "from_attributes": True
    }

class RdsEolMinorFilterRead(RdsInstAwsAcctFilterRead):
    mi_row_created_at : datetime
    rds_mi_seol : str
    days_until_eol : str

class RdsEolLastRefreshDate(BaseModel):
    rds_engine_type : str
    latest_refreshed_at : datetime

class RdsEOLMinorFilterReadAWS(BaseModel):
    minor_refresh_date : List[RdsEolLastRefreshDate]
    minor_eol_data : List[RdsEolMinorFilterRead]

"""
class RdsEngineMajor(BaseModel):
    rds_ma_type :Optional[str] = None 
    rds_ma_ver :Optional[str] = None 
    rds_ma_cm_release_date :Optional[str] = None 
    rds_ma_release_date :Optional[str] = None 
    rds_ma_cm_eol :Optional[str] = None 
    rds_ma_rds_seol :Optional[str] = None 
    rds_ma_ex_eol :Optional[str] = None 
    rds_ma_1y_ex_eol :Optional[str] = None 
    rds_ma_3y_ex_eol :Optional[str] = None 
    rds_ma_lts :Optional[str] = None 
    ma_row_created_at :Optional[datetime] = None
"""

class RdsEolMajorFilterRead(RdsInstAwsAcctFilterRead):
    ma_row_created_at : datetime
    rds_ma_rds_seol : str
    days_until_eol : str

class RdsEolMajorLastRefreshDate(BaseModel):
    rds_engine_type : str
    latest_refreshed_at : datetime

class RdsEOLMajorFilterReadAWS(BaseModel):
    major_refresh_date : List[RdsEolLastRefreshDate]
    major_eol_data : List[RdsEolMajorFilterRead]

class RdsHWEc2(BaseModel):
    rds_hw_model: str
    ec2_hw_type: Optional[str] = None
    rds_hw_vcpu: Optional[str] = None
    rds_hw_core: Optional[str] = None
    rds_hw_mem: Optional[str] = None
    rds_hw_storage: Optional[str] = None
    rds_hw_net_gbps: Optional[str] = None
    ec2_hw_basebandwm :Optional[str] = None 
    ec2_hw_maxbandwm :Optional[str] = None 
    ec2_hw_basethroputm :Optional[str] = None 
    ec2_hw_maxthroputm :Optional[str] = None 
    ec2_hw_baseiopsm :Optional[str] = None 
    ec2_hw_maxiopswm :Optional[str] = None 
    model_config = {
        "from_attributes": True
    }
    

class RdsHWEc2Read(BaseModel):
    rds_hw_details: Optional[RdsHWEc2] = None
#class RdsInstAwsAcctRead(RdsInstanceRead):
#    aws_accounts: AwsAccountRead
#    #rds_inst: list[RdsInstanceRead]
#    model_config = {
#        "from_attributes": True
#    }

class RdsInstanceTotalCount(BaseModel):
    total_instances: int

class RdsEngineCount(BaseModel):
    rds_engine: str
    rds_count: int

class RdsAzAccountCount(BaseModel):
    rds_az : str
    rds_count: int

class AccountAZCount(BaseModel):
    account_alias: str
    data : List[RdsAzAccountCount]

class RdsEngineAccountCount(BaseModel):
    #account_alias : str
    rds_engine: str
    rds_enginever: str
    rds_count: int
    
class RdsRecentActivity(BaseModel):
    #account_alias : str
    rds_identifier: str
    account_alias: str
    event_type: str
    event_time: datetime
    last_seen: datetime


class RdsCountPerDay(BaseModel):
    date: str
    rds_count: int

class AccountRdsCountData(BaseModel):
    account_alias: str
    data: List[RdsCountPerDay]

class RdsInstanceCreate(RdsInstanceBase):
    model_config = {
        "from_attributes": True
    }

class RdsSecRules(BaseModel):
    sec_group_name :str 
    sec_gpid  :str 
    sec_riid  : uuid.UUID
    #sec_rule_name  :str 
    sec_rule_type  :str 
    sec_port_range  :str 
    sec_ip_ranges  :str 
    model_config = {
        "from_attributes": True
    }   
class RdsSecRulesCreate(RdsSecRules):
    model_config = {
        "from_attributes": True
    } 

class RdsSecRulesRead(RdsSecRules):
    sec_id: uuid.UUID
    sec_row_created_at: Optional[datetime] = None
    sec_row_updated_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }
    

class RdsInstParams(BaseModel):
    param_type :str 
    param_groupname  :str 
    param_name  : str
    param_value  :str 
    param_riid  : uuid.UUID 
    model_config = {
        "from_attributes": True
    }   

class RdsInstParamsRead(RdsInstParams):
    param_id: uuid.UUID
    param_row_created_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }
    
class RdsEngineMajor(BaseModel):
    rds_ma_type :Optional[str] = None 
    rds_ma_ver :Optional[str] = None 
    rds_ma_cm_release_date :Optional[str] = None 
    rds_ma_release_date :Optional[str] = None 
    rds_ma_cm_eol :Optional[str] = None 
    rds_ma_rds_seol :Optional[str] = None 
    rds_ma_ex_eol :Optional[str] = None 
    rds_ma_1y_ex_eol :Optional[str] = None 
    rds_ma_3y_ex_eol :Optional[str] = None 
    rds_ma_lts :Optional[str] = None 
    ma_row_created_at :Optional[datetime] = None
    
class RdsEngineMinor(BaseModel): 
    rds_mi_type :Optional[str] = None 
    rds_mi_ma_ver :Optional[str] = None 
    rds_mi_ver :Optional[str] = None 
    rds_mi_cr_date :Optional[str] = None 
    rds_mi_release_date :Optional[str] = None 
    rds_mi_seol :Optional[str] = None 
    rds_mi_lts :Optional[str] = None 
    mi_row_created_at :Optional[datetime] = None    
    
class RdsHWDetail(BaseModel):
    rds_hw_model  :Optional[str] = None
    rds_hw_type :Optional[str] = None
    rds_hw_vcpu :Optional[str] = None
    rds_hw_core :Optional[str] = None
    rds_hw_mem :Optional[str] = None
    rds_hw_storage :Optional[str] = None
    rds_hw_ebs_mbps :Optional[str] = None
    rds_hw_ebs_gbps :Optional[str] = None  
    rds_hw_net_gbps :Optional[str] = None
    url_raw: Optional[str] = None
    
class Ec2HWDetail(BaseModel):
    ec2_hw_model :Optional[str] = None
    ec2_hw_type :Optional[str] = None
    ec2_hw_basebandwm :Optional[str] = None
    ec2_hw_maxbandwm :Optional[str] = None
    ec2_hw_basethroputm :Optional[str] = None
    ec2_hw_maxthroputm :Optional[str] = None
    ec2_hw_baseiopsm :Optional[str] = None
    ec2_hw_maxiopswm :Optional[str] = None
    url_raw: Optional[str] = None
    
class RdsAWSMappingCreate(BaseModel):
    created_at: Optional[datetime] = None
    aws_aid: uuid.UUID
    rds_riid: uuid.UUID 
    map_rds_identifier : str
    map_rds_az : str
    last_collection_at: Optional[int] = None
    
class RdsAWSMappingRead(RdsAWSMappingCreate):
    raid: uuid.UUID
    
    
class RdsInstParamsCreate(BaseModel):
    param_type :str 
    param_groupname :str 
    param_name :str 
    param_value :str 
    param_riid: uuid.UUID  
    param_row_created_at: datetime

class RdsInstParamsRead(RdsInstParamsCreate):
    param_id : uuid.UUID 


class RdsSnapShotsBase(BaseModel):  
    snap_aws_id : str 
    snap_identifier :Optional[str] = None
    snap_rds_identifier :Optional[str] = None
    snap_type :Optional[str] = None
    snap_inst_type :Optional[str] = None
    snap_status :Optional[str] = None
    snap_created_time :Optional[datetime] = None
    snap_engine :Optional[str] = None
    snap_allocated_storage :Optional[str] = None
    snap_az :Optional[str] = None
    snap_region :Optional[str] = None
    snap_engine_ver :Optional[str] = None
    snap_progress :Optional[str] = None
    snap_ipos :Optional[str] = None
    snap_throughtput :Optional[str] = None
    snap_taglist :Optional[str] = None
    snap_arn   :Optional[str] = None
    snap_srcregion :Optional[str] = None
    snap_srcidentifier :Optional[str] = None
    snap_row_created_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }
    
class RdsSnapShotsRead(RdsSnapShotsBase):
    snap_id : uuid.UUID 
    
    model_config = {
        "from_attributes": True
    }
    
class RdsSnapShotsReadList(RdsSnapShotsRead):
    rdssnapshots : List[RdsSnapShotsRead]
    model_config = {
        "from_attributes": True
    }
    
class SnapAwsRdsMapBase(BaseModel):
    sar_created_at: Optional[datetime] = None
    sar_snap_id: uuid.UUID
    sar_aws_aid: uuid.UUID 
    sar_snap_identifier : str
    sar_rds_az : str
    sar_last_collection_at: Optional[datetime] = None
    
class SnapAwsRdsMapRead(SnapAwsRdsMapBase):
    sar_id: uuid.UUID
    