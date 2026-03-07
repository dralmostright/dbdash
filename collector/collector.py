"""_summary_

Raises:
    RuntimeError: _description_

Returns:
    _type_: _description_
"""
import boto3
from datetime import datetime, UTC
import argparse,os,json,httpx,time, pytz, logging,sys,uuid
from dotenv import load_dotenv
from botocore.exceptions import ClientError, BotoCoreError

"""_summary_

Raises:
    RuntimeError: _description_

Returns:
    _type_: _description_
"""
class Settings:
    def __init__(self, az=None,role_arn=None,aws_account_number=None, api_token=None,account_aid=None,logger=None):
        self.AWS_REGION=az
        self.ROLE_ARN=role_arn
        self.AWS_ACCOUNT_NUMBER=aws_account_number
        self.API_TOKEN=api_token
        self.ACCOUNT_AID=account_aid
        self.logger=logger
        self.RDSAPI_URL = os.getenv("RDSAPI_URL")
        self.RDSMAPAPI_URL = os.getenv("RDSMAPAPI_URL")
        self.RDSPARAMSAPI_URL = os.getenv("RDSPARAMSAPI_URL")
        self.RDSSECRULESAPI_URL = os.getenv("RDSSECRULESAPI_URL")
        self.SNAPSHOT_URL = os.getenv("SNAPSHOT_URL")
        self.SNAPSHOTMAP_URL = os.getenv("SNAPSHOTMAP_URL")
        self.logger.debug(f"AWS_REGION : {self.AWS_REGION}")
        self.logger.debug(f"ROLE_ARN : {self.ROLE_ARN}")
        self.logger.debug(f"AWS_ACCOUNT_NUMBER : {self.AWS_ACCOUNT_NUMBER}")
        self.logger.debug(f"RDSAPI_URL : {self.RDSAPI_URL}")
        self.logger.debug(f"RDSMAPAPI_URL : {self.RDSMAPAPI_URL}")
        self.logger.debug(f"RDSPARAMSAPI_URL : {self.RDSPARAMSAPI_URL}")
        self.logger.debug(f"RDSSECRULESAPI_URL : {self.RDSSECRULESAPI_URL}")
        self.logger.debug(f"RDSSECRULESAPI_URL : {self.SNAPSHOT_URL}")
        self.logger.debug(f"SNAPSHOTMAP_URL : {self.SNAPSHOTMAP_URL}")


"""_summary_

Raises:
    RuntimeError: _description_

Returns:
    _type_: _description_
"""
class APIClient:
    def __init__(self, base_url: str, token: str, logger: logging.Logger):
        self.base_url = base_url
        self.token = token
        self.logger = logger
        self.client = httpx.Client(timeout=20)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        self.logger.debug("POST %s", url)
        try:
            response = self.client.post(url, json=payload, headers=self._headers())
            response.raise_for_status()
            self.logger.debug("POST %s succeeded with status %s", url, response.status_code)
            return response.json()
        except httpx.HTTPError as e:
            self.logger.error("POST %s failed: %s", url, e)
            raise

    def get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        self.logger.debug("GET %s", url)
        try:
            response = self.client.get(url, headers=self._headers())
            response.raise_for_status()
            self.logger.debug("GET %s succeeded with status %s", url, response.status_code)
            return response.json()
        except httpx.HTTPError as e:
            self.logger.error("GET %s failed: %s", url, e)
            raise


"""_summary_

Raises:
    RuntimeError: _description_

Returns:
    _type_: _description_
"""
class AWSRoleSession:
    def __init__(self, role_arn: str, logger: logging.Logger):
        self.role_arn = role_arn
        self.logger = logger

        self.current_account = self._get_current_account_id()
        self.target_account = self._get_account_id_from_role_arn(role_arn)

        if self.current_account == self.target_account:
            self.logger.info(
                "Same AWS account detected. Using instance role credentials."
            )
            self.credentials = None
        else:
            self.logger.info(
                f"Cross-account detected ({self.current_account} → {self.target_account}). Assuming role."
            )
            self.credentials = self._assume_role()

    def _get_current_account_id(self):
        try:
            sts = boto3.client("sts")
            return sts.get_caller_identity()["Account"]
        except Exception as e:
            self.logger.error("Failed to determine current AWS account", exc_info=True)
            raise

    def _get_account_id_from_role_arn(self, role_arn: str):
        return role_arn.split(":")[4]

    def _assume_role(self):
        try:
            sts = boto3.client("sts")
            assumed = sts.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName="CollectorSession"
            )
            return assumed["Credentials"]

        except ClientError as e:
            self.logger.error(
                f"Failed to assume role {self.role_arn}: "
                f"{e.response['Error']['Code']} - {e.response['Error']['Message']}",
                exc_info=True
            )
            raise

    def _client(self, service: str, region: str):
        if self.credentials is None:
            return boto3.client(service, region_name=region)

        return boto3.client(
            service,
            region_name=region,
            aws_access_key_id=self.credentials["AccessKeyId"],
            aws_secret_access_key=self.credentials["SecretAccessKey"],
            aws_session_token=self.credentials["SessionToken"]
        )

    def ec2_client(self, region: str):
        self.logger.debug("Boto client is EC2")
        return self._client("ec2", region)

    def rds_client(self, region: str):
        self.logger.debug("Boto client is RDS")
        return self._client("rds", region)

