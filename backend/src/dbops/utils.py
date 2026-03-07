import pymssql, json
from datetime import datetime, timezone, timedelta
import time

async def create_job_remote(dbopsserv, data,job_log_payload, session):
    job_log_payload.update(
        exec_module ="create_job_remote",
        exec_status = "start",
        exec_detail = "Creating Job entries on target sever..",
    )
    await dbopsserv.log_event(job_log_payload, session)
    msdbs_id = data.server_data.server
    msdbs_logdir = await dbopsserv.get_mssql_server_mounts_by_id(data.server_data.mounts.log_dir, session) 
    msdbs_datadir = await dbopsserv.get_mssql_server_mounts_by_id(data.server_data.mounts.datadir, session) 
    remotesrv = await dbopsserv.get_mssql_server_by_id(msdbs_id, session)
    conn = getConnection(remotesrv.msdbs_host, remotesrv.msdbs_user, remotesrv.msdbs_password, remotesrv.msdbs_database, remotesrv.msdbs_port)
    if conn:
        job_log_payload.update(
        exec_status = "finished",
        exec_detail = f"Connection to remote server {remotesrv.msdbs_host} was estabilished successfully."
        )
        await dbopsserv.log_event(job_log_payload, session)
    else:
        job_log_payload.update(
        exec_status = "Failed.",
        exec_detail = "Creating Job entries on target sever failed",
        )
        job_payload = {
            "job_status" : "FAILED",
            "job_current_step" : "create_job_remote",
            "job_current_log" : "create_job_remote",
            "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
        }
        await dbopsserv.log_event(job_log_payload, session)
        await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)

    job_log_payload.update(
        exec_module ="create_remote_tables",
        exec_status = "start",
        exec_detail = "Creating tables if not exists in target sever..",
    )    
    await dbopsserv.log_event(job_log_payload, session)

    status = await create_remote_tables(conn)
    if status:
        job_log_payload.update(
            exec_module ="create_remote_tables",
            exec_status = "completed",
            exec_detail = "Creating tables if not exists in target sever.. completed.",
        )    
        await dbopsserv.log_event(job_log_payload, session)
    else:
        job_log_payload.update(
        exec_status = "Failed.",
        exec_detail = "Creating tables if not exists in target sever failed",
        )
        job_payload = {
            "job_status" : "FAILED",
            "job_current_step" : "create_remote_tables",
            "job_current_log" : "create_remote_tables",
            "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
        }
        await dbopsserv.log_event(job_log_payload, session)
        await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)

    remote_job_payload_parameters = {
        "job_api_job_id" : str(job_log_payload["exec_job_id"]),
        "job_mode" : job_log_payload["exec_action"],
        "num_sites" : data.jira_ticket_details.jirat_num_sites,
        "num_desktops" : data.jira_ticket_details.jirat_desktop_licenses,
        "num_mobiles" : data.jira_ticket_details.jirat_mobile_licenses,
        "target_db_name" : data.jira_ticket_details.jirat_db_name,
        "source_db_name" : data.jira_ticket_details.jirat_src_app_type,
        "company_name" : data.jira_ticket_details.jirat_company_name,
        "data_dir" : msdbs_datadir.msdbsm_path,
        "log_dir" : msdbs_logdir.msdbsm_path
    }
    job_payload = {
            "job_status" : "INITIALIZING",
            "job_current_step" : "create_remote_job_entry",
            "job_current_log" : "create_remote_job_entry",
            "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
    }
    await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)    
    job_log_payload.update(
            exec_module ="create_remote_job_entry",
            exec_status = "start",
            exec_detail = "Creating job entries on remote...",
    )  
    await dbopsserv.log_event(job_log_payload, session)
    remote_job = await create_remote_job_entry(conn, remote_job_payload_parameters)
    if remote_job:
        job_log_payload.update(
            exec_module ="create_remote_job_entry",
            exec_status = "completed",
            exec_detail = "Creating of job entry on target sever.. completed.",
        )    
        await dbopsserv.log_event(job_log_payload, session)
    else:
        job_log_payload.update(
        exec_status = "Failed.",
        exec_detail = "Creating of job entry on target sever..failed",
        )
        job_payload = {
            "job_status" : "FAILED",
            "job_current_step" : "create_remote_job_entry",
            "job_current_log" : "create_remote_job_entry",
            "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
        }
        await dbopsserv.log_event(job_log_payload, session)
        await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)
    conn.close()
    conn = getConnection(remotesrv.msdbs_host, remotesrv.msdbs_user, remotesrv.msdbs_password, "msdb", remotesrv.msdbs_port)
    jobstatus = await create_remote_sqlagent_job(conn, dbopsserv, job_log_payload, session)
    print(jobstatus)
    if jobstatus:
        return jobstatus

