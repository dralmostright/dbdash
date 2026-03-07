# Database Schema & Partitioning Documentation
## Overview

This script is optional, I am posting it here for better performance of the application in future. The owner i have used is apiusr, you can change as per your need and the schema i am using is public you can create you own database and schemas to run this script. Database used is postgres, just to make things simple and ease

This document describes the PostgreSQL database schema used by the application, with a focus on scalability, performance, and long-term data retention.
The design leverages native PostgreSQL partitioning, pg_partman, and pg_cron to efficiently manage large and growing datasets.

* Database Engine: PostgreSQL
* Database: dbdash (configurable)
* Schema: public (configurable)
* Owner: apiusr (configurable)
* Primary Growth Table: public.rdsinstances
* Partitioning Strategy: Time-based (monthly)
* Maintenance: Automated via pg_partman + pg_cron

### Extensions Used
|Extension|Purpose|
|---------|-------|
|pg_partman	|Automated partition creation & retention|
|pg_cron	| Scheduled maintenance jobs |

Script:
```sql
--8<-- "database/init_seed.sql:1:7"
```

### Core Tables
#### 1. public.apiusers

Stores authentication and profile metadata
```sql
--8<-- "database/init_seed.sql:9:24"
```

#### 2. public.awsaccounts

Stores AWS account metadata associated with an organization.

```sql
--8<-- "database/init_seed.sql:56:70"
```
#### 3. public.rdsinstances

Stores RDS instance metadata collected over time. This table is expected to grow significantly and is therefore range-partitioned by time.
```sql
--8<-- "database/init_seed.sql:73:118"
```

##### Why Partitioning?

* Efficient query pruning for time-based queries
* Fast data cleanup via partition drops
* Improved insert and query performance at scale


#### 4. public.rdsawsmap
Maps AWS accounts to RDS instances.
```sql
--8<-- "database/init_seed.sql:123:138"
```

#### 5. public.rdsinstparams
Stores parameter group details per RDS instance (only non default)
```sql
--8<-- "database/init_seed.sql:144:155"
```

#### 6. public.rdssecrules

Stores security group rules associated with RDS instances.
```sql
--8<-- "database/init_seed.sql:160:173"
```

#### 7. public.rdsmajoreol/rdsmajoreol
Tracks major and minor engine end-of-life (EOL) data.
```sql
--8<-- "database/init_seed.sql:178:211"
```

#### 8. public.ec2hwdetail/rdshwdetail

Stores EC2 and RDS hardware specifications.
```sql
--8<-- "database/init_seed.sql:216:246"
```

#### 9. public.rdssnapshots

Stores RDS Snapshots information.
```sql
--8<-- "database/init_seed.sql:249:274"
```

#### 10. public.snapawsrdsmap
Stores RDS Snapshots Mapping information.
```sql
--8<-- "database/init_seed.sql:277:288"
```

### Partition Management with pg_partman

#### Create Monthly Partitions
Behavior

* Monthly partitions
* Automatically creates 4 future partitions
* Backfills partitions based on existing data
```sql
--8<-- "database/init_seed.sql:293:349"
```

#### Retention Policy
Define the retention of the data, you can alter this as per your needs.

Effect

* Retains only the last 24 months of data
* Older partitions are automatically dropped


#### Automated Maintenance (pg_cron)
Runs Daily

* Creates future partitions
* Drops expired partitions
* Keeps metadata in sync
```sql
--8<-- "database/init_seed.sql:353:376"
```

### Notes
The Tables can be created by the by api itself, but due to partitions feature not enabled via ORM the above partitions script are being shared, if those are not needed then the following line needs to be uncommented and it will create all the required tables and their properties as needed.

```text
dbdash/
├── backend/
│   ├── src/
│   │   ├── db/
│   │       ├── main.py    ===> This file needs to be modified.
```


```python
--8<-- "backend/src/db/main.py:14:19"
```

