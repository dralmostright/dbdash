import uuid
import random,string
import os, httpx, time, json
from datetime import datetime, timedelta,UTC
from dotenv import load_dotenv

class Settings:
    RDSAPI_URL = os.getenv("RDSAPI_URL")
    RDSPARAMS_URL = os.getenv("RDSPARAMS_URL")
    RDSSECRULES_URL = os.getenv("RDSSECRULES_URL")
    NUM_ACCOUNTS = 10
    RDS_PER_ACCOUNT = (5, 10)
    SEC_RULES_PER_RDS = (2, 5)
    PARAMS_PER_RDS = (2, 4)
    DAYS_HISTORY = 30
    STORAGE_TYPES = ["standard", "gp2", "gp3", "io1"]
    AWS_DOMAIN = "rds.amazonaws.com"

    ENGINE_VERSIONS = {
        "postgres": ["12.15", "13.11", "14.6", "15.3"],
        "mysql": ["5.7.44", "8.0.33"],
        "sqlserver-se": ["14.00.3456.2", "15.00.4316.3"],   
        "sqlserver-ee": ["14.00.3456.2", "15.00.4316.3"],  
        "oracle-se2": ["19.0.0.0.ru-2023-10.rur-2023-10"], 
    }

    INSTANCE_CLASSES = [
        "db.t3.medium",
        "db.m5.large",
        "db.r5.large",
    ]

    STATUSES = ["available", "stopped", "modifying"]

    REGION_AZ_MAP = {
        "us-east-1": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "us-west-1": ["us-west-1a", "us-west-1b"],
        "eu-west-1": ["eu-west-1a", "eu-west-1b", "eu-west-1c"],
    }  
    ENGINE_PORTS = {
        "postgres": "5432",
        "mysql": "3306",
        "mariadb": "3306",
        "oracle-se2": "1521",
        "sqlserver-se": "1433",
        "sqlserver-ee": "1433",
    }


"""_summary_

Raises:
    RuntimeError: _description_

Returns:
    _type_: _description_
"""
class APIClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(timeout=20)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        response = self.client.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        response = self.client.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

def get_api_token(username, password, url,max_attempts=5, delay=2):
    """
        Attempt to get API token using username and password.
        Retries up to `max_attempts` times if login fails.
        
        Args:
            username (str): username/email.
            password (str): password or hashed password.
            url (str): API login endpoint.
            max_attempts (int): Maximum retry attempts.
            delay (int): Seconds to wait between attempts.
        
        Returns:
            str: Access token if successful.
    """    
    client = httpx.Client(timeout=20)
    url = url
    payload = {
    "email": username,
    "password_hash": password
    }
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.post(url, json=payload)
            response.raise_for_status()
            
            token = response.json().get("access_token")
            if token:
                print(f">>>> Login successful on attempt {attempt}!")
                return token
            else:
                print(f">>>> Login attempt {attempt} failed: No token in response.")

        except httpx.HTTPStatusError as e:
            print(f">>>> Login attempt {attempt} failed: {e}")
        except httpx.RequestError as e:
            print(f">>>> Request error on attempt {attempt}: {e}")

        if attempt < max_attempts:
            print(f">>>> Retrying in {delay} seconds...")
            time.sleep(delay)
    
    raise RuntimeError(f">>>> Failed to login after {max_attempts} attempts")

def datetime_days_ago(days: int) -> datetime:
    return (datetime.now(UTC) - timedelta(days=days)).replace(tzinfo=None)

def random_account_regions():
    regions = ["us-east-1", "us-west-1", "eu-west-1"]
    r = random.random()

    if r < 0.2:           
        return [random.choice(regions)]
    elif r < 0.6:         
        return random.sample(regions, k=2)
    else:                 
        return regions.copy()

def pick_rds_az(account_regions, settings):
    region = random.choice(account_regions)
    return random.choice(settings.REGION_AZ_MAP[region])