async def create_remote_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM sys.tables
                WHERE name = 'execjob'
                AND schema_id = SCHEMA_ID('dbo')
            )
            BEGIN
                CREATE TABLE dbo.execjob (
                    job_id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWID(),
                    job_api_job_id VARCHAR(255) NOT NULL,
                    job_mode VARCHAR(50) NOT NULL,
                    job_parameters VARCHAR(MAX) NOT NULL,
                    job_progress VARCHAR(255) NULL,
                    job_status VARCHAR(50) NULL,
                    job_current_step VARCHAR(100) NULL,
                    job_current_log VARCHAR(255) NULL,
                    job_created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                    job_updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
                )
            END
        """)

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM sys.tables
                WHERE name = 'execlog'
                AND schema_id = SCHEMA_ID('dbo')
            )
                BEGIN
                    CREATE TABLE dbo.execlog (
                        exec_id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWID(),
                        exec_user VARCHAR(100) NULL,
                        exec_job_id VARCHAR(100) NOT NULL,
                        exec_module VARCHAR(100) NULL,
                        exec_action VARCHAR(255) NULL,
                        exec_status VARCHAR(50) NULL,
                        exec_detail VARCHAR(MAX) NULL,
                        exec_remotepull VARCHAR(100) NULL,
                        exec_datetime DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
                    )
                END
        """)
        conn.commit()
        cursor.close()
        return {"action" : "success"}
    except pymssql.DatabaseError as e:
        print("Failed to create tables:", e)
        cursor.close()
        conn.rollback()
        return None


async def create_remote_job_entry(conn, payload):
    try:
        cursor = conn.cursor()          
        cursor.execute("""
                    INSERT INTO execjob
                    (job_api_job_id, job_mode, job_parameters, job_progress, job_status, job_current_step,job_current_log)
                    VALUES (%s, %s, %s,%s ,%s, %s, %s)
                    """, 
                    (payload["job_api_job_id"], payload["job_mode"], json.dumps(payload), '5', "INITIALIZING","create_remote_job_entry", "" ))
        conn.commit()
        return {"action" : "success"}
    except pymssql.DatabaseError as e:
        print("Failed create job parameters on remote:", e)
        cursor.close()
        conn.rollback()
        return None        

