from datetime import timedelta, datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
from src.db.models import AwsAccount, RdsAWSMap, RdsInstance, RdsHWDetail, Ec2HWDetail, RdsEngineMajor, RdsEngineMinor, RdsSecRules, \
    RdsInstParams, RdsSnapShots, SnapAwsRdsMap
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload,joinedload,contains_eager
from sqlmodel import select, func, literal, case
from sqlalchemy import desc, text, tuple_, Date, String, union_all, update
from .schemas import AwsAccountCreate, AccountRdsCountData, RdsCountPerDay, RdsAzAccountCount, AccountAZCount, RdsInstAwsAcctRead, \
    RdsInstAwsAcctFilterRead, RdsSnapShotsBase, RdsInstanceBaseSeed, RdsAWSMappingCreate, RdsInstParamsCreate, RdsSecRulesCreate, SnapAwsRdsMapBase
from .utils import scrape_rds_instances, scrape_ebs_instances, get_postgres_eol, get_aurorapg_eol ,get_mysql_eol_from_aws, extract_eol_amysql_major_table

class RdsService:
    async def get_aws_accounts(self, session: AsyncSession):
        statement = select(AwsAccount)
        results = await session.exec(statement)
        awsaccounts = results.all()
        return awsaccounts

    async def get_account_by_acn(self, account_number: str, session: AsyncSession):
        statement = select(AwsAccount).where(
            AwsAccount.account_number == account_number
        )
        result = await session.exec(statement)
        account = result.first()
        return account

    async def get_account_by_aid(self, aid: str, session: AsyncSession):
        statement = select(AwsAccount).where(AwsAccount.aid == aid)
        result = await session.exec(statement)
        account = result.first()
        return account

    async def get_account_by_account_number(self, account_number: str, session: AsyncSession):
        statement = select(AwsAccount).where(AwsAccount.account_number == account_number)
        result = await session.exec(statement)
        account = result.first()
        return account

    async def account_exsits(self, account_number: str, session: AsyncSession):
        useracn = await self.get_account_by_acn(account_number, session)
        return useracn is not None

    async def create_aws_accounts(
        self, account_data: AwsAccountCreate, session: AsyncSession
    ):
        account_data_dict = account_data.model_dump()
        new_account = AwsAccount(**account_data_dict)
        session.add(new_account)
        await session.commit()
        return new_account

    async def update_aws_account(
        self, aid: str, update_data: AwsAccountCreate, session: AsyncSession
    ):
        account_to_update = await self.get_account_by_aid(aid, session)
        if account_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(account_to_update, k, v)
            await session.commit()
            return account_to_update
        else:
            return None

    async def delete_aws_account(self, aid: str, session: AsyncSession):
        account_to_delete = await self.get_account_by_aid(aid, session)
        if account_to_delete is not None:
            await session.delete(account_to_delete)
            await session.commit()
            return {}
        else:
            return None

    async def get_total_instances(self, status, session: AsyncSession):
        statement = (
            select(func.count())
            .select_from(RdsInstance)
            .join(RdsAWSMap, (RdsInstance.riid == RdsAWSMap.rds_riid))
            .where(RdsAWSMap.last_collection_at == 0)
        )
        if status:
            if status == "up":
                statement = statement.where(RdsInstance.rds_inststatus != "stopped")
            else:
                statement = statement.where(RdsInstance.rds_inststatus == "stopped")
        result = await session.exec(statement)
        return result.first() or 0

    async def get_rds_count_by_account(self, interval, duration, session: AsyncSession):
        thirty_days_ago = datetime.utcnow() - timedelta(days=int(duration))
        created_date = func.date(RdsInstance.created_at)
        region_part = func.left(
            RdsInstance.rds_az,
            func.length(RdsInstance.rds_az) - 1
        )

        concat_value = RdsInstance.rds_identifier + region_part        
        statement = (
            select(
                created_date.label("created_date"),
                AwsAccount.account_alias,
                func.count(func.distinct(concat_value)).label(
                    "rds_count"
                ),
            )
            .join(AwsAccount, RdsInstance.rds_aws_id == AwsAccount.aid)
            .where(RdsInstance.created_at >= thirty_days_ago)
            .group_by(created_date, AwsAccount.account_alias)
            .order_by(created_date)
        )

        results = await session.exec(statement)
        rows = results.all()
        grouped = defaultdict(list)
        for row in rows:
            grouped[row.account_alias].append(
                RdsCountPerDay(
                    date=row.created_date.strftime("%Y-%m-%d"), rds_count=row.rds_count
                )
            )
        result = [
            AccountRdsCountData(account_alias=account, data=data_list)
            for account, data_list in grouped.items()
        ]
        return result

    async def get_rds_count_by_engine(self, session: AsyncSession):
        statement = (
            select(
                RdsInstance.rds_engine,
                func.count(RdsInstance.rds_identifier).label("rds_count"),
            )
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .where(RdsAWSMap.last_collection_at == 0)
            .group_by(RdsInstance.rds_engine)
        )
        results = await session.exec(statement)
        rows = results.all()
        return rows

    async def get_rds_count_by_az_account(self, session: AsyncSession):
        az_prefix = func.left(
            RdsInstance.rds_az, func.length(RdsInstance.rds_az) - literal(1)
        )
        statement = (
            select(
                AwsAccount.account_alias,
                az_prefix.label("rds_az"),
                func.count().label("rds_count"),
            )
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, RdsInstance.rds_aws_id == AwsAccount.aid)
            .where(RdsAWSMap.last_collection_at == 0)
            .group_by(
                AwsAccount.account_alias, az_prefix  
            ).order_by (desc(AwsAccount.account_alias))
        )
        results = await session.exec(statement)
        rows = results.all()
        grouped = defaultdict(list)
        for row in rows:
            grouped[row.account_alias].append(
                RdsAzAccountCount(rds_az=row.rds_az, rds_count=row.rds_count)
            )

        accounts_data = [
            AccountAZCount(account_alias=account, data=data_list)
            for account, data_list in grouped.items()
        ]
        return accounts_data
    
    async def get_rds_count_by_account_engine(self, session: AsyncSession):
        rds_enginever = func.substring(RdsInstance.rds_enginever, r'^\d+').label("rds_enginever")
        statement = (
            select(
                #AwsAccount.account_alias,
                RdsInstance.rds_engine,
                rds_enginever,
                func.count().label("rds_count")
            )
            .join(AwsAccount, RdsInstance.rds_aws_id == AwsAccount.aid)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .where(AwsAccount.account_status == True)
            .where(RdsAWSMap.last_collection_at == 0)
            .group_by(
                #AwsAccount.account_alias,
                RdsInstance.rds_engine,
                rds_enginever
            )
        )
        results = await session.exec(statement)
        rows = results.all()
        return rows


    async def get_rds_created_count(self, interval, duration, session: AsyncSession):
        durationdays = datetime.utcnow() - timedelta(days=int(duration))
        statement = (select(
                func.count(
                    func.distinct(
                        tuple_(
                            RdsInstance.rds_identifier,
                            func.to_char(
                                RdsInstance.rds_instcreatetime,
                                text("'YYYY-MM-DD'")
                            )
                        )
                    )
                ).label("total_instances")
            )
            .select_from(RdsInstance)
            .join(AwsAccount, RdsInstance.rds_aws_id == AwsAccount.aid)
            .where(RdsInstance.rds_instcreatetime >= durationdays)
            )
        results = await session.exec(statement)
        #rows = results.all()
        return results.first() or 0

    async def get_rds_instances(self, viewmode,session: AsyncSession):
        cutoff = datetime.utcnow() - timedelta(days=30)
        columns = [
            AwsAccount.aid,
            AwsAccount.account_alias,
            RdsInstance.rds_identifier,
            RdsInstance.riid,
            RdsInstance.rds_engine,
            RdsInstance.rds_instcreatetime,
            RdsInstance.rds_enginever,
        ]
        statement = (
            select(*columns)
            .join(RdsAWSMap, RdsAWSMap.rds_riid == RdsInstance.riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .where(AwsAccount.account_status == True)
            .where(RdsAWSMap.last_collection_at == 0)
        )
        if viewmode == 'recent':
            statement = statement.filter(RdsInstance.rds_instcreatetime >= cutoff)
        elif viewmode == 'up': 
            statement = statement.filter(RdsInstance.rds_inststatus != 'stopped')
        elif viewmode == 'down':
            statement = statement.filter(RdsInstance.rds_inststatus == 'stopped')
        elif viewmode == 'eolmajor':
            return await self.get_eol_major(columns, session)
        elif viewmode == 'eolminor':
            return await self.get_minor_eol_detail(columns, session)        
        else:
            pass
        results = await session.exec(statement)
        rows = results.all() 
        return rows
    
    async def get_rds_by_riid(self, riid: str, session: AsyncSession):
        statement = select(RdsInstance).where(RdsInstance.riid == riid)
        result = await session.exec(statement)
        account = result.first()
        return account   
        """
            async def get_rds_instances(self, session: AsyncSession):
        cutoff = datetime.utcnow() - timedelta(days=30)
        statement = (
            select(RdsInstance)
            .join(RdsAWSMap, RdsAWSMap.rds_riid == RdsInstance.riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .options(contains_eager(RdsInstance.aws_accounts))
            .filter(RdsInstance.rds_instcreatetime >= cutoff)
        )
        result = await session.exec(statement)
        return result.unique().all()
        """

    async def get_rds_hw_detail_from_aws(self,url: str, session: AsyncSession):
        data = scrape_rds_instances(url)

        updated = 0
        inserted = 0
        for row in data:
            rds_hw_type = row.get("rds_hw_type")
            rds_hw_model = row.get("rds_hw_model")
            
            if not rds_hw_model:
                continue

            statement = (
                select(RdsHWDetail)
                .where(RdsHWDetail.rds_hw_type == rds_hw_type)
                .where(RdsHWDetail.rds_hw_model == rds_hw_model)
            )
            result = await session.exec(statement)
            existing = result.first()

            if existing:
                for key, value in row.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                new_instance = RdsHWDetail(**row)
                session.add(new_instance)
                inserted += 1

        await session.commit()
        return {
            "inserted": inserted,
            "updated": updated,
            "total_processed": len(data)
        }
    
    async def get_ebs_hw_detail_from_aws(self,url: str, session: AsyncSession):
        data = scrape_ebs_instances(url)    
        updated = 0
        inserted = 0
        for row in data:
            ec2_hw_model = row.get("ec2_hw_model")
            
            if not ec2_hw_model:
                continue

            statement = (
                select(Ec2HWDetail)
                .where(Ec2HWDetail.ec2_hw_model == ec2_hw_model)
            )
            result = await session.exec(statement)
            existing = result.first()

            if existing:
                for key, value in row.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                new_instance = Ec2HWDetail(**row)
                session.add(new_instance)
                inserted += 1

        await session.commit()
        
    async def get_rds_hw_details(self,model:str, session : AsyncSession):
        joincondition = func.replace(RdsHWDetail.rds_hw_model, "db.", "")
        columns = [
            RdsHWDetail.rds_hw_model,
            Ec2HWDetail.ec2_hw_type,
            RdsHWDetail.rds_hw_vcpu,
            RdsHWDetail.rds_hw_core,
            RdsHWDetail.rds_hw_mem,
            RdsHWDetail.rds_hw_storage,
            RdsHWDetail.rds_hw_net_gbps,
            Ec2HWDetail.ec2_hw_basebandwm,
            Ec2HWDetail.ec2_hw_maxbandwm,
            Ec2HWDetail.ec2_hw_basethroputm,
            Ec2HWDetail.ec2_hw_maxthroputm,
            Ec2HWDetail.ec2_hw_baseiopsm,
            Ec2HWDetail.ec2_hw_maxiopswm
        ]

        statement = (
            select(*columns)
            .join(RdsHWDetail, joincondition == Ec2HWDetail.ec2_hw_model)
            .where(RdsHWDetail.rds_hw_model == model)
        )
        results = await session.exec(statement)
        rows = results.first() 
        return rows
    
    async def get_rds_instance_type(self,riid:str, session : AsyncSession):
        statement = select(RdsInstance.rds_instanceclass).where(
            RdsInstance.riid == riid
        )
        result = await session.exec(statement)
        rds_model = result.first()
        data = await self.get_rds_hw_details(rds_model, session)
        if data:
            return {"rds_hw_details": data}  
        else:
            return {"rds_hw_details": None}


    async def get_ebs_hw_detail_from_api(self, session: AsyncSession):
        statement = select(Ec2HWDetail)
        result = await session.exec(statement)
        insttypes = result.all()
        return insttypes
    
    async def get_rds_hw_detail_from_api(self, session: AsyncSession):
        statement = select(RdsHWDetail)
        result = await session.exec(statement)
        insttypes = result.all()
        return insttypes

    async def get_rds_major_eol_save (self, data, session):
        inserted=0
        updated=0
        for row in data:
            rds_ma_ver = row.get("rds_ma_ver")
            rds_ma_type = row.get("rds_ma_type")
            statement = (
                select(RdsEngineMajor)
                .where(RdsEngineMajor.rds_ma_ver == rds_ma_ver)
                .where(RdsEngineMajor.rds_ma_type == rds_ma_type)
            )            
            result = await session.exec(statement)
            existing = result.first()

            if existing:
                for key, value in row.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                new_instance = RdsEngineMajor(**row)
                session.add(new_instance)
                inserted += 1
        await session.commit()
        return {
            "inserted": inserted,
            "updated": updated,
            "total_processed": len(data)
        }

    async def get_rds_minor_eol_save (self, data, session):
        inserted=0
        updated=0
        for row in data:
            rds_mi_ver = row.get("rds_mi_ver")
            rds_mi_type = row.get("rds_mi_type")
            statement = (
                select(RdsEngineMinor)
                .where(RdsEngineMinor.rds_mi_ver == rds_mi_ver)
                .where(RdsEngineMinor.rds_mi_type == rds_mi_type)
            )            
            result = await session.exec(statement)
            existing = result.first()

            if existing:
                for key, value in row.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                new_instance = RdsEngineMinor(**row)
                session.add(new_instance)
                inserted += 1
        await session.commit()
        return {
            "inserted": inserted,
            "updated": updated,
            "total_processed": len(data)
        }       
        
    async def get_rds_postgresl_eol(self,url:str, session : AsyncSession):
        data = get_postgres_eol(url)
        result= {}
        major = await self.get_rds_major_eol_save(data['major'], session)
        minor = await self.get_rds_minor_eol_save(data['minor'], session)
        result["major"] = major
        result["minor"] = minor
        return result
        
    async def get_rds_aurorapg_eol(self,url:str, session : AsyncSession):
        data = get_aurorapg_eol(url)
        print(data)
        result={}
        major = await self.get_rds_major_eol_save(data['major'], session)
        minor = await self.get_rds_minor_eol_save(data['minor'], session)
        result["major"] = major
        result["minor"] = minor
        return result
    
    async def get_major_eol_pg(self, session: AsyncSession):
        regex_condition = RdsEngineMajor.rds_ma_rds_seol.op('~')('^[A-Za-z]+\\s+\\d{4}$')

        days_diff_expr = case(
            (
                regex_condition,
                func.to_date(func.concat('1 ', RdsEngineMajor.rds_ma_rds_seol), 'DD Month YYYY')
            ),
            else_=func.to_date(RdsEngineMajor.rds_ma_rds_seol, 'DD Month YYYY')
        ).cast(Date) - func.now().cast(Date)
        statement = (
            select(func.count())
            .select_from(RdsInstance)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMajor,
                (RdsInstance.rds_engine == RdsEngineMajor.rds_ma_type) &
                (func.substring(RdsInstance.rds_enginever, '^[^.]+') == RdsEngineMajor.rds_ma_ver)
            )
            .where(days_diff_expr < 180)
            .where(AwsAccount.account_status== True)
            .where(RdsAWSMap.last_collection_at == 0)
        )
        result = await session.exec(statement)
        return result.first() or 0

    async def get_eol_major(self,columns, session: AsyncSession):

        col = RdsEngineMajor.rds_ma_rds_seol

        # Fix typo once
        clean_text = func.replace(col, 'Septemeber', 'September')

        parsed_date = case(
            # Month YYYY → assume 1st day
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(func.concat('1 ', clean_text), 'DD Month YYYY')
            ),
            # 8 May 2025
            (
                col.op('~')('^\\d{1,2}\\s+[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(clean_text, 'DD Month YYYY')
            ),
            # April 8 2025
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{1,2}\\s+\\d{4}$'),
                func.to_date(clean_text, 'Month DD YYYY')
            ),
            else_=None
        ).cast(Date)    


        days_until_eol = (parsed_date - func.current_date()).cast(String).label("days_until_eol")
        today = func.current_date()
        one180days = today + text("interval '180 days'")
        
        columns = [
            AwsAccount.aid,
            AwsAccount.account_alias,
            RdsInstance.rds_identifier,
            RdsInstance.riid,
            RdsInstance.rds_engine,
            RdsInstance.rds_instcreatetime,
            RdsInstance.rds_enginever,
            RdsEngineMajor.ma_row_created_at,
            RdsEngineMajor.rds_ma_rds_seol,
            days_until_eol
        ]

        statement = (
            select(*columns)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMajor,
                (RdsInstance.rds_engine == RdsEngineMajor.rds_ma_type) &
                (func.substring(RdsInstance.rds_enginever, '^[^.]+') == RdsEngineMajor.rds_ma_ver)
            )
            .where(parsed_date.isnot(None))
            .where(parsed_date >= today)
            .where(parsed_date <= one180days)
            .where(AwsAccount.account_status.is_(True))
            .where(RdsAWSMap.last_collection_at == 0)
        )
        results = await session.exec(statement)
        rows = results.all() 
        return rows

    async def get_major_eol_detail(self, viewmode, session):

        col = RdsEngineMajor.rds_ma_rds_seol

        # Fix typo once
        clean_text = func.replace(col, 'Septemeber', 'September')

        parsed_date = case(
            # Month YYYY → assume 1st day
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(func.concat('1 ', clean_text), 'DD Month YYYY')
            ),
            # 8 May 2025
            (
                col.op('~')('^\\d{1,2}\\s+[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(clean_text, 'DD Month YYYY')
            ),
            # April 8 2025
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{1,2}\\s+\\d{4}$'),
                func.to_date(clean_text, 'Month DD YYYY')
            ),
            else_=None
        ).cast(Date)    


        days_until_eol = (parsed_date - func.current_date()).cast(String).label("days_until_eol")
        today = func.current_date()
        one180days = today + text("interval '180 days'")
        
        columns = [
            AwsAccount.aid,
            AwsAccount.account_alias,
            RdsInstance.rds_identifier,
            RdsInstance.riid,
            RdsInstance.rds_engine,
            RdsInstance.rds_instcreatetime,
            RdsInstance.rds_enginever,
            RdsEngineMajor.ma_row_created_at,
            RdsEngineMajor.rds_ma_rds_seol,
            days_until_eol
        ]

        statement = (
            select(*columns)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMajor,
                (RdsInstance.rds_engine == RdsEngineMajor.rds_ma_type) &
                (func.substring(RdsInstance.rds_enginever, '^[^.]+') == RdsEngineMajor.rds_ma_ver)
            )
            .where(parsed_date.isnot(None))
            .where(parsed_date >= today)
            .where(parsed_date <= one180days)
            .where(AwsAccount.account_status.is_(True))
            .where(RdsAWSMap.last_collection_at == 0)
        )
        results = await session.exec(statement)
        rows = results.all() 
        return rows        

    async def get_minor_eol_pg(self, session: AsyncSession):

        col = RdsEngineMinor.rds_mi_seol

        # Fix typo once
        clean_text = func.replace(col, 'Septemeber', 'September')

        parsed_date = case(
            # Month YYYY → assume 1st day
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(func.concat('1 ', clean_text), 'DD Month YYYY')
            ),
            # 8 May 2025
            (
                col.op('~')('^\\d{1,2}\\s+[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(clean_text, 'DD Month YYYY')
            ),
            # April 8 2025
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{1,2}\\s+\\d{4}$'),
                func.to_date(clean_text, 'Month DD YYYY')
            ),
            else_=None
        ).cast(Date)

        today = func.current_date()
        ninety_days_from_now = today + text("interval '90 days'")

        statement = (
            select(func.count())
            .select_from(RdsInstance)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMinor,
                (RdsInstance.rds_engine == RdsEngineMinor.rds_mi_type) &
                (RdsInstance.rds_enginever == RdsEngineMinor.rds_mi_ver)
            )
            .where(parsed_date.isnot(None))
            .where(parsed_date >= today)
            .where(parsed_date <= ninety_days_from_now)
            .where(AwsAccount.account_status.is_(True))
            .where(RdsAWSMap.last_collection_at == 0)
        )

        result = await session.exec(statement)
        return result.first() or 0


    """
    async def get_minor_eol_pg(self, session: AsyncSession):
        
        regex_condition = RdsEngineMinor.rds_mi_seol.op('~')('^[A-Za-z]+\\s+\\d{4}$')
        clean_text = func.replace(RdsEngineMinor.rds_mi_seol, 'Septemeber', 'September')
        parsed_date = case(
            (
                regex_condition,
                func.to_date(func.concat('1 ', clean_text), 'DD Month YYYY')
            ),
            else_=func.to_date(clean_text, 'DD Month YYYY')
        ).cast(Date)
        days_diff_expr = func.extract(
            'day',
            func.age(func.now().cast(Date), parsed_date)
        )        
        statement = (
            select(func.count())
            .select_from(RdsInstance)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMinor,
                (RdsInstance.rds_engine == RdsEngineMinor.rds_mi_type) &
                (RdsInstance.rds_enginever == RdsEngineMinor.rds_mi_ver)
            )
            .where(days_diff_expr < 90)
            .where(AwsAccount.account_status== True)
        )
        result = await session.exec(statement)
        return result.first() or 0
        """
    
    async def get_minor_eol_detail(self, columns, session: AsyncSession):

        col = RdsEngineMinor.rds_mi_seol

        # Fix typo once
        clean_text = func.replace(col, 'Septemeber', 'September')

        parsed_date = case(
            # Month YYYY → assume 1st day
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(func.concat('1 ', clean_text), 'DD Month YYYY')
            ),
            # 8 May 2025
            (
                col.op('~')('^\\d{1,2}\\s+[A-Za-z]+\\s+\\d{4}$'),
                func.to_date(clean_text, 'DD Month YYYY')
            ),
            # April 8 2025
            (
                col.op('~')('^[A-Za-z]+\\s+\\d{1,2}\\s+\\d{4}$'),
                func.to_date(clean_text, 'Month DD YYYY')
            ),
            else_=None
        ).cast(Date).label("parsed_date")
        days_until_eol = (parsed_date - func.current_date()).cast(String).label("days_until_eol")
        
        columns = [
            AwsAccount.aid,
            AwsAccount.account_alias,
            RdsInstance.rds_identifier,
            RdsInstance.riid,
            RdsInstance.rds_engine,
            RdsInstance.rds_instcreatetime,
            RdsInstance.rds_enginever,
            RdsEngineMinor.mi_row_created_at,
            RdsEngineMinor.rds_mi_seol,
            days_until_eol
        ]

        today = func.current_date()
        ninety_days_from_now = today + text("interval '90 days'")


        statement = (
            select(*columns)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMinor,
                (RdsInstance.rds_engine == RdsEngineMinor.rds_mi_type) &
                (RdsInstance.rds_enginever == RdsEngineMinor.rds_mi_ver)
            )
            .where(parsed_date.isnot(None))
            .where(parsed_date >= today)
            .where(parsed_date <= ninety_days_from_now)
            .where(AwsAccount.account_status.is_(True))
            .where(RdsAWSMap.last_collection_at == 0)
        )

        results = await session.exec(statement)
        return results.all()
    
    async def get_minor_last_refresh_date(self, session):
        statement = (
            select(
                RdsEngineMinor.rds_mi_type.label("rds_engine_type"),
                func.max(RdsEngineMinor.mi_row_created_at).label("latest_refreshed_at")
            )
            .group_by(RdsEngineMinor.rds_mi_type)
        )

        result = await session.exec(statement)
        return result.all()       

    async def get_major_last_refresh_date(self, session):
        statement = (
            select(
                RdsEngineMajor.rds_ma_type.label("rds_engine_type"),
                func.max(RdsEngineMajor.ma_row_created_at).label("latest_refreshed_at")
            )
            .group_by(RdsEngineMajor.rds_ma_type)
        )

        result = await session.exec(statement)
        return result.all()  

    """
    async def get_minor_eol_detail(self,columns, session: AsyncSession):
        
        regex_condition = RdsEngineMinor.rds_mi_seol.op('~')('^[A-Za-z]+\\s+\\d{4}$')
        clean_text = func.replace(RdsEngineMinor.rds_mi_seol, 'Septemeber', 'September')
        parsed_date = case(
            (
                regex_condition,
                func.to_date(func.concat('1 ', clean_text), 'DD Month YYYY')
            ),
            else_=func.to_date(clean_text, 'DD Month YYYY')
        ).cast(Date)
        days_diff_expr = func.extract(
            'day',
            func.age(func.now().cast(Date), parsed_date)
        )        
        statement = (
            select(*columns)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .join(AwsAccount, AwsAccount.aid == RdsAWSMap.aws_aid)
            .join(
                RdsEngineMinor,
                (RdsInstance.rds_engine == RdsEngineMinor.rds_mi_type) &
                (RdsInstance.rds_enginever == RdsEngineMinor.rds_mi_ver)
            )
            .where(days_diff_expr < 90)
            .where(AwsAccount.account_status== True)
        )
        results = await session.exec(statement)
        rows = results.all() 
        return rows
    """
    
    async def get_rds_sec_rules(self, riid: str, session: AsyncSession):
        statement = select(RdsSecRules).where(
            RdsSecRules.sec_riid == riid
        )
        result = await session.exec(statement)
        secrules = result.all()
        return secrules
    
    async def get_rds_inst_params(self, riid: str, session: AsyncSession):
        statement = select(RdsInstParams).where(
            RdsInstParams.param_riid == riid
        )
        result = await session.exec(statement)
        secrules = result.all()
        return secrules
    
    async def get_engine_eol_detail_major(self, engine: str, session: AsyncSession):
        statement = select(RdsEngineMajor).where(
            RdsEngineMajor.rds_ma_type == engine
        ).order_by (desc(RdsEngineMajor.rds_ma_type))
        result = await session.exec(statement)
        secrules = result.all()
        return secrules
    
    async def get_engine_eol_detail_minor(self, engine: str, session: AsyncSession):
        statement = select(RdsEngineMinor).where(
            RdsEngineMinor.rds_mi_type == engine
        ).order_by (desc(RdsEngineMinor.rds_mi_type))
        result = await session.exec(statement)
        secrules = result.all()
        return secrules
    

    async def get_rds_count_by_awsact_engine(self, session: AsyncSession):
        statement = (
            select(
                AwsAccount.account_alias,
                RdsInstance.rds_engine,
                func.count().label("rds_count")
            )
            .join(AwsAccount, RdsInstance.rds_aws_id == AwsAccount.aid)
            .join(RdsAWSMap, RdsInstance.riid == RdsAWSMap.rds_riid)
            .where(AwsAccount.account_status == True)
            .group_by(
                AwsAccount.account_alias,
                RdsInstance.rds_engine,
            )
        )

        results = await session.exec(statement)
        rows = results.all()

        if not rows:
            return {"dataset": []}

        accounts = sorted(list({r.account_alias for r in rows}))
        engines = sorted(list({r.rds_engine for r in rows}))

        # Prepare dataset
        dataset = []
        header = ["rds_engine", *accounts]
        dataset.append(header)

        for engine in engines:
            row = [engine]
            for account in accounts:
                match = next((r.rds_count for r in rows if r.account_alias == account and r.rds_engine == engine), 0)
                row.append(match)
            dataset.append(row)

        return {"dataset": dataset}


    async def get_rds_recent_activity(self, duration, session: AsyncSession):
        """_summary_
        WITH account_collection AS (
        SELECT a.account_alias, MAX(r.created_at) AS max_collection
        FROM rdsinstances r
        JOIN awsaccounts a ON a.aid = r.rds_aws_id
        GROUP BY a.account_alias
        ),
        rds_seen as (
            SELECT r.rds_identifier,
                a.account_alias,
                MIN(r.rds_instcreatetime) AS first_seen,
                MAX(r.created_at) AS last_seen
        FROM rdsinstances r
        JOIN awsaccounts a ON a.aid = r.rds_aws_id
        WHERE r.created_at >= NOW() - INTERVAL '30 days'
        GROUP BY r.rds_identifier, a.account_alias)
        SELECT
        rs.rds_identifier,
        rs.account_alias,
        'create' AS event_type,
        rs.first_seen AS event_time,
        rs.last_seen
        FROM rds_seen rs
        where first_seen >= NOW() - INTERVAL '30 days'
        union all
        SELECT
        rs.rds_identifier,
        rs.account_alias,
        'deleted' AS event_type,
        rs.last_seen AS event_time,   -- use last_seen as the chronological point
        rs.last_seen
        FROM rds_seen rs
        JOIN account_collection ac ON ac.account_alias = rs.account_alias
        WHERE rs.last_seen < ac.max_collection - INTERVAL '1 day'
        ORDER BY event_time ASC;
        ;
        """
        n_days = datetime.utcnow() - timedelta(days=int(duration))

        account_collection = (
            select(
                AwsAccount.account_alias,
                func.max(RdsInstance.created_at).label("max_collection")
            )
            .join(AwsAccount, AwsAccount.aid == RdsInstance.rds_aws_id)
            .where(AwsAccount.account_status== True)
            .where(RdsInstance.created_at >= n_days)
            .group_by(AwsAccount.account_alias)
            .cte("account_collection")
        )

        rds_seen = (
            select(
                RdsInstance.rds_identifier,
                AwsAccount.account_alias,
                func.min(RdsInstance.rds_instcreatetime).label("first_seen"),
                func.max(RdsInstance.created_at).label("last_seen")
            )
            .join(AwsAccount, AwsAccount.aid == RdsInstance.rds_aws_id)
            .where(RdsInstance.created_at >= n_days)
            .where(AwsAccount.account_status== True)
            .group_by(RdsInstance.rds_identifier, AwsAccount.account_alias)
            .cte("rds_seen")
        )

        create_query = (
            select(
                rds_seen.c.rds_identifier,
                rds_seen.c.account_alias,
                literal("create").label("event_type"),
                rds_seen.c.first_seen.label("event_time"),
                rds_seen.c.last_seen
            )
            .where(rds_seen.c.first_seen >= n_days)
        )
        
        deleted_query = (
            select(
                rds_seen.c.rds_identifier,
                rds_seen.c.account_alias,
                literal("deleted").label("event_type"),
                rds_seen.c.last_seen.label("event_time"),
                rds_seen.c.last_seen
            )
            .join(account_collection, account_collection.c.account_alias == rds_seen.c.account_alias)
            .where(rds_seen.c.last_seen < account_collection.c.max_collection - timedelta(days=1))
        )

        statement = union_all(create_query, deleted_query).order_by(desc("event_time"))
        results = await session.exec(statement)
        rows = results.all()
        return rows
    

    async def create_rds_instance(
        self, rds_data: RdsInstanceBaseSeed, session: AsyncSession
    ):
        rds_data_dict = rds_data.model_dump()
        new_account = RdsInstance(**rds_data_dict)
        session.add(new_account)
        await session.commit()
        return new_account
    
    async def create_rds_account_map(
        self, rds_data: RdsAWSMappingCreate, session: AsyncSession
    ):
        statement = (
                select(RdsAWSMap)
                .where(RdsAWSMap.aws_aid == rds_data.aws_aid)
                .where(RdsAWSMap.map_rds_identifier == rds_data.map_rds_identifier)
                .where(RdsAWSMap.map_rds_az == rds_data.map_rds_az)
        ) 
        print(rds_data)
        result = await session.exec(statement)
        existing = result.first()

        inserted =0
        updated = 0
        rds_data_dict = rds_data.model_dump()
        if existing:
            for key, value in rds_data_dict.items():
                setattr(existing, key, value)
            updated += 1
        else:
            new_instance = RdsAWSMap(**rds_data_dict)
            session.add(new_instance)
            inserted += 1
        await session.commit()
        return {
            "inserted": inserted,
            "updated": updated,
        }          
        
    async def create_rds_parameters(
        self, rds_data: RdsInstParamsCreate, session: AsyncSession
    ):
        rds_data_dict = rds_data.model_dump()
        new_account = RdsInstParams(**rds_data_dict)
        session.add(new_account)
        await session.commit()
        return new_account
    
    async def create_rds_secrules(
        self, rds_data: RdsSecRulesCreate, session: AsyncSession
    ):
        rds_data_dict = rds_data.model_dump()
        new_account = RdsSecRules(**rds_data_dict)
        session.add(new_account)
        await session.commit()
        return new_account

    async def get_rds_mysql_eol(self,url:str, version, engine, session : AsyncSession):
        data = get_mysql_eol_from_aws(url, etype=version, engine=engine)
        if version == "minor":
            result = await self.get_rds_minor_eol_save(data, session)
            return result
        elif version == "major":
            result = await self.get_rds_major_eol_save(data, session)
            return result
        else:
            return {}    
        
    async def create_rds_snapshots(
        self, rds_data: RdsSnapShotsBase, session: AsyncSession
    ):
        rds_data_dict = rds_data.model_dump()
        new_account = RdsSnapShots(**rds_data_dict)
        session.add(new_account)
        await session.commit()
        return new_account  
    
    async def view_rds_snapshots(self, viewmode: str, session: AsyncSession):
        statement = select(RdsSnapShots)
        result = await session.exec(statement)
        secrules = result.all()
        return secrules  

    async def create_snap_aws_rds_map(
        self, rds_data: SnapAwsRdsMapBase, session: AsyncSession
    ):
        statement = (
                select(SnapAwsRdsMap)
                .where(SnapAwsRdsMap.sar_aws_aid == rds_data.sar_aws_aid)
                .where(SnapAwsRdsMap.sar_snap_identifier == rds_data.sar_snap_identifier)
                .where(SnapAwsRdsMap.sar_rds_az == rds_data.sar_rds_az)
        ) 
        print(rds_data)
        result = await session.exec(statement)
        existing = result.first()

        inserted =0
        updated = 0
        rds_data_dict = rds_data.model_dump()
        if existing:
            for key, value in rds_data_dict.items():
                setattr(existing, key, value)
            updated += 1
        else:
            new_instance = SnapAwsRdsMap(**rds_data_dict)
            session.add(new_instance)
            inserted += 1
        await session.commit()
        return {
            "inserted": inserted,
            "updated": updated,
        } 
    

    async def reset_rds_instance_map(self, aws_aid,map_rds_az, session):
        statement = update(RdsAWSMap).where(RdsAWSMap.aws_aid == aws_aid, RdsAWSMap.map_rds_az == map_rds_az).values(last_collection_at=-1)
        result = await session.exec(statement)
        if result:
            await session.commit()            
            return {"action":"success"}
        else:
            return {"action":"failed"}