def load_data():
    load_dotenv(override=True)  
    settings = Settings()  
    API_USERNAME = os.getenv("API_USERNAME")
    API_PASSWORD = os.getenv("API_PASSWORD")  
    API_TOKEN_URL = os.getenv("API_TOKEN_URL")
    API_BASE_URL = os.getenv("API_BASE_URL")
    token=get_api_token(API_USERNAME,API_PASSWORD,API_TOKEN_URL)
    #print(token)
    api = APIClient(base_url=API_BASE_URL, token=token)
    acct_endpoint = "/aws/org/register"
    rds_apiendpoint = "/aws/rds/instance"
    rds_apimapendpoint = "/aws/rds/instance/map"
    rds_apiparameter = "/aws/rds/instance/parameter"
    rds_apisecrules ="/aws/rds/instance/secrules"
    
    for i in range(settings.NUM_ACCOUNTS):
        regions = random_account_regions()
        account_number = random.randint(10**11, 10**12 - 1)
        payload = {
            "account_number": f"{account_number}",
            "account_alias": f"aws-acct-{i}",
            "account_org": "example-org",
            "account_az": ",".join(regions),
            "account_status": True,
            "description": "Seeded AWS account"
        }
        #print(payload)
        
        aid=api.post(acct_endpoint, payload)
        #account_aid= aid.get("aid")
        for region in regions:
            rds_count = random.randint(*settings.RDS_PER_ACCOUNT)
            for rds_idx in range(rds_count):
                ## replicate instance deletion
                skip_instance = random.random() < 0.05
                skip_days = random.randint(3, 30) if skip_instance else 0
                rds_engine = random.choice(list(settings.ENGINE_VERSIONS.keys()))
                rds_enginever = random.choice(settings.ENGINE_VERSIONS[rds_engine])  
                rds_instanceclass = random.choice(settings.INSTANCE_CLASSES)
                rds_allocstorage = str(random.randint(50, 100))
                rds_instcreatetime=random_datetime(365)
                rds_paramgroup = random_paramgroup(rds_engine)
                rds_az=pick_rds_az(regions, settings)
                rds_lisencemodel = random_lisencemodel(rds_engine)
                rds_copytagsnapshot = str(random.choice([True, False])).lower()
                rds_storagetype = random.choice(settings.STORAGE_TYPES)
                rds_multiaz = str(random.choice([True, False])).lower()
                rds_storageencrypted = str(random.choice([True, False])).lower()
                rds_deleteprotection = str(random.choice([True, False])).lower()
                rds_clusteridentifier = random_cluster_id() if random.random() < 0.5 else None
                rds_clusterendpoint = f"{rds_clusteridentifier}.{settings.AWS_DOMAIN}" if rds_clusteridentifier else None
                rds_identifier=random_rdsinst_id()
                rds_endpoint=f"{rds_identifier}.{settings.AWS_DOMAIN}"
                rds_port = str(settings.ENGINE_PORTS.get(rds_engine, "5432"))
                rds_vpc = random_vpc_id()
                rds_secgroup = random_secgroup_list()
                rds_subnetgrp = random_subnetgrp()
                rds_subnets = random_subnet_list()
                rds_backupretention = random_backup_retention()
                rds_taglist = random_taglist()
                rds_inststatus = random.choice(settings.STATUSES)
                for day in reversed(range(settings.DAYS_HISTORY)):
                    created_at = datetime_days_ago(day)
                    if skip_instance and (settings.DAYS_HISTORY - day) <= skip_days:
                        continue
                    if created_at > rds_instcreatetime:
                        playload = {
                            "rds_aws_id": str(uuid.UUID(aid.get("aid"))),
                            "rds_identifier": rds_identifier,
                            "rds_instanceclass": rds_instanceclass,
                            "rds_engine": rds_engine,
                            "rds_inststatus": rds_inststatus,
                            "created_at": created_at.isoformat(),
                            "rds_instcreatetime": rds_instcreatetime.isoformat(),
                            "rds_allocstorage": rds_allocstorage,
                            "rds_paramgroup": rds_paramgroup,
                            "rds_az": rds_az,
                            "rds_enginever": rds_enginever,
                            "rds_lisencemodel": rds_lisencemodel,
                            "rds_copytagsnapshot": rds_copytagsnapshot,
                            "rds_storagetype": rds_storagetype,
                            "rds_multiaz": rds_multiaz,
                            "rds_storageencrypted": rds_storageencrypted,
                            "rds_deleteprotection": rds_deleteprotection,
                            "rds_clusteridentifier": rds_clusteridentifier or "",
                            "rds_masteruser": "admin",
                            "rds_dbinstrole": "Writer",
                            "rds_clusterendpoint": rds_clusterendpoint or "",
                            "rds_endpoint": rds_endpoint,
                            "rds_port": rds_port,
                            "rds_vpc": rds_vpc,
                            "rds_secgroup": rds_secgroup,
                            "rds_subnetgrp": rds_subnetgrp,
                            "rds_subnets": rds_subnets,
                            "rds_backupretention": rds_backupretention,
                            "rds_taglist": rds_taglist  
                        }
                        #print(playload)
                        #for key, value in playload.items():
                        #    print(f"{key}: {value} ({type(value)})")
                        riid=api.post(rds_apiendpoint, playload)
                        mapplayload = {
                            "aws_aid" : str(uuid.UUID(aid.get("aid"))),
                            "rds_riid" : str(uuid.UUID(riid.get("riid"))),
                            "created_at" : created_at.isoformat(),
                            "map_rds_identifier" : rds_identifier,
                            "map_rds_az" : rds_az,
                            "last_collection_at" : 0
                        }
                        #print(mapplayload)
                        raid=api.post(rds_apimapendpoint, mapplayload)
                        for _ in range(random.randint(*settings.PARAMS_PER_RDS)):
                            paramplayload = {
                                "param_type" : "Instance",
                                "param_groupname" : rds_paramgroup ,
                                "param_name": random_param_name(rds_engine),
                                "param_value" :str(random.randint(100, 1000)) ,
                                "param_riid" : str(uuid.UUID(riid.get("riid"))) ,
                                "param_row_created_at" : created_at.isoformat(),                            
                            }
                            rparam=api.post(rds_apiparameter, paramplayload)
                            
                        for _ in range(random.randint(*settings.SEC_RULES_PER_RDS)):
                            secplayload ={
                                "sec_riid" : str(uuid.UUID(riid.get("riid"))) ,
                                "sec_group_name" : random.choice(
                                    ["allow-db", "allow-app", "allow-admin"]
                                ),
                                "sec_gpid" : f"sg-{random.randint(100000,999999)}",
                                #"sec_rule_name" : random.choice(["allow-db", "allow-app", "allow-admin"]),
                                "sec_rule_type" : random.choice(["Inbound", "Outbound"]),
                                "sec_port_range" : "5432-5432" if rds_engine == "postgres" else "3306-3306",
                                "sec_ip_ranges" : random.choice(
                                    ["10.0.0.0/16", "172.16.0.0/12", "0.0.0.0/0"]
                                ),
                            }
                            rsec=api.post(rds_apisecrules, secplayload)
                    else:
                        #print('ignored..')
                        pass
        print(f">>>> Data Seeded for Account [{account_number}]: {regions}")