async def create_remote_sqlagent_job(conn, dbopsserv, job_log_payload, session):
    try:
        job_name = "ProvisionDBbyDbDashAutomation"
        job_description = "Job Created by DbDash database provision Automation"

        cursor = conn.cursor()

        job_payload = {
            "job_status" : "INITIALIZING",
            "job_current_step" : "create_remote_sqlagent_job",
            "job_current_log" : "create_remote_sqlagent_job",
            "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
        }
        await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)

        try:
            job_log_payload.update(
                exec_module ="create_remote_sqlagent_job",
                exec_status = "Start.",
                exec_detail = f"Deleting job {job_name} if already exists on remote.",
                )
            await dbopsserv.log_event(job_log_payload, session)

            cursor.execute("""
            IF EXISTS (
                SELECT 1
                FROM msdb.dbo.sysjobs
                WHERE name = %s
            )
            BEGIN
                EXEC msdb.dbo.sp_delete_job
                    @job_name = %s,
                    @delete_unused_schedule = 1
            END
            """, (job_name, job_name))  

            job_log_payload.update(
                exec_status = "Completed.",
                )
            await dbopsserv.log_event(job_log_payload, session)

        except pymssql.DatabaseError as e:
            print("Failed create job parameters on remote:", e)   
            job_log_payload.update(
            exec_status = "Failed.",
            exec_detail = "Deleting of remote job on target sever..failed",
            )
            job_payload.update (
                job_status = "FAILED",
                job_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
            await dbopsserv.log_event(job_log_payload, session)
            await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)
            cursor.close()
            conn.close()
            #raise

        try:
            job_log_payload.update(
                exec_module ="create_remote_sqlagent_job",
                exec_status = "Start.",
                exec_detail = f"Creating job {job_name} on remote.",
                )
            await dbopsserv.log_event(job_log_payload, session)
            cursor.execute("""
                EXEC msdb.dbo.sp_add_job
                    @job_name = %s,
                    @enabled = 1,
                    @description = %s
                """, (job_name, job_description))  
            job_log_payload.update(
                exec_status = "Completed.",
                )
            await dbopsserv.log_event(job_log_payload, session)            

        except pymssql.DatabaseError as e:
            print("Failed create job parameters on remote:", e)   
            job_log_payload.update(
            exec_status = "Failed.",
            exec_detail = "Creating of remote job on target sever..failed",
            )
            job_payload.update (
                job_status = "FAILED",
                job_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
            await dbopsserv.log_event(job_log_payload, session)
            await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)  
            cursor.close()
            conn.close()

        try:
            cliJobCmd=f'"C:\\Users\\PIDVISCXADMINP\\Desktop\\dba-workspace\\DbDashAutomation\\DbDashAutomate.bat" "{job_log_payload["exec_job_id"]}"'       
            job_log_payload.update(
                exec_module ="create_remote_sqlagent_job",
                exec_status = "Start.",
                exec_detail = f"Adding job steps on remote - {cliJobCmd}",
                )
            await dbopsserv.log_event(job_log_payload, session)
            cursor.execute("""
            EXEC msdb.dbo.sp_add_jobstep
                @job_name = %s,
                @step_name = 'RunBat',
                @subsystem = 'CmdExec',
                @command = %s,
                @on_success_action = 1,
                @on_fail_action = 2
            """, (job_name, cliJobCmd))
            job_log_payload.update(
                exec_status = "Completed.",
                )
            await dbopsserv.log_event(job_log_payload, session)    

        except pymssql.DatabaseError as e:
            print("Failed create job parameters on remote:", e)   
            job_log_payload.update(
            exec_status = "Failed.",
            exec_detail = "Adding job steps on remote - failed",
            )
            job_payload.update (
                job_status = "FAILED",
                job_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
            await dbopsserv.log_event(job_log_payload, session)
            await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)  
            cursor.close()
            conn.close()

        try:
            job_log_payload.update(
                exec_module ="create_remote_sqlagent_job",
                exec_status = "Start.",
                exec_detail = f"Attaching the job to a SQL Server Agent server",
                )
            await dbopsserv.log_event(job_log_payload, session)            
            cursor.execute("""
            EXEC msdb.dbo.sp_add_jobserver
                @job_name = %s
            """, (job_name,))
            conn.commit()
            job_log_payload.update(
                exec_status = "Completed.",
                )
            await dbopsserv.log_event(job_log_payload, session)                
        except pymssql.DatabaseError as e:
            print("Failed create job parameters on remote:", e)   
            job_log_payload.update(
            exec_status = "Failed.",
            exec_detail = "Attaching the job to a SQL Server Agent server - failed",
            )
            job_payload.update (
                job_status = "FAILED",
                job_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
            await dbopsserv.log_event(job_log_payload, session)
            await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)  
            cursor.close()
            conn.close()            

        try:
            job_log_payload.update(
                exec_module ="create_remote_sqlagent_job",
                exec_status = "Start.",
                exec_detail = f"Preparing to run the job on remote server",
                )
            await dbopsserv.log_event(job_log_payload, session)   
            cursor.execute("""
            EXEC msdb.dbo.sp_start_job @job_name = %s
            """, (job_name,))
            conn.commit()
            job_log_payload.update(
                exec_status = "Completed.",
                exec_detail = f"Job has been started on remote server",                
                )
            await dbopsserv.log_event(job_log_payload, session) 
            job_payload.update (
                job_status = "VALIDATING",
                job_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
            await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)  
            return {"action":"submitted"}

        except pymssql.DatabaseError as e:
            print("Failed create job parameters on remote:", e)   
            job_log_payload.update(
            exec_status = "Failed.",
            exec_detail = "Preparing to run the job on remote server - failed",
            )
            job_payload.update (
                job_status = "FAILED",
                job_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
            await dbopsserv.log_event(job_log_payload, session)
            await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)  
            cursor.close()
            conn.close()

        cursor.close()
        conn.close()

    except Exception as e:
        print("Something went wrong..", e)        
        job_payload = {
            "job_status" : "FAILED",
            "job_current_step" : "create_remote_sqlagent_job",
            "job_current_log" : "create_remote_sqlagent_job",
            "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
        }
        job_log_payload.update(
                exec_module ="create_remote_sqlagent_job",
                exec_status = "Failed.",
                exec_detail = f"Something went wrong, please contact team..",
        )       
        await dbopsserv.log_event(job_log_payload, session)
        await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session) 
        cursor.close()
        conn.close()        

