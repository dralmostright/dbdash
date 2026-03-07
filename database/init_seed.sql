\connect postgres
CREATE EXTENSION IF NOT EXISTS pg_cron;

\connect dbdash
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman SCHEMA partman;

CREATE TABLE IF NOT EXISTS public.apiusers
(
    uid uuid NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    password_hash character varying COLLATE pg_catalog."default" NOT NULL,
    first_name character varying COLLATE pg_catalog."default" NOT NULL,
    last_name character varying COLLATE pg_catalog."default" NOT NULL,
    role character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'user'::character varying,
    is_verified boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    display_pic character varying COLLATE pg_catalog."default" DEFAULT '/img/profile-imp.jpg'::character varying,
    CONSTRAINT apiusers_pkey PRIMARY KEY (uid)
)
TABLESPACE pg_default;

---
--- Insert a default admin user
--- plain text password : Test@1234
---
INSERT INTO PUBLIC.apiusers
            (uid,
             username,
             email,
             password_hash,
             first_name,
             last_name,
             role,
             is_verified,
             created_at,
             updated_at)
VALUES      ( 'a1023fe6-1dea-4525-bc6e-2b546092d031',
              'admin',
              'admin@dbdash.com',
              '$pbkdf2-sha256$29000$IwQAIMRY633vvZeSslaKcQ$Y9Tt/ibcwyjaK6pUJRPMjMVdKupnxq4iVmpsjJJgGQE',
              'Srisha',
              'Adhikari',
              'admin',
              'true',
              Now(),
              Now() 
              ); 

--
-- This table constains information about aws accounts that a orginization has
--
CREATE TABLE IF NOT EXISTS public.awsaccounts
(
    aid uuid NOT NULL,
    account_number character varying(50) COLLATE pg_catalog."default" NOT NULL,
    account_alias character varying COLLATE pg_catalog."default" NOT NULL,
    account_org character varying COLLATE pg_catalog."default" NOT NULL,
    account_status boolean NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    description character varying COLLATE pg_catalog."default",
    account_az character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT awsaccounts_pkey PRIMARY KEY (aid),
    CONSTRAINT awsaccounts_account_number_key UNIQUE (account_number)
)
TABLESPACE pg_default;


--
-- This is one of the main table and its the one which will be growing in future
-- It holds all the rds information obtained from each account
-- 
CREATE TABLE IF NOT EXISTS public.rdsinstances
(
    riid uuid NOT NULL,
    rds_aws_id uuid NOT NULL,
    rds_identifier character varying COLLATE pg_catalog."default",
    rds_instanceclass character varying COLLATE pg_catalog."default",
    rds_engine character varying COLLATE pg_catalog."default",
    rds_inststatus character varying COLLATE pg_catalog."default",
    rds_instcreatetime timestamp without time zone,
    rds_allocstorage character varying COLLATE pg_catalog."default",
    rds_paramgroup character varying COLLATE pg_catalog."default",
    rds_az character varying COLLATE pg_catalog."default",
    rds_enginever character varying COLLATE pg_catalog."default",
    rds_lisencemodel character varying COLLATE pg_catalog."default",
    rds_copytagsnapshot character varying COLLATE pg_catalog."default",
    rds_storagetype character varying COLLATE pg_catalog."default",
    rds_multiaz character varying COLLATE pg_catalog."default",
    rds_storageencrypted character varying COLLATE pg_catalog."default",
    rds_deleteprotection character varying COLLATE pg_catalog."default",
    rds_clusteridentifier character varying COLLATE pg_catalog."default",
    rds_masteruser character varying COLLATE pg_catalog."default",
    rds_dbinstrole character varying COLLATE pg_catalog."default",
    rds_clusterendpoint character varying COLLATE pg_catalog."default",
    rds_endpoint character varying COLLATE pg_catalog."default",
    rds_port character varying COLLATE pg_catalog."default",
    rds_vpc character varying COLLATE pg_catalog."default",
    rds_secgroup character varying COLLATE pg_catalog."default",
    rds_subnetgrp character varying COLLATE pg_catalog."default",
    rds_subnets character varying COLLATE pg_catalog."default",
    rds_backupretention character varying COLLATE pg_catalog."default",
    rds_taglist character varying COLLATE pg_catalog."default" NOT NULL,
    rds_datacollectiondate bigint,
    created_at timestamp without time zone,
    CONSTRAINT rdsinstances_pkey PRIMARY KEY (riid, created_at)
)
PARTITION BY RANGE (created_at);

CREATE INDEX idx_rdsinstances_created_at
    ON public.rdsinstances (created_at);

CREATE INDEX idx_rdsinstances_rds_identifier
    ON public.rdsinstances (rds_identifier);

