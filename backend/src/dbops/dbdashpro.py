##
## Developed By : Suman Adhikari
##
## Developed Date :
##
## Description : 


## This script is used provision database in MSSQL
## It uses values provided on basis of .env file hences it needs to be corredt
## It can be run in two modes : dry and exec
##
## Version : v2
## Required Packages:
## pyodbc==5.2.0
## python-dotenv==1.0.1 
##
## Modified by :
##
## Modified Date :
##
## Modified Description :
##
##
## This script is meant to be run by automation job only and should not be exected on its own.
##
import pyodbc, os, argparse,sys, socket, json,subprocess, time
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# ============================================================
# Pass Job Arguments
# ============================================================
def parse_arguments():
    parser = argparse.ArgumentParser(description="Python script for DbDash Automation..")
    parser.add_argument('-job_id', required=True, help="The Job id by which the script can pull metadata")
    return parser.parse_args()


# ============================================================
# Custom Exceptions
# ============================================================

class CustomerAlreadyExists(Exception):
    def __init__(self, message="Database or Configuration already exists."):
        super().__init__(message)

class IncompleteVariables(Exception):
    def __init__(self, message="Required Values cannot be retrived."):
        super().__init__(message)

class DirPathDoesnotExists(Exception):
    def __init__(self, message="Directory Doesn't Exists or is not accessible."):
        super().__init__(message)

class DirPathNotEmpty(Exception):
    def __init__(self, message="Directory is not empty."):
        super().__init__(message)

class SomethingWentWrong(Exception):
    def __init__(self, message="Error Occurred."):
        super().__init__(message)
        
class JobNotFound(Exception):
    def __init__(self, message="Automation was not able to find the job."):
        super().__init__(message)
        
class JobPayLoadInValid(Exception):
    def __init__(self, message="Payload to Automation is not valid."):
        super().__init__(message)

class MetaDataAlreadyExists(Exception):
    def __init__(self, message="Metadata Already Exists on PLMADMINDB."):
        super().__init__(message)


# ============================================================
# Database Logger
# ============================================================