async def get_job_status_remote(dbopsserv, data,job_log_payload, session):
    job_id = job_log_payload["exec_job_id"]
    msdbs_id = data.server_data.server
    remotesrv = await dbopsserv.get_mssql_server_by_id(msdbs_id, session)
    try:
        TIMEOUT_HOURS=2
        start_time = datetime.now()
        timeout_at = start_time + timedelta(hours=TIMEOUT_HOURS)

        conn = getConnection(remotesrv.msdbs_host, remotesrv.msdbs_user, remotesrv.msdbs_password, remotesrv.msdbs_database, remotesrv.msdbs_port)
        cursor = conn.cursor(as_dict=True)
        while True:
            if datetime.now() >= timeout_at:
                print(f"Job {job_id} timed out after {TIMEOUT_HOURS} hours")
                job_payload = {
                    "job_status" : "FAILED",
                    "job_mode" : "",
                    "job_current_step" : "Job ran for longer than 2 hrs and makred as timed out",
                    "job_current_log" : "",
                    "job_progress" : "",
                    "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
                }
                await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session) 
                break
            cursor.execute(
                "SELECT * FROM dbo.execjob WHERE job_api_job_id = %s",
                (job_id,)
            )
            #cursor.execute("SELECT * FROM dbo.execjob WHERE job_api_job_id = ?", job_id)
            row = cursor.fetchone()

            if row:
                job_payload = {
                    "job_status": row["job_status"],
                    "job_mode": row["job_mode"],
                    "job_current_step": row["job_current_step"],
                    "job_current_log": row["job_current_log"],
                    "job_progress": row["job_progress"],
                    "job_updated_at" : datetime.now(timezone.utc).replace(tzinfo=None)
                }
                cursor.execute(
                    "SELECT * FROM dbo.execlog WHERE exec_job_id = %s and exec_remotepull='N' order by exec_datetime asc",
                    (job_id,)
                )                
                #cursor.execute("SELECT * FROM dbo.execlog WHERE exec_job_id = ? and exec_remotepull='N'", job_id)
                jobrows = cursor.fetchall()
                if jobrows:
                    for jrow in jobrows:
                        job_log_payload.update(
                            exec_module = jrow["exec_module"],
                            exec_status = jrow["exec_status"],
                            exec_detail = jrow["exec_detail"],
                        )       
                        await dbopsserv.log_event(job_log_payload, session)    
                        cursor.execute(
                            "UPDATE dbo.execlog SET exec_remotepull = 'Y' WHERE exec_id = %s ",
                            (jrow["exec_id"],)
                        )                                         
                        #cursor.execute("UPDATE dbo.execlog SET exec_remotepull = 'Y' WHERE exec_job_id = ? ", job_id)
                        conn.commit()
                await dbopsserv.update_job_status_local(job_log_payload["exec_job_id"], job_payload, session)                  
                status = row["job_status"]
                if status in ("COMPLETED", "FAILED"):
                    comment = f"DbDash Automation Update -> Job Status : {status}"
                    #     async def close_jira_ticket(self, jirat_meta_id: str, jira_ticket: str, transition_id: str, session: AsyncSession):
                    await dbopsserv.add_comment_to_jira(data.jira_ticket_details.jirat_meta_id, data.jira_ticket_details.jirat_ticket, comment, session)
                    await dbopsserv.close_jira_ticket(data.jira_ticket_details.jirat_meta_id, data.jira_ticket_details.jirat_ticket, "31", session)
                    print(f"Job {job_id} finished with status: {status}")
                    break
            time.sleep(30)
        cursor.close()
        conn.close()
    except Exception():
        pass

async def start_job_execution_remote(self, data):
    pass


##
## Get the connection of the database
##
def getConnection(server, username, password,database, port):
    try:
        return pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database,
            port=port
            )

    except Exception as e:
        print(f"Obtaining Connection to remote server {server} failed.: {e}")
        

##
## Close the connection to database
##
def closeConnection(conn):
    conn.close()