--
--
--
CREATE TABLE IF NOT EXISTS public.rdsawsmap
(
    raid uuid NOT NULL,
    created_at timestamp without time zone,
    aws_aid uuid NOT NULL,
    rds_riid uuid NOT NULL,
    map_rds_identifier character varying COLLATE pg_catalog."default",
    map_rds_az character varying COLLATE pg_catalog."default",
    last_collection_at bigint,
    CONSTRAINT rdsawsmap_pkey PRIMARY KEY (raid, rds_riid),
    CONSTRAINT rdsawsmap_aws_aid_fkey FOREIGN KEY (aws_aid)
        REFERENCES public.awsaccounts (aid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE    
)
TABLESPACE pg_default;


---
---
---
CREATE TABLE IF NOT EXISTS public.rdsinstparams
(
    param_id uuid NOT NULL,
    param_type character varying COLLATE pg_catalog."default",
    param_groupname character varying COLLATE pg_catalog."default",
    param_name character varying COLLATE pg_catalog."default",
    param_value character varying COLLATE pg_catalog."default",
    param_riid uuid NOT NULL,
    param_row_created_at timestamp without time zone,
    CONSTRAINT rdsinstparams_pkey PRIMARY KEY (param_id,param_row_created_at)
)
PARTITION BY RANGE (param_row_created_at);

---
---
--- sec_rule_name character varying COLLATE pg_catalog."default",
CREATE TABLE IF NOT EXISTS public.rdssecrules
(
    sec_id uuid NOT NULL,
    sec_group_name character varying COLLATE pg_catalog."default",
    sec_gpid character varying COLLATE pg_catalog."default",
    sec_riid uuid NOT NULL,
    sec_port_range character varying COLLATE pg_catalog."default",
    sec_rule_type character varying COLLATE pg_catalog."default",
    sec_ip_ranges character varying COLLATE pg_catalog."default",
    sec_row_created_at timestamp without time zone,
    sec_row_updated_at timestamp without time zone,
    CONSTRAINT rdssecrules_pkey PRIMARY KEY (sec_id,sec_row_created_at)
)
PARTITION BY RANGE (sec_row_created_at);

---
---
---
CREATE TABLE IF NOT EXISTS public.rdsmajoreol
(
    rds_ma_id uuid NOT NULL,
    rds_ma_type character varying COLLATE pg_catalog."default",
    rds_ma_ver character varying COLLATE pg_catalog."default",
    rds_ma_cm_release_date character varying COLLATE pg_catalog."default",
    rds_ma_release_date character varying COLLATE pg_catalog."default",
    rds_ma_cm_eol character varying COLLATE pg_catalog."default",
    rds_ma_rds_seol character varying COLLATE pg_catalog."default",
    rds_ma_ex_eol character varying COLLATE pg_catalog."default",
    rds_ma_1y_ex_eol character varying COLLATE pg_catalog."default",
    rds_ma_3y_ex_eol character varying COLLATE pg_catalog."default",
    rds_ma_lts character varying COLLATE pg_catalog."default",
    url_raw character varying COLLATE pg_catalog."default",
    ma_row_created_at timestamp without time zone,
    CONSTRAINT rdsmajoreol_pkey PRIMARY KEY (rds_ma_id)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.rdsminoreol
(
    rds_mi_id uuid NOT NULL,
    rds_mi_type character varying COLLATE pg_catalog."default",
    rds_mi_ma_ver character varying COLLATE pg_catalog."default",
    rds_mi_ver character varying COLLATE pg_catalog."default",
    rds_mi_cr_date character varying COLLATE pg_catalog."default",
    rds_mi_release_date character varying COLLATE pg_catalog."default",
    rds_mi_seol character varying COLLATE pg_catalog."default",
    rds_mi_lts character varying COLLATE pg_catalog."default",
    url_raw character varying COLLATE pg_catalog."default",
    mi_row_created_at timestamp without time zone,
    CONSTRAINT rdsminoreol_pkey PRIMARY KEY (rds_mi_id)
)
TABLESPACE pg_default;

---
---
---
CREATE TABLE IF NOT EXISTS public.ec2hwdetail
(
    ec2_hw_type_id uuid NOT NULL,
    ec2_hw_model character varying COLLATE pg_catalog."default",
    ec2_hw_type character varying COLLATE pg_catalog."default",
    ec2_hw_basebandwm character varying COLLATE pg_catalog."default",
    ec2_hw_maxbandwm character varying COLLATE pg_catalog."default",
    ec2_hw_basethroputm character varying COLLATE pg_catalog."default",
    ec2_hw_maxthroputm character varying COLLATE pg_catalog."default",
    ec2_hw_baseiopsm character varying COLLATE pg_catalog."default",
    ec2_hw_maxiopswm character varying COLLATE pg_catalog."default",
    url_raw character varying COLLATE pg_catalog."default",
    CONSTRAINT ec2hwdetail_pkey PRIMARY KEY (ec2_hw_type_id)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.rdshwdetail
(
    rds_hw_id uuid NOT NULL,
    rds_hw_model character varying COLLATE pg_catalog."default",
    rds_hw_type character varying COLLATE pg_catalog."default",
    rds_hw_vcpu character varying COLLATE pg_catalog."default",
    rds_hw_core character varying COLLATE pg_catalog."default",
    rds_hw_mem character varying COLLATE pg_catalog."default",
    rds_hw_storage character varying COLLATE pg_catalog."default",
    rds_hw_ebs_mbps character varying COLLATE pg_catalog."default",
    rds_hw_net_gbps character varying COLLATE pg_catalog."default",
    rds_hw_ebs_gbps character varying COLLATE pg_catalog."default",
    url_raw character varying COLLATE pg_catalog."default",
    CONSTRAINT rdshwdetail_pkey PRIMARY KEY (rds_hw_id)
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.rdssnapshots
(
    snap_id uuid NOT NULL,
    snap_identifier character varying COLLATE pg_catalog."default",
    snap_rds_identifier character varying COLLATE pg_catalog."default",
    snap_type character varying COLLATE pg_catalog."default",
    snap_inst_type character varying COLLATE pg_catalog."default",
    snap_status character varying COLLATE pg_catalog."default",
    snap_created_time timestamp without time zone,
    snap_engine character varying COLLATE pg_catalog."default",
    snap_allocated_storage character varying COLLATE pg_catalog."default",
    snap_az character varying COLLATE pg_catalog."default",
    snap_region character varying COLLATE pg_catalog."default",    
    snap_engine_ver character varying COLLATE pg_catalog."default",
    snap_ipos character varying COLLATE pg_catalog."default",
    snap_throughtput character varying COLLATE pg_catalog."default",
    snap_taglist character varying COLLATE pg_catalog."default",
    snap_arn character varying COLLATE pg_catalog."default",
    snap_srcregion character varying COLLATE pg_catalog."default",
    snap_srcidentifier character varying COLLATE pg_catalog."default",
    snap_row_created_at timestamp without time zone,
    snap_aws_id uuid NOT NULL,
    snap_progress character varying COLLATE pg_catalog."default",
    CONSTRAINT rdssnapshots_pkey PRIMARY KEY (snap_id, snap_row_created_at)
)
PARTITION BY RANGE (snap_row_created_at);


CREATE TABLE IF NOT EXISTS public.snapawsrdsmap
(
    sar_id uuid NOT NULL,
    sar_created_at timestamp without time zone,
    sar_snap_id uuid NOT NULL,
    sar_aws_aid uuid NOT NULL,
    sar_snap_identifier character varying COLLATE pg_catalog."default",
    sar_rds_az character varying COLLATE pg_catalog."default",
    sar_last_collection_at timestamp without time zone,
    CONSTRAINT snapawsrdsmap_pkey PRIMARY KEY (sar_id)
)
TABLESPACE pg_default;




SET search_path TO "$user", partman, public;
-- Create monthly partitions for the table
-- create the next 4 partition in advance
-- starts from first existing row
SELECT partman.create_parent(
    p_parent_table := 'public.rdsinstances',
    p_control := 'created_at',
    p_type := 'range',
    p_interval := '1 month',
    p_premake := 4,           
    p_start_partition := NULL 
);
UPDATE partman.part_config
SET retention = '24 months',
    retention_keep_table = false
WHERE parent_table = 'public.rdsinstances';

SELECT partman.create_parent(
    p_parent_table := 'public.rdsinstparams',
    p_control := 'param_row_created_at',
    p_type := 'range',
    p_interval := '1 month',
    p_premake := 4,           
    p_start_partition := NULL  
);
UPDATE partman.part_config
SET retention = '24 months',
    retention_keep_table = false
WHERE parent_table = 'public.rdsinstparams';

SELECT partman.create_parent(
    p_parent_table := 'public.rdssecrules',
    p_control := 'sec_row_created_at',
    p_type := 'range',
    p_interval := '1 month',
    p_premake := 4,           
    p_start_partition := NULL    
);

UPDATE partman.part_config
SET retention = '24 months',
    retention_keep_table = false
WHERE parent_table = 'public.rdssecrules';

SELECT partman.create_parent(
    p_parent_table := 'public.rdssnapshots',
    p_control := 'snap_row_created_at',
    p_type := 'range',
    p_interval := '1 month',
    p_premake := 4,           
    p_start_partition := NULL    
);

UPDATE partman.part_config
SET retention = '12 months',
    retention_keep_table = false
WHERE parent_table = 'public.rdssnapshots';



\connect postgres
SELECT cron.schedule(
    'pg_partman_maintenance',
    '0 2 * * *',  
    $$SELECT partman.run_maintenance('public.rdsinstances');$$
);

SELECT cron.schedule(
    'pg_partman_maintenance',
    '0 2 * * *', 
    $$SELECT partman.run_maintenance('public.rdsinstparams');$$
);

SELECT cron.schedule(
    'pg_partman_maintenance',
    '0 2 * * *', 
    $$SELECT partman.run_maintenance('public.rdssecrules');$$
);

SELECT cron.schedule(
    'pg_partman_maintenance',
    '0 2 * * *', 
    $$SELECT partman.run_maintenance('public.rdssnapshots');$$
);