def random_param_name(engine: str) -> str:
    if engine == "postgres":
        return random.choice([
            "max_connections",
            "work_mem",
            "shared_buffers",
            "log_min_duration_statement",
        ])
    elif engine == "mysql":
        return random.choice([
            "max_connections",
            "innodb_buffer_pool_size",
            "slow_query_log",
        ])
    elif engine.startswith("sqlserver"):
        return random.choice([
            "max degree of parallelism",
            "cost threshold for parallelism",
            "backup compression default",
        ])
    elif engine.startswith("oracle"):
        return random.choice([
            "processes",
            "sessions",
            "open_cursors",
        ])
    return "generic_param"
 
def random_datetime(days_back: int = 90) -> datetime:
    now = (datetime.now(UTC)).replace(tzinfo=None)
    delta_days = random.randint(0, days_back)
    delta_seconds = random.randint(0, 24*60*60 - 1)
    return now - timedelta(days=delta_days, seconds=delta_seconds)

def random_paramgroup(engine_type: str) -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"pg-{engine_type}-{suffix}"

def random_lisencemodel(engine_type: str) -> str:
    if engine_type in ["postgres", "mysql"]:
        return "general-public-license"
    elif engine_type.startswith("oracle") or engine_type.startswith("sqlserver"):
        return random.choice(["license-included", "bring-your-own-license"])
    else:
        return "general-public-license"