"""
_summary_
"""
def setup_logger(
    name: str = "DbDash Collector",
    level: int = logging.DEBUG,
    log_file: str | None = None,
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(
            log_file,
            mode="w",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


##
## Parse command-line arguments.
##
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a Python script with a database parameter")
    parser.add_argument('-awsacct', required=True, help="The Aws Account alias in .env")
    parser.add_argument('-resource', required=True, help="The resource for the script is run i.e. rds, snapshot")
    return parser.parse_args()


def get_api_token(username, password, url,logger,max_attempts=5, delay=2):
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
    logger.info(f"Token Endpoint : {url}")
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
                logger.info(f"Login successful on attempt {attempt}!")
                return token
            else:
                logger.error(f"Login attempt {attempt} failed: No token in response.")

        except httpx.HTTPStatusError as e:
            logger.error(f"Login attempt {attempt} failed: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error on attempt {attempt}: {e}")

        if attempt < max_attempts:
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    raise RuntimeError(f"Failed to login after {max_attempts} attempts")

"""_summary_

Returns:
    _type_: _description_
"""
import logging
import uuid
import json
import pytz
from datetime import datetime, UTC
from botocore.exceptions import ClientError, BotoCoreError


class RDSCollector:

    def __init__(self, aws, api, settings, logger: logging.Logger):
        self.aws = aws
        self.api = api
        self.logger = logger
        self.settings = settings

    def collect(self):
        try:
            self.logger.debug(f"Starting collecting RDS metadata for account : {self.settings.AWS_ACCOUNT_NUMBER} Region : {self.settings.AWS_REGION}")
            rds = self.aws.rds_client(self.settings.AWS_REGION)
            response = rds.describe_db_instances()
        except (ClientError, BotoCoreError) as e:
            self.logger.error("Failed to describe RDS instances", exc_info=True)
            return
        except Exception as e:
            self.logger.exception("Unexpected error while initializing RDS collection")
            return
        
        mapresetpayload={"account_aid":self.settings.ACCOUNT_AID}
        self.api.post(f"{self.settings.RDSMAPAPI_URL}/reset/{str(uuid.UUID(self.settings.ACCOUNT_AID))}/{self.settings.AWS_REGION}", mapresetpayload)

        for rdsInst in response.get('DBInstances', []):
            try:
                self.logger.debug(
                    f"Collecting RDS metadata for RDS : {rdsInst.get('DBInstanceIdentifier')}"
                )

                dbclusteridentifier = rdsInst.get('DBClusterIdentifier', "None")

                dbclusterendpoint = 'None'
                dbinstancerole = 'Writer'
                db_cluster_parameter_group = None

                if dbclusteridentifier != 'None':
                    try:
                        clusterendpoint = rds.describe_db_clusters(
                            DBClusterIdentifier=dbclusteridentifier
                        )
                        clusters = clusterendpoint.get('DBClusters', [])
                        if clusters:
                            db_cluster_parameter_group = clusters[0].get(
                                'DBClusterParameterGroup'
                            )
                            for clustMem in clusters:
                                dbclusterendpoint = clustMem.get('Endpoint', 'None')
                                for instance in clustMem.get('DBClusterMembers', []):
                                    if instance.get('DBInstanceIdentifier') == rdsInst.get('DBInstanceIdentifier'):
                                        dbinstancerole = "Writer" if instance.get('IsClusterWriter') else "Reader"
                                        break
                    except (ClientError, BotoCoreError):
                        self.logger.warning(
                            f"Failed to describe DB cluster {dbclusteridentifier}",
                            exc_info=True
                        )

                dbsubnetgroup = rdsInst.get('DBSubnetGroup')
                dbrdssubnetgrp = ''
                subnetsall = ''

                if dbsubnetgroup:
                    dbrdssubnetgrp = dbsubnetgroup.get('DBSubnetGroupName', '')
                    for subnetgs in dbsubnetgroup.get('Subnets', []):
                        subnetsall += ',' + subnetgs.get('SubnetIdentifier', '')

                vpcsecuritygroups = rdsInst.get('VpcSecurityGroups', [])
                securitygp = ''
                for vpcsecuritygp in vpcsecuritygroups:
                    securitygp += ',' + vpcsecuritygp.get('VpcSecurityGroupId', '')

                rdspayload = {
                    "rds_aws_id": str(uuid.UUID(self.settings.ACCOUNT_AID)),
                    "rds_identifier": rdsInst['DBInstanceIdentifier'],
                    "rds_instanceclass": rdsInst['DBInstanceClass'],
                    "rds_engine": rdsInst['Engine'],
                    "rds_inststatus": rdsInst['DBInstanceStatus'],
                    "created_at": (datetime.now(UTC)).astimezone(pytz.timezone('US/Mountain')).replace(tzinfo=None).replace(microsecond=0).isoformat(),
                    "rds_instcreatetime": rdsInst['InstanceCreateTime']
                        .astimezone(pytz.timezone('US/Mountain'))
                        .replace(tzinfo=None, microsecond=0)
                        .isoformat(),
                    "rds_allocstorage": str(rdsInst['AllocatedStorage']),
                    "rds_paramgroup": rdsInst['DBParameterGroups'][0]['DBParameterGroupName'],
                    "rds_az": rdsInst['AvailabilityZone'],
                    "rds_enginever": rdsInst['EngineVersion'],
                    "rds_lisencemodel": rdsInst['LicenseModel'],
                    "rds_copytagsnapshot": str(rdsInst['CopyTagsToSnapshot']),
                    "rds_storagetype": rdsInst['StorageType'],
                    "rds_multiaz": str(rdsInst['MultiAZ']),
                    "rds_storageencrypted": str(rdsInst['StorageEncrypted']),
                    "rds_deleteprotection": str(rdsInst['DeletionProtection']),
                    "rds_clusteridentifier": dbclusteridentifier,
                    "rds_masteruser": rdsInst['MasterUsername'],
                    "rds_dbinstrole": dbinstancerole,
                    "rds_clusterendpoint": dbclusterendpoint,
                    "rds_endpoint": rdsInst['Endpoint']['Address'],
                    "rds_port": str(rdsInst['Endpoint']['Port']),
                    "rds_vpc": dbsubnetgroup.get('VpcId') if dbsubnetgroup else None,
                    "rds_secgroup": securitygp.strip(','),
                    "rds_subnetgrp": dbrdssubnetgrp,
                    "rds_subnets": subnetsall.strip(','),
                    "rds_backupretention": str(rdsInst['BackupRetentionPeriod']),
                    "rds_taglist": json.dumps(rdsInst.get('TagList', []))
                }

                riid = self.api.post(self.settings.RDSAPI_URL, rdspayload)
                self.logger.debug(f"Collecting RDS metadata for RDS : {rdsInst['DBInstanceIdentifier']} completed..")
                self.logger.debug(f"Saving Entries on Mapping..")
                mapplayload = {
                    "aws_aid": str(uuid.UUID(self.settings.ACCOUNT_AID)),
                    "rds_riid": str(uuid.UUID(riid.get("riid"))),
                    "map_rds_identifier": rdsInst['DBInstanceIdentifier'],
                    "map_rds_az": self.settings.AWS_REGION,
                    "created_at": (datetime.now(UTC)).astimezone(pytz.timezone('US/Mountain')).replace(tzinfo=None).replace(microsecond=0).isoformat(),
                    "last_collection_at": 0
                }

                self.api.post(self.settings.RDSMAPAPI_URL, mapplayload)
                self.logger.debug(f"Saving Entries on Mapping successful..")
                self.logger.debug(f"Collecting information for security groups associated with RDS instance..")
                secrules = SecurityCollector(
                    aws=self.aws,
                    vpcsecuritygroups=vpcsecuritygroups,
                    settings=self.settings,
                    riid=riid,
                    api=self.api,
                    logger=self.logger
                )
                secrules.collect()
                self.logger.debug(f"Collecting information for security groups associated with RDS instance successful")

                if dbclusteridentifier != 'None' and db_cluster_parameter_group:
                    self.logger.debug(f"RDS is clustered. Getting Cluster parameters..")
                    ParameterCollector(
                        aws=self.aws,
                        paramname=db_cluster_parameter_group,
                        paramtype="Cluster",
                        settings=self.settings,
                        riid=riid,
                        api=self.api,
                        logger=self.logger
                    ).collect()
                    self.logger.debug(f"RDS is clustered. Getting Cluster parameters completed..")
                self.logger.debug(f"Collecting RDS instance parameters..")
                ParameterCollector(
                    aws=self.aws,
                    paramname=rdsInst['DBParameterGroups'][0]['DBParameterGroupName'],
                    paramtype="Instance",
                    settings=self.settings,
                    riid=riid,
                    api=self.api,
                    logger=self.logger
                ).collect()
                self.logger.debug(f"Collecting RDS instance parameters.. completed..")

                self.logger.debug(
                    f"Collecting All metadata for RDS : {rdsInst['DBInstanceIdentifier']} completed."
                )
            except KeyError as e:
                self.logger.error(
                    f"Missing expected key while processing RDS instance {rdsInst.get('DBInstanceIdentifier')}: {e}",
                    exc_info=True
                )
            except Exception as e:
                self.logger.exception(
                    f"Unexpected error while processing RDS instance {rdsInst.get('DBInstanceIdentifier')}"
                )
        self.logger.debug(f"Collecting RDS metadata completed for account : {self.settings.AWS_ACCOUNT_NUMBER} Region : {self.settings.AWS_REGION}")

    def _now(self):
        tz = pytz.timezone("US/Mountain")
        return datetime.now(tz).replace(microsecond=0).isoformat()

"""
_summary_
"""
class SecurityCollector:

    def __init__(self, aws, vpcsecuritygroups, settings, riid, api, logger: logging.Logger):
        self.aws = aws
        self.api = api
        self.settings = settings
        self.riid = riid
        self.vpcsecuritygroups = vpcsecuritygroups or []
        self.logger = logger

    def collect(self):
        if not self.vpcsecuritygroups:
            self.logger.warning("No VPC security groups found for RDS instance")
            return

        try:
            ec2 = self.aws.ec2_client(self.settings.AWS_REGION)
            sg_ids = [sg["VpcSecurityGroupId"] for sg in self.vpcsecuritygroups]
            self.logger.debug(f"Collecting security rules for SGs: {sg_ids}")

            resp = ec2.describe_security_groups(GroupIds=sg_ids)

        except (ClientError, BotoCoreError):
            self.logger.error("Failed to describe security groups", exc_info=True)
            return
        except Exception:
            self.logger.exception("Unexpected error while initializing SecurityCollector")
            return

        for sg in resp.get("SecurityGroups", []):
            try:
                self.logger.debug(
                    f"Processing security group {sg.get('GroupName')} ({sg.get('GroupId')})"
                )
                ##
                ## Inbound rules
                ##
                for rule in sg.get("IpPermissions", []):
                    for ip in rule.get("IpRanges", []):
                        try:
                            secplayload = {
                                "sec_riid": str(uuid.UUID(self.riid.get("riid"))),
                                "sec_group_name": sg.get('GroupName'),
                                "sec_gpid": sg.get('GroupId'),
                                "sec_rule_type": "Inbound",
                                "sec_port_range": (
                                    f"{rule.get('FromPort')} - {rule.get('ToPort')}"
                                    if all(k in rule for k in ("FromPort", "ToPort"))
                                    else "-"
                                ),
                                "sec_ip_ranges": ip.get('CidrIp')
                            }

                            self.api.post(
                                self.settings.RDSSECRULESAPI_URL,
                                secplayload
                            )

                        except Exception:
                            self.logger.exception(
                                f"Failed to save inbound rule for SG {sg.get('GroupId')}"
                            )
                ##
                ## Outbound rules
                ##
                for rule in sg.get("IpPermissionsEgress", []):
                    for ip in rule.get("IpRanges", []):
                        try:
                            secplayload = {
                                "sec_riid": str(uuid.UUID(self.riid.get("riid"))),
                                "sec_group_name": sg.get('GroupName'),
                                "sec_gpid": sg.get('GroupId'),
                                "sec_rule_type": "Outbound",
                                "sec_port_range": (
                                    f"{rule.get('FromPort')} - {rule.get('ToPort')}"
                                    if all(k in rule for k in ("FromPort", "ToPort"))
                                    else "-"
                                ),
                                "sec_ip_ranges": ip.get('CidrIp')
                            }

                            self.api.post(
                                self.settings.RDSSECRULESAPI_URL,
                                secplayload
                            )

                        except Exception:
                            self.logger.exception(
                                f"Failed to save outbound rule for SG {sg.get('GroupId')}"
                            )

                self.logger.debug(
                    f"Security rules collection completed for SG {sg.get('GroupId')}"
                )

            except KeyError as e:
                self.logger.error(
                    f"Missing expected key in security group data: {e}",
                    exc_info=True
                )
            except Exception:
                self.logger.exception(
                    f"Unexpected error while processing security group {sg.get('GroupId')}"
                )

"""_summary_
"""
class ParameterCollector:

    def __init__(self, aws, api, settings, paramname, paramtype, riid, logger: logging.Logger):
        self.aws = aws
        self.api = api
        self.settings = settings
        self.riid = riid
        self.paramname = paramname
        self.paramtype = paramtype
        self.logger = logger

    def collect(self):
        try:
            rds = self.aws.rds_client(self.settings.AWS_REGION)

            paginator = (
                rds.get_paginator("describe_db_cluster_parameters")
                if self.paramtype == "Cluster"
                else rds.get_paginator("describe_db_parameters")
            )

            list_args = (
                {"DBClusterParameterGroupName": self.paramname}
                if self.paramtype == "Cluster"
                else {"DBParameterGroupName": self.paramname}
            )

            self.logger.debug(
                f"Collecting {self.paramtype} parameters for parameter group: {self.paramname}"
            )

        except (ClientError, BotoCoreError):
            self.logger.error(
                f"Failed to initialize paginator for parameter group {self.paramname}",
                exc_info=True
            )
            return
        except Exception:
            self.logger.exception(
                f"Unexpected error initializing ParameterCollector for {self.paramname}"
            )
            return

        try:
            for page in paginator.paginate(**list_args):
                for param in page.get("Parameters", []):
                    if param.get("Source") != "user":
                        continue

                    try:
                        payload = {
                            "param_riid": str(uuid.UUID(self.riid.get("riid"))),
                            "param_groupname": self.paramname,
                            "param_type": self.paramtype,
                            "param_name": param.get("ParameterName"),
                            "param_value": param.get("ParameterValue"),
                            "param_row_created_at": (
                                datetime.now(UTC)
                                .astimezone(pytz.timezone('US/Mountain'))
                                .replace(tzinfo=None, microsecond=0)
                                .isoformat()
                            )
                        }

                        self.api.post(
                            self.settings.RDSPARAMSAPI_URL,
                            payload
                        )

                    except KeyError as e:
                        self.logger.error(
                            f"Missing expected key in parameter data: {e}",
                            exc_info=True
                        )
                    except Exception:
                        self.logger.exception(
                            f"Failed to save parameter {param.get('ParameterName')} "
                            f"for group {self.paramname}"
                        )

            self.logger.debug(
                f"Parameter collection completed for {self.paramtype} group: {self.paramname}"
            )

        except (ClientError, BotoCoreError):
            self.logger.error(
                f"AWS error while paginating parameters for {self.paramname}",
                exc_info=True
            )
        except Exception:
            self.logger.exception(
                f"Unexpected error during parameter pagination for {self.paramname}"
            )


class SnapshotCollector:

    def __init__(self, aws, api, settings, logger: logging.Logger):
        self.aws = aws
        self.api = api
        self.logger = logger
        self.settings = settings

    def collect(self):
        self.logger.debug(f"Starting collecting RDS metadata for account : {self.settings.AWS_ACCOUNT_NUMBER} Region : {self.settings.AWS_REGION}")
        self._collect_clus()
        self._collect_inst()
        self.logger.debug(f"Collecting RDS metadata completed for account : {self.settings.AWS_ACCOUNT_NUMBER} Region : {self.settings.AWS_REGION}")

    def _now(self):
        tz = pytz.timezone("US/Mountain")
        return datetime.now(tz).replace(microsecond=0).isoformat()

    def _collect_inst(self):

        try:
            self.logger.debug(f"Starting collecting RDS Snapshot for account : {self.settings.AWS_ACCOUNT_NUMBER} Region : {self.settings.AWS_REGION}")
            rds = self.aws.rds_client(self.settings.AWS_REGION)
            paginator = rds.get_paginator("describe_db_snapshots")
        except (ClientError, BotoCoreError) as e:
            self.logger.error("Failed to describe RDS instances", exc_info=True)
            return
        except Exception as e:
            self.logger.exception("Unexpected error while initializing RDS collection")
            return

        try:
            for page in paginator.paginate():
                for snapshot in page.get("DBSnapshots", []):
                    snappayload = {
                        "snap_aws_id" : str(uuid.UUID(self.settings.ACCOUNT_AID)),
                        "snap_identifier": snapshot.get("DBSnapshotIdentifier"),
                        "snap_rds_identifier": snapshot.get("DBInstanceIdentifier"),
                        "snap_type": snapshot.get("SnapshotType"),
                        "snap_inst_type" : "instance",
                        "snap_status": snapshot.get("Status"),
                        "snap_created_time": (
                            snapshot['SnapshotCreateTime']
                            .astimezone(pytz.timezone('US/Mountain'))
                            .replace(tzinfo=None, microsecond=0)
                            .isoformat()
                        ),
                        "snap_engine": snapshot.get("Engine"),
                        "snap_allocated_storage": str(snapshot.get("AllocatedStorage")),
                        "snap_az": snapshot.get("AvailabilityZone"),
                        "snap_region" : self.settings.AWS_REGION,
                        "snap_engine_ver": snapshot.get("EngineVersion"),
                        "snap_progress": str(snapshot.get("PercentProgress")),
                        "snap_ipos": str(snapshot.get("Iops")),
                        "snap_throughtput": str(snapshot.get("StorageThroughput")),
                        "snap_taglist": json.dumps(snapshot.get('TagList', [])),
                        "snap_arn": snapshot.get("DBSnapshotArn"),
                        "snap_srcregion": snapshot.get("SourceRegion"),
                        "snap_srcidentifier": snapshot.get("SourceDBSnapshotIdentifier"),
                        "snap_row_created_at": (
                            datetime.now(UTC)
                            .astimezone(pytz.timezone('US/Mountain'))
                            .replace(tzinfo=None, microsecond=0)
                            .isoformat()
                        )
                    }
                    #print(snappayload)
                    snap = self.api.post(
                        self.settings.SNAPSHOT_URL,
                        snappayload
                    )
                    snapmappayload = {
                    "sar_aws_aid": str(uuid.UUID(self.settings.ACCOUNT_AID)),
                    "sar_snap_id": str(uuid.UUID(snap.get("snap_id"))),
                    "sar_snap_identifier": snapshot.get("DBSnapshotIdentifier"),
                    "sar_rds_az": self.settings.AWS_REGION,
                    "sar_created_at": (datetime.now(UTC)).astimezone(pytz.timezone('US/Mountain')).replace(tzinfo=None).replace(microsecond=0).isoformat(),
                    "sar_last_collection_at": (datetime.now(UTC)).astimezone(pytz.timezone('US/Mountain')).replace(tzinfo=None).replace(microsecond=0).isoformat()
                    }
                    #print(snapmappayload)
                    self.api.post(self.settings.SNAPSHOTMAP_URL, snapmappayload)
        except ClientError as e:
            print(f"Error in region : {e}")

    def _collect_clus(self):

        try:
            self.logger.debug(f"Starting collecting RDS Cluster snapshot for account : {self.settings.AWS_ACCOUNT_NUMBER} Region : {self.settings.AWS_REGION}")
            rds = self.aws.rds_client(self.settings.AWS_REGION)
            paginator = rds.get_paginator("describe_db_cluster_snapshots")
        except (ClientError, BotoCoreError) as e:
            self.logger.error("Failed to describe RDS instances", exc_info=True)
            return
        except Exception as e:
            self.logger.exception("Unexpected error while initializing RDS collection")
            return

        try:
            for page in paginator.paginate():
                for snapshot in page.get("DBClusterSnapshots", []):
                    snappayload = {
                        "snap_aws_id" : str(uuid.UUID(self.settings.ACCOUNT_AID)),
                        "snap_identifier": snapshot.get("DBClusterSnapshotIdentifier"),
                        "snap_rds_identifier": snapshot.get("DBClusterIdentifier"),
                        "snap_type": snapshot.get("SnapshotType"),
                        "snap_inst_type" : "instance",
                        "snap_status": snapshot.get("Status"),
                        "snap_created_time": (
                            snapshot['SnapshotCreateTime']
                            .astimezone(pytz.timezone('US/Mountain'))
                            .replace(tzinfo=None, microsecond=0)
                            .isoformat()
                        ),
                        "snap_engine": snapshot.get("Engine"),
                        "snap_allocated_storage": str(snapshot.get("AllocatedStorage")),
                        "snap_az": snapshot.get("AvailabilityZone"),
                        "snap_region" : self.settings.AWS_REGION,
                        "snap_engine_ver": snapshot.get("EngineVersion"),
                        "snap_progress": str(snapshot.get("PercentProgress")),
                        "snap_ipos": str(snapshot.get("Iops")),
                        "snap_throughtput": str(snapshot.get("StorageThroughput")),
                        "snap_taglist": json.dumps(snapshot.get('TagList', [])),
                        "snap_arn": snapshot.get("DBSnapshotArn"),
                        "snap_srcregion": snapshot.get("SourceRegion"),
                        "snap_srcidentifier": snapshot.get("SourceDBSnapshotIdentifier"),
                        "snap_row_created_at": (
                            datetime.now(UTC)
                            .astimezone(pytz.timezone('US/Mountain'))
                            .replace(tzinfo=None, microsecond=0)
                            .isoformat()
                        )
                    }
                    #print(snappayload)
                    snap = self.api.post(
                        self.settings.SNAPSHOT_URL,
                        snappayload
                    )
                    snapmappayload = {
                    "sar_aws_aid": str(uuid.UUID(self.settings.ACCOUNT_AID)),
                    "sar_snap_id": str(uuid.UUID(snap.get("snap_id"))),
                    "sar_snap_identifier": snapshot.get("DBClusterSnapshotIdentifier"),
                    "sar_rds_az": self.settings.AWS_REGION,
                    "sar_created_at": (datetime.now(UTC)).astimezone(pytz.timezone('US/Mountain')).replace(tzinfo=None).replace(microsecond=0).isoformat(),
                    "sar_last_collection_at": (datetime.now(UTC)).astimezone(pytz.timezone('US/Mountain')).replace(tzinfo=None).replace(microsecond=0).isoformat()
                    }
                    #print(snapmappayload)
                    self.api.post(self.settings.SNAPSHOTMAP_URL, snapmappayload)
        except ClientError as e:
            print(f"Error in region : {e}")


def main():
    load_dotenv(override=True)

    args = parse_arguments()
    rdsacct = args.awsacct
    resource = args.resource
    awsRoleArn = os.getenv(rdsacct)
    result = awsRoleArn.split(":")
    API_USERNAME = os.getenv("API_USERNAME")
    API_PASSWORD = os.getenv("API_PASSWORD")
    API_TOKEN_URL = os.getenv("API_TOKEN_URL")
    API_BASE_URL = os.getenv("API_BASE_URL")
    log_file=f"collector_{rdsacct}_{resource}.log"
    logger = setup_logger(
        level=logging.DEBUG,
        log_file=log_file
    )
    logger.info("Starting RDS collection job")
    logger.info(f"Account : {rdsacct}")
    logger.info(f"Api Username : {API_USERNAME}")
    logger.info(f"Api Baseurl : {API_BASE_URL}")
    logger.info(f"Validating Credentails to get token ")
    token=get_api_token(API_USERNAME,API_PASSWORD,API_TOKEN_URL,logger)
    endpoint= f"/aws/org/byaccount?account_number={result[4]}"
    api = APIClient(base_url=API_BASE_URL, token=token, logger=logger)
    azs = api.get(endpoint)
    aid = azs.get("aid")
    logger.info(f"Initializing Configuration Parameters")
    for az in azs.get("account_az").split(","):
        settings = Settings(az=az, role_arn=awsRoleArn,aws_account_number=result[4],api_token=token,account_aid=aid, logger=logger)
        aws = AWSRoleSession(role_arn=settings.ROLE_ARN, logger=logger)
        if resource == "rds":
            rds = RDSCollector(aws=aws,api=api,settings=settings,logger=logger)
            rds.collect()
        else:
            SnapshotCollector(aws, api, settings, logger).collect()



##
## Start execution of the script
##
if __name__ == "__main__":
    main()