class DBLogger:
    def __init__(self, conn, job_id, runmode):
        self.conn = conn
        self.job_id = job_id
        self.runmode = runmode

    def log(
        self,
        status,
        module,
        msg,
        *,
        job_status=None,
        job_progress=None,
        job_step=None
    ):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO dbo.execlog
                (exec_user, exec_job_id, exec_module, exec_action,exec_status,exec_detail, exec_remotepull)
            VALUES ('DbDashAuto', ?, ?, ?,?, ?, 'N')
            """,
            self.job_id,
            module,
            self.runmode,
            status,
            msg
        )

        update_cols = []
        params = []

        if job_progress is not None:
            update_cols.append("job_progress = ?")
            params.append(job_progress)

        if job_status is not None:
            update_cols.append("job_status = ?")
            params.append(job_status)

        if job_step is not None:
            update_cols.append("job_current_step = ?")
            params.append(job_step)

        if update_cols:
            update_sql = f"""
                UPDATE dbo.execjob
                SET {", ".join(update_cols)},
                    job_updated_at = GETDATE()
                WHERE job_api_job_id = ?
            """
            params.append(self.job_id)
            cursor.execute(update_sql, params)

        self.conn.commit()

    def info(self, module, msg, **kwargs):
        takerest()
        self.log("INFO",module, msg, **kwargs)

    def error(self, module, msg, **kwargs):
        takerest()
        self.log( "ERROR",module, msg, **kwargs)

    def end(self, module, msg, **kwargs):
        self.log("SUCCESS",module, msg, **kwargs)

# ============================================================
# DB Connection Manager
# ============================================================

class DBConnectionManager:
    def __init__(self, server, database, user, password, port):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None

    def connect(self):
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={self.server},{self.port};DATABASE={self.database};"
            f"UID={self.user};PWD={self.password}"
        )
        print(f"{self.server} {self.database} {self.user} {self.password} {self.password}")
        print(conn_str)
        self.conn = pyodbc.connect(conn_str)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

# ============================================================
# Job Metadata Loader
# ============================================================

class ExecJobLoader:
    def __init__(self, conn, job_id, logger):
        self.conn = conn
        self.job_id = job_id
        self.logger = logger

    def load(self):
        self.logger.info("Validating", f"Fetching execjob payload for job_api_job_id={self.job_id}", job_status="VALIDATING", job_step="VALIDATING JOB")
        cursor = self.conn.cursor()
        """
        cursor.execute(
            "SELECT job_parameters FROM dbo.execjob WHERE job_api_job_id = ? and ",
            self.job_id
        )        
        """
        
        cursor.execute(
            "SELECT job_parameters FROM dbo.execjob WHERE job_api_job_id = ?",
            self.job_id
        )

        row = cursor.fetchone()
        if not row:
            self.logger.error(
                    "Failed", f"Validating failed | Mode={self.runmode} | job entry not found",job_status="FAILED", job_step="VALIDATING JOB"
            )
            raise JobPayLoadInValid
        try:
            payload = json.loads(row[0])

        except json.JSONDecodeError as e:
            self.logger.error(
                    "Failed", f"Validating failed | Mode={self.runmode} | job entry not found",job_status="FAILED", job_step="VALIDATING JOB"
            )            
            raise JobPayLoadInValid

        self._validate(payload)
        self.logger.info("Validating",f"Fetching & validating payload for job_api_job_id={self.job_id} completed.", job_status="VALIDATING", job_step="VALIDATION_PAYLOAD")        
        return payload

    
    def _validate(self, payload):
        required = [
            "job_api_job_id",
            "job_mode",
            "num_sites",
            "num_desktops",
            "num_mobiles",
            "target_db_name",
            "source_db_name",
            "company_name",
            "data_dir",
            "log_dir"
        ]
        missing = [k for k in required if k not in payload]
        if missing:
            self.logger.error(
                    "Failed", f"Validating failed | Mode={self.runmode} | job entry not found",job_status="FAILED", job_step="VALIDATING JOB"
            )               
            raise JobPayLoadInValid

# ============================================================
# Database Provisioner
# ============================================================

class DatabaseProvisioner:
    def __init__(self, jobpayload, logger):
        self.server = socket.gethostname()
        self.jobpayload = jobpayload
        self.logger = logger

        self.runmode = jobpayload["job_mode"].lower()
        self.target_db = jobpayload["target_db_name"]
        self.source_db = jobpayload["source_db_name"]          
        self.data_dir = jobpayload["data_dir"]
        self.log_dir = jobpayload["log_dir"]

        self.db_host = os.getenv(f"{self.server}_PROVISION_HOSTIP")
        self.db_user = os.getenv(f"{self.server}_PROVISION_USER")
        self.db_pwd = os.getenv(f"{self.server}_PROVISION_PASSWORD")
        self.db_port = os.getenv(f"{self.server}_PROVISION_PORT")
        self.backupdir = ""
        self.app_type =""
        self.app_base_url = ""
        #self.server='SQLP01'

        if not all([self.db_host, self.db_user, self.db_pwd]):
            raise IncompleteVariables("Missing DB connection info in .env")
        
        if self.source_db =='RESTOPROSMASTERDB':
            self.backupdir = r"\\sqlp02\RedGate_SQLBACKUP\SQLP03\RESTOPROSMASTERDB"
            self.app_type = os.getenv("META_RMTYPE")
            self.app_base_url = os.getenv("META_RMBASEURL")
        elif self.source_db == "RMMASTERDB":
            self.backupdir = r"\\sqlp02\RedGate_SQLBACKUP\SQLP03\MASTERRMDB"
            self.app_type = os.getenv("META_RMTYPE")
            self.app_base_url = os.getenv("META_RMBASEURL")  
            self.source_db = "MASTERRMDB"           
        else:
            self.backupdir = ""
            self.app_type = os.getenv("META_PLMTYPE")
            self.app_base_url = os.getenv("META_PLMBASEURL")
            
    def _connect_master(self):
        return DBConnectionManager(
            self.db_host,
            "master",
            self.db_user,
            self.db_pwd,
            self.db_port
        ).connect()

    def provision(self):
        self.logger.info(
            "Provisioning", f"Provisioning start | Mode={self.runmode} | DB={self.target_db}",job_status="PROVISIONING", job_step="VALIDATING INPUTS"
        )
        self.check_db_exists()
        self.checkBackupLocation(self.backupdir)
        self.checkIfCustomerExists()
        self.getTopfilesList(self.backupdir)
        self.createDBFLocation(self.data_dir)
        self.createDBFLocation(self.log_dir)
        self.restore_database()
        self.post_provision_step()
        self.remapLogicalName()
        self.backupDatabase()
        self.logger.info("Provisioning Completed", f"Provisioning Completed | Mode={self.runmode} | Updating client database tables.",job_status="COMPLETED", job_step="COMPLETED")
        #self.logger.info("Provisioning completed successfully")

    def check_db_exists(self):
        conn = self._connect_master()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sys.databases WHERE name = ?",
            self.target_db
        )
        if cursor.fetchone():
            self.logger.error(
                "Provisioning", f"Provisioning failed | Mode={self.runmode} | DB={self.target_db} exists.",job_status="FAILED", job_step="VALIDATING DBNAME"
            )  
            conn.close()            
            raise CustomerAlreadyExists(
                f"Database {self.target_db} already exists."
            )

        self.logger.info(
            "Provisioning", f"Provisioning checks completed | Mode={self.runmode} | DB={self.target_db} doesn't exists.",job_status="PROVISIONING", job_step="VALIDATING DBNAME"
        )        
        conn.close()

    def checkBackupLocation(self, os_path):
        try:
            if os.path.isdir(os_path):
                self.logger.info(
                    "Provisioning", f"Provisioning checks completed | Mode={self.runmode} | path={os_path} exists",job_status="PROVISIONING", job_step="VALIDATING BACKUP DIR"
                )

            else:
                self.logger.error(
                    "Provisioning", f"Provisioning failed | Mode={self.runmode} | path={os_path} doesn't exists",job_status="FAILED", job_step="VALIDATING BACKUP DIR"
                )
                raise DirPathDoesnotExists
            
        except Exception as e:
            self.logger.error(
                    "Provisioning", f"Provisioning failed | Mode={self.runmode} | path={os_path} doesn't exists",job_status="FAILED", job_step="VALIDATING BACKUP DIR"
            )
            raise DirPathDoesnotExists

    def getTopfilesList(self, os_path):
        try:
            self.logger.info(
                    "Provisioning", f"Provisioning checks | Mode={self.runmode} | path={os_path} exists",job_status="PROVISIONING", job_step="GETTING TOP 5 NEWEST FILES"
            )
            cmd = ["powershell","-Command",f"Get-ChildItem '{os_path}' | Sort-Object LastWriteTime -Descending | Select-Object -First 5"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.logger.info(
                    "Provisioning", f"{result.stdout}",job_status="PROVISIONING", job_step="GETTING TOP 5 NEWEST FILES"
            )            
        except Exception as e:
            self.logger.error(
                    "Provisioning", f"Provisioning failed | Mode={self.runmode} | viewing file from path path={os_path}",job_status="FAILED", job_step="VALIDATING BACKUP DIR"
            )
            raise DirPathDoesnotExists

    def checkIfCustomerExists(self):
        try:
            self.logger.info(
                    "Provisioning", f"Provisioning checks | Mode={self.runmode} | checking if customer already exists",job_status="PROVISIONING", job_step="CHECKING IF CUSTOMER EXISTS"
            )             
            meta_conn = DBConnectionManager(
                os.getenv("META_SERVER"),
                os.getenv("META_DATABASE"),
                os.getenv("META_USER"),
                os.getenv("META_PASSWORD"),
                os.getenv("META_PORT")
            ).connect()
            cursor = meta_conn.cursor()
            cursor.execute(
                "SELECT Customer_ID FROM dbo.Customers WHERE CustomerCode = ? ",
                self.target_db
            )

            if cursor.fetchone():
                self.logger.error(
                         "Provisioning", f"Provisioning checks | Mode={self.runmode} | Metadata found on PLMADMIN tables",job_status="FAILED", job_step="CHECKING IF CUSTOMER EXISTS"
                ) 
                raise MetaDataAlreadyExists

            cursor.execute(
                "SELECT Customer_ID FROM dbo.tblAuth WHERE DB_NAME = ? ",
                self.target_db
            )

            if cursor.fetchone():
                self.logger.error(
                         "Provisioning", f"Provisioning checks | Mode={self.runmode} | Metadata found on PLMADMIN tables",job_status="FAILED", job_step="CHECKING IF CUSTOMER EXISTS"
                ) 
                raise MetaDataAlreadyExists
                
            self.logger.info(
                     "Provisioning", f"Provisioning checks | Mode={self.runmode} | checking if customer already exists - Passed",job_status="PROVISIONING", job_step="CHECKING IF CUSTOMER EXISTS"
            ) 
            meta_conn.close()
        except Exception as e:
                print(e)
                meta_conn.close()
                self.logger.error(
                         "Provisioning", f"Provisioning checks | Mode={self.runmode} | checking if customer already exists",job_status="FAILED", job_step="CHECKING IF CUSTOMER EXISTS"
                ) 
                raise MetaDataAlreadyExists      

    def createDBFLocation(self,loc):
            try:
                self.logger.info(
                        "Provisioning", f"Provisioning checks | Mode={self.runmode} | checking if directory {loc} exists",job_status="PROVISIONING", job_step="CHECKING DIRECTORIES"
                )                 
                directory=os.path.join(loc,self.target_db)
                dirpath=Path(directory)
                if os.path.isdir(directory):
                    self.logger.info(
                            "Provisioning", f"Provisioning checks | Mode={self.runmode} | Directory {loc} exists",job_status="PROVISIONING", job_step="CHECKING DIRECTORIES"
                    )  
                    if any(f.is_file() for f in dirpath.iterdir()):
                        self.logger.error(
                                "Provisioning", f"Provisioning checks | Mode={self.runmode} | Directory {loc} exists and is not empty",job_status="FAILED", job_step="CHECKING DIRECTORIES"
                        ) 
                        raise DirPathNotEmpty(f"{directory} is not empty")
                else:
                    if self.runmode == 'dry':
                        self.logger.info(
                                "Provisioning", f"Provisioning checks | Mode={self.runmode} | checking if directory {loc} skipped.",job_status="PROVISIONING", job_step="CHECKING DIRECTORIES"
                        )  
                    else:
                        dirpath.mkdir(parents=True, exist_ok=True)
                        self.logger.info(
                                "Provisioning", f"Provisioning checks | Mode={self.runmode} | Directory {loc} didn't exits and is created.",job_status="PROVISIONING", job_step="CHECKING DIRECTORIES"
                        ) 
            except Exception as e:
                    self.logger.error(
                                "Provisioning", f"Provisioning checks | Mode={self.runmode} | Something went wrong for dir : {loc}.",job_status="FAILED", job_step="CHECKING DIRECTORIES"
                    ) 
                    raise SomethingWentWrong
                    
    def checkErros(self, rows, error):
        try:
            if rows:
                self.logger.info(
                    "Validating", f"Validating | Mode={self.runmode} | Validating restore log.",job_status="VALIDATING", job_step="VALIDATING RESTORE"
                    ) 
                for row in rows:
                    if str(row) == "(' ',)":
                        continue
                    rrow=str(tuple(str(item).rstrip() if isinstance(item, str) else item for item in row))
                    self.logger.info(
                                "Validating", f"Validating | Mode={self.runmode} | {rrow}"
                    ) 
                    if error.lower() in rrow.lower():
                        self.logger.error(
                                    "Validating", f"Validation error restore failed | Mode={self.runmode} | {rrow}.",job_status="FAILED", job_step="VALIDATING RESTORE"
                        ) 
                        raise SomethingWentWrong

        except Exception as e:
            self.logger.error(
                "Validating", f"Validation error | Mode={self.runmode} | Something went wrong during validation.",job_status="FAILED", job_step="VALIDATING RESTORE"
            ) 
            raise SomethingWentWrong

    def restore_database(self):
        try:
            self.logger.info(
                "Provisioning", f"Provisioning checks | Mode={self.runmode} | Creating Restore Command.",job_status="PROVISIONING", job_step="RESTORING"
            ) 
            restore_sql = (
                "EXECUTE master..sqlbackup N'-SQL \""
                f"RESTORE DATABASE [{self.target_db}] "
                f"FROM DISK = ''{self.backupdir}\\*{self.source_db}*.sqb'' "
                f"SOURCE=[{self.source_db}] LATEST_ALL WITH RECOVERY, "
                f"MOVE ''{self.source_db}_Data'' "
                f"TO ''{self.data_dir}\\{self.target_db}\\{self.target_db}_data.mdf'', "
                f"MOVE ''{self.source_db}_Log'' "
                f"TO ''{self.log_dir}\\{self.target_db}\\{self.target_db}_log.ldf''"
                "\"'"
            )
            self.logger.info(
                "Provisioning", f"Provisioning checks | Mode={self.runmode} | {restore_sql}.",job_status="PROVISIONING", job_step="RESTORING"
            ) 

            if self.runmode == "dry":
                self.logger.info(
                    "Provisioning", f"Provisioning checks | Mode={self.runmode} | restore skipped.",job_status="PROVISIONING", job_step="RESTORING - DRY"
                ) 
                return
            
            self.logger.info(
                    "Provisioning", f"Provisioning checks | Mode={self.runmode} | Starting Restore.",job_status="PROVISIONING", job_step="RESTORING"
                ) 
            conn = self._connect_master()
            cursor = conn.cursor()
            cursor.execute(restore_sql)
            rows = cursor.fetchall()
            self.checkErros(rows, 'Error')
            conn.close()
            takerest()
            self.logger.info(
                    "Validating", f"Validating checks | Mode={self.runmode} | Restore completed.",job_status="PROVISIONING", job_step="RESTORING"
                ) 
            takerest()
        except Exception as e:
            self.logger.error(
                "Provisioning", f"Provisioning error | Mode={self.runmode} | Something went wrong during restore.",job_status="FAILED", job_step="RESTORING"
            ) 
            raise SomethingWentWrong
        
    def autoFixUsers(db, conn):
        query=f"EXEC sp_change_users_login 'Auto_Fix', '{db}'"
        #logging.info(f"Fixing Orphan users for the database {db}")
        #execNonTranQ(conn, query)
        #logging.info(f"Fixing Orphan users for the database {db} completed.")

    def backupDatabase(self):
        try:
            conn = self._connect_master()
            cursor = conn.cursor()
            query = "EXECUTE master..sqlbackup N'-SQL "
            query = query + '"' + f"Backup DATABASE [{self.target_db}] TO DISK = ''\\\\SQLP02\\RedGate_SQLBACKUP\\{self.server}\\<database>\\<AUTO>.sqb'' "
            query = query + f"WITH ERASEFILES_PRIMARY = 30, MAILTO_ONERROR = ''sadhikari@verisk.com''"
            query = query + f", CHECKSUM, DISKRETRYINTERVAL = 30, DISKRETRYCOUNT = 10, THREADCOUNT = 8, COPYTO_HOSTED, HOSTED_FOLDER = ''PROD-BACKUP/{self.server}/<database>''" + '"' + "'"
            cursor.execute(query)
            rows = cursor.fetchall() 
            #rows=executeQueryOn(conn, query)
            #printRows(rows)
            self.checkErros(rows, 'Error')
            
        except Exception as e:
            self.logger.info(
                    "Provisioning", f"Taking full backup | Mode={self.runmode} | Failed.",job_status="FAILED", job_step="TAKING FULL BACKUP - FAILED"
            )             
            print(e)
            cursor.close()
            conn.close()
            raise SomethingWentWrong

    def remapLogicalName(self):
        query = f"SELECT d.name, mf.name, mf.type_desc from sys.databases d join sys.master_files mf ON mf.database_id = d.database_id where d.name = '{self.target_db}'"
        try:
            if self.runmode == "dry":
                self.logger.info(
                    "Provisioning", f"Provisioning checks | Mode={self.runmode} | Mapping of logical filename skipped.",job_status="PROVISIONING", job_step="REMAPPING LOGICAL - DRY"
                ) 
                return
            else:
                conn = self._connect_master()
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()                
                for row in rows:
                    conn.autocommit = True
                    rrow=tuple(str(item).rstrip() if isinstance(item, str) else item for item in row)
                    self.logger.info(
                        "Provisioning", f"Mapping Logical filename | Mode={self.runmode} | {rrow}.",job_status="PROVISIONING", job_step="REMAPPING LOGICAL"
                    )                     
                    if row[2] == 'ROWS':
                        chgdbf=f"ALTER DATABASE [{self.target_db}] MODIFY FILE (NAME = N'{row[1]}', NEWNAME = N'{self.target_db}_Data');"
                        cursor.execute(chgdbf)
                        #cursor.fetchall() 
                    else:
                        chgldf=f"ALTER DATABASE [{self.target_db}] MODIFY FILE (NAME = N'{row[1]}', NEWNAME = N'{self.target_db}_Log');"
                        cursor.execute(chgldf)
                        #cursor.fetchall() 
                    conn.autocommit=False
            
                cursor.execute(query)
                lrows = cursor.fetchall()
                for row in lrows:
                    rrow=tuple(str(item).rstrip() if isinstance(item, str) else item for item in row)
                    self.logger.info(
                        "Provisioning", f"Mapping Logical filename | Mode={self.runmode} | {rrow}.",job_status="PROVISIONING", job_step="REMAPPING LOGICAL"
                    )                     
                
        except Exception as e:
            self.logger.info(
                    "Provisioning", f"Mapping Logical filename | Mode={self.runmode} | Mapping of logical filename failed.",job_status="FAILED", job_step="REMAPPING LOGICAL - FAILED"
            )             
            print(e)
            cursor.close()
            conn.close()
            raise SomethingWentWrong
            #logging.error(f"Error Running Script: {e}")

    def post_provision_step(self):
        try:
            takerest()
            self.logger.info(
            "Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Inserting metadata configs.",job_status="PROVISIONING", job_step="POST PROVISIONING"
            ) 
            meta_conn = DBConnectionManager(
                os.getenv("META_SERVER"),
                os.getenv("META_DATABASE"),
                os.getenv("META_USER"),
                os.getenv("META_PASSWORD"),
                os.getenv("META_PORT")
            ).connect()
            cursor = meta_conn.cursor()
            clientdate = datetime.now()
            formatted_time = clientdate.strftime("%b %d %Y %I:%M%p")
            DBServer_ID=""
            cursor.execute(
                "SELECT DBServer_ID FROM dbo.DBServers WHERE DBServer = ? ",
                self.server
            )
            row = cursor.fetchone()  
            if row:
                DBServer_ID = row[0] 
                self.logger.info("Post Provisioning", f"Server id identified as : {DBServer_ID} | Mode={self.runmode} | Inserting metadata configs.") 
            else:
                self.logger.error(
                    "Post Provisioning", f"Post Provisioning Error | Mode={self.runmode} | DBServer_ID not found for {self.server}.",job_status="FAILED", job_step="POST PROVISIONING"
                ) 
            self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Inserting Metadata on Customers.") 
            query = """
            INSERT INTO dbo.Customers (
                CustomerName, CustomerCode, Notes, IsSSLLCHosted, Customer_Status,
                NumSites, NumUsers, Server_ID, EnableQP, EnablePrelimReport,
                EnableWarranty, EnableEquipment, EnableMoistureMapper, Integration,
                IntegrationType, EnableDocumentMerge, OnLiveSite, DBServer_ID,
                BaseUrl, EnableMapping, JobSoftwareIntegrationName, EnableTechLoc,
                EnableActiveDirectory, TechLocMasterId, EnableSalesRouting,
                EnableAdditionalWarrantyStatus, EnableMuleHide,
                EnableQpReportFormatAustralianMoistureReadings
            )
            VALUES (
                ?, ?, ?, 1, 'Active',
                ?, ?, 6,
                1,1,0,1,0,0,NULL,1,0,?,
                ?,1,'None',0,0,NULL,1,0,0,0
            )
            """
            self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Query : {query.strip()}") 
            params = (
                self.jobpayload["company_name"],
                self.jobpayload["target_db_name"],
                os.getenv('META_NOTES')+f" {formatted_time}",
                self.jobpayload["num_sites"],
                self.jobpayload["num_desktops"],
                DBServer_ID,
                self.app_base_url
            )

            if self.runmode == "dry":
                print("===== DRY RUN =====")
                print("SQL:")
                print(query.strip())
                print("VALUES:")
                for i, val in enumerate(params, start=1):
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Param {i}: {repr(val)}") 
                    print(f"  Param {i}: {repr(val)}")

            elif self.runmode == "exec":
                for i, val in enumerate(params, start=1):
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Param {i}: {repr(val)}") 
                    print(f"  Param {i}: {repr(val)}")
                cursor.execute(query, params)
                meta_conn.commit()
                self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Inserted on Customers Table.") 

            clientcustomerID=""
            cursor.execute(
                "SELECT Customer_ID FROM dbo.Customers WHERE CustomerCode = ? ",
                self.target_db
            )
            row = cursor.fetchone()  
            if row:
                clientcustomerID = row[0] 
                self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | CustomerID identified as {clientcustomerID}.") 
            else:
                self.logger.error(
                    "Post Provisioning", f"Post Provisioning Error | Mode={self.runmode} | CustomerID not found for {self.target_db}.",job_status="FAILED", job_step="POST PROVISIONING"
                )                 
            clienseats= ""
            cursor.execute(
                "SELECT DeviceCode FROM dbo.DeviceCodes WHERE Num_Devices = ? ",
                self.jobpayload["num_mobiles"]
            )
            row = cursor.fetchone()  
            if row:
                clienseats = row[0] 
                self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | ClientSeats identified as {clienseats}.") 
            else:
                self.logger.error(
                    "Post Provisioning", f"Post Provisioning Error | Mode={self.runmode} | ClientSeats not found for No of mobile users {self.jobpayload["num_mobiles"]}.",job_status="FAILED", job_step="POST PROVISIONING"
                )
            self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Inserting on TblAuth.")                                   
            query = """
            INSERT INTO dbo.tblAuth (
                Customer_ID, COMPANY, PASSWORD, DeviceCodes_ID, SEATS, WALKS_ENABLED,
                DB_DSN, DB_USER, DB_PW, DB_NAME, DB_VERSION,
                ITEM_SYNC_LIMIT, ITEM_SYNC_MONTHS, SERVICE_REQUEST_STAMP,
                IMAGE_DIRECTORY, WO_SENDONSYNC, APPLICATION_TYPE,
                GPS_ENABLED, GPS_INTERVAL_HOURS, WALK_SYNC_MONTHS,
                EMAILSYNC_EMAIL, EMAILSYNC_PW, QBONLINE_ENABLED
            )
            VALUES (
                ?, ?, ?, ?, ?, 1,
                ?, 'PLMSyncUser', ?, ?, '1.5',
                24000, 24, 1,
                ?, 1, ?,
                0, 0, 12,
                ?, 'dNNg6C6HdegDBnT', ?
            )
            """
            self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Query : {query}") 
            params = (
                clientcustomerID,
                self.jobpayload["target_db_name"],
                self.jobpayload["target_db_name"][::-1],
                self.jobpayload["num_mobiles"],
                clienseats,
                "INT_"+ self.server,
                os.getenv('META_PASSWORD'),
                self.jobpayload["target_db_name"],
                f"{os.getenv('META_IMGDIR')}{self.jobpayload["target_db_name"]}",
                self.app_type,
                f"{self.jobpayload["target_db_name"]}@servicesoftwareinc.com",
                os.getenv('META_QBOENABLED')
            )

            if self.runmode == "dry":
                print("===== DRY RUN =====")
                print("SQL:")
                print(query.strip())
                print("VALUES:")
                for i, v in enumerate(params, start=1):
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Param {i}: {repr(v)}") 
                    print(f"  Param {i}: {repr(v)}")

            elif self.runmode == "exec":
                cursor.execute(query, params)
                for i, v in enumerate(params, start=1):
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Param {i}: {repr(v)}") 
                    print(f"  Param {i}: {repr(v)}")                
                meta_conn.commit()
                self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Inserted on TblAuth Table.",job_status="PROVISIONING", job_step="POST PROVISIONING") 

            else:
                raise ValueError(f"Invalid runmode: {self.runmode}")
            
            takerest()
            client_conn = DBConnectionManager(
                self.db_host,
                self.jobpayload["target_db_name"],
                self.db_user,
                self.db_pwd,
                self.db_port
            ).connect()
            if self.app_type == "RESTORATION":
                if self.runmode == "exec":
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Updating client database tables.",job_status="PROVISIONING", job_step="POST PROVISIONING") 
                    clcursor = client_conn.cursor()
                    query= f"""
                    UPDATE [dbo].[BUILDER]
                    SET build_PLMWebSite = 'https://{self.jobpayload["target_db_name"]}.restorationmanager.net',
                        build_OwnerWebSite = 'https://{self.jobpayload["target_db_name"]}.restorationmanager.net',
                        build_VendorWebSite = 'https://{self.jobpayload["target_db_name"]}.restorationmanager.net',
                        LogoDashboard = '/Builder Files/{self.jobpayload["target_db_name"]}/Logos/RESTOPROS_DashboardLogo_x2.png'
                    """
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Query [BUILDER] : {query}") 
                    clcursor.execute(query) 
                    query=f"""
                    UPDATE [dbo].[SYSTEM_Settings]
                    SET Logo = '/Builder Files/{self.jobpayload["target_db_name"]}/Logos/RESTOPROS_LoginLogo_x2.png',
                        LogoReports = '/Builder Files/{self.jobpayload["target_db_name"]}/Logos/RESTOPROS_ReportsLogo_x2.png'
                    """
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Query [SYSTEM_Settings] : {query}") 
                    clcursor.execute(query)
                    client_conn.commit()
                else:
                    query= f"""
                    UPDATE [dbo].[BUILDER]
                    SET build_PLMWebSite = 'https://{self.jobpayload["target_db_name"]}.restorationmanager.net',
                        build_OwnerWebSite = 'https://{self.jobpayload["target_db_name"]}.restorationmanager.net',
                        build_VendorWebSite = 'https://{self.jobpayload["target_db_name"]}.restorationmanager.net',
                        LogoDashboard = '/Builder Files/{self.jobpayload["target_db_name"]}/Logos/RESTOPROS_DashboardLogo_x2.png'
                    """
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Query [BUILDER] : {query}") 
                    query=f"""
                    UPDATE [dbo].[SYSTEM_Settings]
                    SET Logo = '/Builder Files/{self.jobpayload["target_db_name"]}/Logos/RESTOPROS_LoginLogo_x2.png',
                        LogoReports = '/Builder Files/{self.jobpayload["target_db_name"]}/Logos/RESTOPROS_ReportsLogo_x2.png'
                    """
                    self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Query [SYSTEM_Settings] : {query}") 
            else:
                pass
            self.logger.info("Post Provisioning", f"Post Provisioning | Mode={self.runmode} | Updating client database tables.",job_status="PROVISIONING", job_step="POST PROVISIONING")

        except Exception as e:
            print(e) 
        finally:
            clcursor.close()
            client_conn.close()
            cursor.close()
            meta_conn.close()

# ============================================================
# Sleep
# ============================================================
def takerest():
    time.sleep(0.01)


# ============================================================
# Entry Point
# ============================================================

def main():
    load_dotenv(override=True)
    server = socket.gethostname()
    args = parse_arguments()

    srvconn = DBConnectionManager(
            os.getenv(f"{server}_PROVISION_HOSTIP"),
            os.getenv(f"{server}_PROVISION_LOG_DATABASE"),
            os.getenv(f"{server}_PROVISION_USER"),
            os.getenv(f"{server}_PROVISION_PASSWORD"),
            os.getenv(f"{server}_PROVISION_PORT")
    ).connect()    
    logger = DBLogger(srvconn, args.job_id, "")

    try:
        job_loader = ExecJobLoader(srvconn, args.job_id, logger)

        job_payload = job_loader.load()
        logger.runmode = job_payload["job_mode"]

        provisioner = DatabaseProvisioner(job_payload, logger)
        provisioner.provision()

    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()