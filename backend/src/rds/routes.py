from fastapi import APIRouter, Depends, status
from typing import Optional, List
from .schemas import AwsAccountBase,RdsInstanceRead, AwsAccountRead, \
    AwsAccountCreate, RdsInstanceTotalCount, AccountRdsCountData, RdsEngineCount ,AccountAZCount, \
        RdsEngineAccountCount, RdsInstAwsAcctRead, RdsInstAwsAcctFilterRead, RdsHWEc2Read, RdsSecRulesRead, \
            RdsInstParamsRead, RdsEngineMajor, RdsEngineMinor, RdsHWDetail ,Ec2HWDetail, RdsRecentActivity, RdsInstanceBase , \
                RdsInstanceBaseSeed, RdsAWSMapCreate, RdsAWSMappingRead, RdsAWSMappingCreate, RdsInstParamsCreate, RdsSecRules, RdsSecRulesCreate, \
                    RdsSnapShotsBase, RdsSnapShotsRead, SnapAwsRdsMapBase, RdsEolMinorFilterRead, RdsEOLMinorFilterReadAWS, RdsEOLMajorFilterReadAWS
from .service import RdsService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.config import Config
from src.errors import AwsAccountAlreadyExists, AwsAccountNotFound,InvalidParameters
from src.auth.dependencies import AccessTokenBearer
from .utils import validate_interval_duration

rds_router = APIRouter()
rds_service = RdsService()
access_token_bearer = AccessTokenBearer()

@rds_router.get("/org/getall", response_model=list[AwsAccountRead])
async def get_all_aws_accounts(session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    all_accounts = await rds_service.get_aws_accounts(session)
    return all_accounts

@rds_router.post('/org/register', response_model=AwsAccountRead, status_code=status.HTTP_201_CREATED)
async def create_org_account(account_data: AwsAccountCreate, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    acn = account_data.account_number
    acn_exists = rds_service.account_exsits(acn,session)
    if await acn_exists:
        raise AwsAccountAlreadyExists()
    new_acn = await rds_service.create_aws_accounts(account_data, session)
    return new_acn

@rds_router.get('/org/account/{aid}', response_model=AwsAccountRead)
async def get_aws_account(aid:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)) -> dict:
    account = await rds_service.get_account_by_aid(aid,session)
    if account:
        return account
    else:
        raise AwsAccountNotFound 

@rds_router.get('/org/byaccount', response_model=AwsAccountRead)
async def get_account_by_account_number(account_number:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)) -> dict:
    account = await rds_service.get_account_by_account_number(account_number,session)
    if account:
        return account
    else:
        raise AwsAccountNotFound 
    
@rds_router.patch('/org/account/{aid}', response_model=AwsAccountRead)
async def update_aws_account(aid: str, aws_acct_up_data:AwsAccountCreate,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)) -> dict:
    update_account = await rds_service.update_aws_account(aid, aws_acct_up_data, session)
    if update_account:
        return update_account
    else:
        raise AwsAccountNotFound 