def random_cluster_id() -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"cluster-{suffix}"

def random_rdsinst_id() -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"dbdash-rds-{suffix}"

def random_vpc_id() -> str:
    suffix = ''.join(random.choices('0123456789abcdef', k=8))
    return f"vpc-{suffix}"

def random_secgroup_id() -> str:
    suffix = ''.join(random.choices('0123456789abcdef', k=8))
    return f"sg-{suffix}"

def random_secgroup_list(min_count: int = 1, max_count: int = 3) -> str:
    count = random.randint(min_count, max_count)
    return ','.join(random_secgroup_id() for _ in range(count))

def random_subnetgrp() -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"subnetgrp-{suffix}"

def random_subnet_id() -> str:
    suffix = ''.join(random.choices('0123456789abcdef', k=8))
    return f"subnet-{suffix}"

def random_subnet_list(min_count: int = 1, max_count: int = 3) -> str:
    count = random.randint(min_count, max_count)
    return ','.join(random_subnet_id() for _ in range(count))

def random_backup_retention(min_days: int = 7, max_days: int = 30) -> str:
    days = random.randint(min_days, max_days)
    return str(days)

def random_taglist() -> str:
    env = random.choice(["dev", "staging", "prod"])
    owner = random.choice(["platform", "team-a", "team-b"])
    return json.dumps({"env": env, "owner": owner})



""" Testing only """
API_BASE_URL = "http://localhost:8080/api/v1/aws/rds/instance"
API_TOKEN = "API TOKEN"

def seed_rds_instance():
    payload = {
        "rds_aws_id": "17502b18-fe4a-416d-a092-f29658dc613b",
        "rds_identifier": "dbdash-rds-kpib6r",
        "rds_instanceclass": "db.m5.large",
        "rds_engine": "postgres",
        "created_at": datetime.utcnow().isoformat(),
        "rds_instcreatetime": "2025-11-06T06:43:40.227903",
        "rds_allocstorage": "81",
        "rds_paramgroup": "pg-postgres-vrhf",
        "rds_az": "us-west-1b",
        "rds_enginever": "12.15",
        "rds_lisencemodel": "general-public-license",
        "rds_copytagsnapshot": "true",
        "rds_storagetype": "io1",
        "rds_multiaz": "true",
        "rds_storageencrypted": "false",
        "rds_deleteprotection": "false",
        "rds_clusteridentifier": "",
        "rds_masteruser": "admin",
        "rds_dbinstrole": "Writer",
        "rds_clusterendpoint": "",
        "rds_endpoint": "dbdash-rds-kpib6r.rds.amazonaws.com",
        "rds_port": "5432",
        "rds_vpc": "vpc-14be6683",
        "rds_secgroup": "sg-71d87c80,sg-c5e358fa",
        "rds_subnetgrp": "subnetgrp-ko188c",
        "rds_subnets": "subnet-30718901,subnet-ab90fe6a",
        "rds_backupretention": "30",
        "rds_taglist": "{'env': 'dev', 'owner': 'team-a'}"
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    with httpx.Client(timeout=20) as client:
        response = client.post(API_BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        print("RDS instance seeded successfully!")
        print(response.json())

if __name__ == "__main__":
    load_data()
    #seed_rds_instance()