@rds_router.delete('/org/account/{aid}',status_code= status.HTTP_204_NO_CONTENT)
async def delete_aws_account(aid:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    delete_aws_account = await rds_service.delete_aws_account(aid,session)
    if delete_aws_account is None:
        raise AwsAccountNotFound
    else:
        return {}

@rds_router.get('/rds/total', response_model=RdsInstanceTotalCount)
async def get_rds_total_count(status: Optional[str] = None, 
                              session:AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    rds_total_count = await rds_service.get_total_instances(status,session)
    return RdsInstanceTotalCount(total_instances=rds_total_count)

@rds_router.get('/rds/account/count', response_model=List[AccountRdsCountData])
async def get_rds_total_count(interval: Optional[str] = None, 
                              duration: Optional[str] = None,
                              session:AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    if validate_interval_duration(interval, duration):
        rds_total_counts = await rds_service.get_rds_count_by_account(interval, duration ,session)
        return rds_total_counts
    else:
        raise InvalidParameters
    
@rds_router.get('/rds/engine/count', response_model=List[RdsEngineCount])
async def get_rds_engine_count(
                              session:AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    rds_engine_count = await rds_service.get_rds_count_by_engine(session)
    return rds_engine_count

@rds_router.get('/rds/engine/az-count', response_model=List[AccountAZCount])
async def get_rds_count_by_az_account(
                              session:AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    rds_engine_count = await rds_service.get_rds_count_by_az_account(session)
    return rds_engine_count

@rds_router.get('/rds/engine/ver-count', response_model=List[RdsEngineAccountCount])
async def get_rds_count_by_account_engine(
                              session:AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    rds_engine_count = await rds_service.get_rds_count_by_account_engine(session)
    return rds_engine_count

@rds_router.get('/rds/created/count', response_model=RdsInstanceTotalCount)
async def get_rds_created_count(interval: Optional[str] = None, 
                              duration: Optional[str] = None,
                              session:AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    if validate_interval_duration(interval, duration):
        rds_created_counts = await rds_service.get_rds_created_count(interval, duration ,session)
        return RdsInstanceTotalCount(total_instances=rds_created_counts)
    else:
        raise InvalidParameters
    
    
@rds_router.get("/rds/getall", response_model=list[RdsInstAwsAcctFilterRead])
#@rds_router.get("/rds/getall")
async def get_all_rds(viewmode: Optional[str] = 'all', session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    all_accounts = await rds_service.get_rds_instances(viewmode,session)
    return all_accounts


#@rds_router.get("/rds/getall/minoreol", response_model=list[RdsEolMinorFilterRead])
@rds_router.get("/rds/getall/minoreol", response_model=RdsEOLMinorFilterReadAWS)
async def get_minor_eol_detail(viewmode: Optional[str] = 'all', session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    minor_eol_data = await rds_service.get_minor_eol_detail(viewmode,session)
    minor_refresh_date = await rds_service.get_minor_last_refresh_date(session)
    
    return { "minor_eol_data" : minor_eol_data, "minor_refresh_date" : minor_refresh_date}

@rds_router.get("/rds/getall/majoreol", response_model=RdsEOLMajorFilterReadAWS)
async def get_major_eol_detail(viewmode: Optional[str] = 'all', session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    minor_eol_data = await rds_service.get_major_eol_detail(viewmode,session)
    minor_refresh_date = await rds_service.get_major_last_refresh_date(session)
    
    return { "major_eol_data" : minor_eol_data, "major_refresh_date" : minor_refresh_date}


@rds_router.get('/rds/instance/{riid}', response_model=RdsInstanceRead)
async def get_rds_detail(riid:str,session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)) -> dict:
    account = await rds_service.get_rds_by_riid(riid,session)
    if account:
        return account
    else:
        raise AwsAccountNotFound 
    
@rds_router.get('/rds/engine/hw/ebs-types/refresh')
async def get_ebs_hw_detail_from_aws(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    url="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html"
    #hwdata = await rds_service.get_rds_hw_detail_from_aws(url,session)
    count = await rds_service.get_ebs_hw_detail_from_aws(url,session)
    return {"status": "success"}

@rds_router.get('/rds/engine/hw/rds-types/refresh')
async def get_rds_hw_detail_from_aws(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    url="https://aws.amazon.com/rds/instance-types"
    count = await rds_service.get_rds_hw_detail_from_aws(url,session)
    return {"status": "success"}

@rds_router.get('/rds/engine/hw/ebs-types/detail', response_model=List[Ec2HWDetail])
async def get_ebs_hw_detail_from_api(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rdstypes = await rds_service.get_ebs_hw_detail_from_api(session)
    return rdstypes

@rds_router.get('/rds/engine/hw/rds-types/detail',response_model=List[RdsHWDetail])
async def get_rds_hw_detail_from_api(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rdstypes = await rds_service.get_rds_hw_detail_from_api(session)
    return rdstypes

@rds_router.get('/rds/engine/eol/refresh')
async def get_rds_postgresl_eol(engine, version, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    if engine == "postgres":
        url="https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html"
        pg_eol=await rds_service.get_rds_postgresl_eol(url,session)
        return pg_eol
    elif engine =="aurora-postgresql":
        url="https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/aurorapostgresql-release-calendar.html"
        apg_eol=await rds_service.get_rds_aurorapg_eol(url,session)
        return apg_eol 
    elif engine == "mysql":
        url="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html"
        apg_eol=await rds_service.get_rds_mysql_eol(url,version,engine,session)
        return apg_eol
    elif engine == "aurora-mysql":
        url="https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/AuroraMySQL.release-calendars.html"
        apg_eol=await rds_service.get_rds_mysql_eol(url,version,engine,session)
        return apg_eol        
    else:
        return {}          

@rds_router.get('/rds/engine/hw-details/{riid}', response_model=RdsHWEc2Read)
async def get_rds_hw_types(riid:str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rds_hw = await rds_service.get_rds_instance_type(riid,session)
    return rds_hw

@rds_router.get('/rds/engine/eol')
async def get_rds_engine_eol(eoltype:str = 'major', session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    if eoltype == 'major':
        rds_hw = await rds_service.get_major_eol_pg(session)
    else:
        rds_hw = await rds_service.get_minor_eol_pg(session)
    return {"eolcount": rds_hw}

@rds_router.get('/rds/engine/eol/detail/major', response_model=List[RdsEngineMajor])
async def get_engine_eol_detail_major(engine:str = 'postgres', session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rdseol = await rds_service.get_engine_eol_detail_major(engine,session)
    return rdseol

@rds_router.get('/rds/engine/eol/detail/minor', response_model=List[RdsEngineMinor])
async def get_engine_eol_detail_minor(engine:str = 'postgres', session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rdseol = await rds_service.get_engine_eol_detail_minor(engine,session)
    return rdseol


@rds_router.get('/rds/engine/secrules', response_model=List[RdsSecRulesRead])
async def get_rds_secrules(riid:str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rds_secrules = await rds_service.get_rds_sec_rules(riid, session)
    return rds_secrules

@rds_router.get('/rds/engine/params', response_model=List[RdsInstParamsRead])
async def get_rds_inst_params(riid:str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rds_instparams = await rds_service.get_rds_inst_params(riid, session)
    return rds_instparams


@rds_router.get('/rds/account/engine/count')
async def get_rds_count_by_awsact_engine(session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rds_awsact_engine_count = await rds_service.get_rds_count_by_awsact_engine(session)
    #print(rds_awsact_engine_count)
    return rds_awsact_engine_count

@rds_router.get('/rds/engine/recent/activity', response_model=List[RdsRecentActivity])
async def get_rds_recent_activity(duration : str, session:AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    rdsdata = await rds_service.get_rds_recent_activity(duration, session)
    return rdsdata

@rds_router.post('/rds/instance', response_model=RdsInstanceRead, status_code=status.HTTP_201_CREATED)
async def create_rds_instance(account_data: RdsInstanceBaseSeed, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.create_rds_instance(account_data, session)
    return new_acn

@rds_router.post('/rds/instance/map', status_code=status.HTTP_201_CREATED)
async def create_rds_account_map(account_data: RdsAWSMappingCreate, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.create_rds_account_map(account_data, session)
    return new_acn

@rds_router.post('/rds/instance/parameter', status_code=status.HTTP_201_CREATED)
async def create_rds_parameters(account_data: RdsInstParamsCreate, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.create_rds_parameters(account_data, session)
    return new_acn

@rds_router.post('/rds/instance/secrules', status_code=status.HTTP_201_CREATED)
async def create_rds_secrules(account_data: RdsSecRulesCreate, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.create_rds_secrules(account_data, session)
    return new_acn

@rds_router.post('/rds/instance/snapshot', status_code=status.HTTP_201_CREATED)
async def create_rds_snapshots(account_data: RdsSnapShotsBase, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.create_rds_snapshots(account_data, session)
    return new_acn

@rds_router.get('/rds/instance/snapshots', response_model=List[RdsSnapShotsRead])
async def view_rds_snapshots(view_mode: str, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.view_rds_snapshots(view_mode, session)
    return new_acn

@rds_router.post('/rds/instance/snapshot/map', status_code=status.HTTP_201_CREATED)
async def create_snap_aws_rds_map(account_data: SnapAwsRdsMapBase, session: AsyncSession = Depends(get_session), 
                              token_details : dict =Depends(access_token_bearer)):
    new_acn = await rds_service.create_snap_aws_rds_map(account_data, session)
    return new_acn

@rds_router.post('/rds/instance/map/reset/{aws_aid}/{map_rds_az}', status_code=status.HTTP_201_CREATED)
async def reset_rds_instance_map(aws_aid:str, map_rds_az: str, session: AsyncSession = Depends(get_session), token_details : dict =Depends(access_token_bearer)):
    status = await rds_service.reset_rds_instance_map(aws_aid, map_rds_az, session)
    return status