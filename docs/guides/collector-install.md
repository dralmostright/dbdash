# Collector 
This module describes how to set up the data collection process and what are required to set up the data collection. This is  a simple python scripts which collects the RDS metadata from aws. It doesn't do amy modification or any changes and is completely readonly scripts to AWS. It depends upon some configuration files hence, it's necessary for proper setup of those configurations, which are described detail on below

## Configuration 

### Environment valraibles
The collector script depends on below environment variables, some of which it derives automatcally from the ```.env``` file.
```python
--8<-- "collector/collector.py:23:34"
```

Below is the sample ```.env``` teamplate, you need to adjust the values accordingly, only ```API_*``` needs to be changed and ```API_*_URL``` 's host and port needs to be changes. ```aws-acct-1=arn:aws:iam::430045346560:role/DbDashCollectorRemoteRole``` this is the role's arn of the aws account which we want to collect the metadata and this can be any n number.
```bash
aws-acct-1=arn:aws:iam::430045346560:role/DbDashCollectorRemoteRole
aws-acct-2=arn:aws:iam::358665433441:role/DbDashCollectorRole

RDSAPI_URL = "/aws/rds/instance"
RDSMAPAPI_URL = "/aws/rds/instance/map"
RDSPARAMSAPI_URL = "/aws/rds/instance/parameter"
RDSSECRULESAPI_URL = "/aws/rds/instance/secrules"
API_USERNAME = "admin@dbdash.com"
API_PASSWORD = "Test@1234"
API_TOKEN_URL = "http://apihost:8000/api/v1/auth/login"
API_AZ_URL = "http://apihost:8000/api/v1/aws/org/byaccount"
API_BASE_URL = "http://apihost:8000/api/v1"
```

### Privileges required

#### Cross-Account Access Flow

* Account A (358665433441): Account where the collector script resides.
* Account B (430045346560): On of the target account, which the collector script wants to collect the data.

Below is the control flow how the collector works:
```text
+----------------+                        +----------------+
|                |                        |                |
|   Account A    |                        |   Account B    |
|  (Caller)      |                        |  (RDS Owner)   |
|                |                        |                |
+----------------+                        +----------------+
        |                                           |
        | 1. Assume Role (sts:AssumeRole)           |
        |------------------------------------------>|
        |                                           |
        |                                           | 2. Verify Trust Policy
        |                                           |   - Principal: Account A
        |                                           |   - Action: sts:AssumeRole
        |                                           |
        |                                           | 3. Issue Temporary Credentials
        |                                           |   - AccessKeyId
        |                                           |   - SecretAccessKey
        |                                           |   - SessionToken
        |<------------------------------------------|
        |                                           |
        | 4. Use Temporary Credentials to Call      |
        |    rds:DescribeDBInstances                |
        |------------------------------------------>|
        |                                           |
        |                                           | 5. Respond with RDS Metadata
        |<------------------------------------------|

```

#### Policies and Roles

##### Account A 

This is account where collector script resides.

On Account A create a collector policy ```DbDashCollectorPolicy``` with below json.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances",
        "rds:DescribeDBSecurityGroups",
        "rds:DescribeDBClusterParameterGroups",
        "rds:DescribeDBClusterParameters",
        "rds:DescribeDBClusters",
        "rds:DescribeDBParameterGroups",
        "rds:DescribeDBParameters",
        "rds:DescribeDBClusterEndpoints",
        "rds:DescribeDBSnapshotAttributes",
        "rds:DescribeDBSnapshots",
        "rds:DescribeDBClusterSnapshots",
        "ec2:DescribeSecurityGroups"
      ],
      "Resource": "*"
    }
  ]
}
```

Now we need to create a new role ```DbDashCollectorRole```with below Trust policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Additionally we need to create a policy ```DbDashCollectorRemotePolicy``` containing arn of role ```DbDashCollectorRemoteRole``` in Remote Account B 
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DbDashCollectorRemoteRole",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::430045346560:role/DbDashCollectorRemoteRole"
    }
  ]
}
```

Now we need to prepare the ec2 instance where the collector script resides. Create instance profile ```DbDashCollectorProfile``` as below execute the below on CloudShell to avoid issues:
```json
aws iam create-instance-profile --instance-profile-name DbDashCollectorProfile
```

After successful creation of profile add role ```DbDashCollectorProfile``` to the instance profile
```json
aws iam add-role-to-instance-profile \
--instance-profile-name DbDashCollectorProfile \
--role-name DbDashCollectorRole
```

As part of final step we need to assign the profile to the ec2, as assigning role to ec2 directly is not possible at this time.
```json
aws ec2 associate-iam-instance-profile \
--instance-id <EC2instanceID> \
--iam-instance-profile Name=<EC2InstanceProfile> 
```

##### Account B
This is remote account where the collector script collects the rds metadata.

Create policy ```DbDashCollectorPolicy``` with below privileges. 
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances",
        "rds:DescribeDBSecurityGroups",
        "rds:DescribeDBClusterParameterGroups",
        "rds:DescribeDBClusterParameters",
        "rds:DescribeDBClusters",
        "rds:DescribeDBParameterGroups",
        "rds:DescribeDBParameters",
        "rds:DescribeDBClusterEndpoints",
        "rds:DescribeDBSnapshotAttributes",
        "rds:DescribeDBSnapshots",
        "rds:DescribeDBClusterSnapshots",
        "ec2:DescribeSecurityGroups"
      ],
      "Resource": "*"
    }
  ]
}
```

Create Role ```DbDashCollectorRemoteRole``` with below policy with arn of the role where the collector scripts resides.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::350437859186:role/DbDashCollectorRole"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
This completes the privileges setup.

#### Verify 

Open a session to the ec2 where the collector resides, and run below commands
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::430045346560:role/DbDashCollectorRemoteRole \
  --role-session-name test > creds.json
```

```bash
ubuntu@ip-172-31-37-234:~$ aws sts assume-role \
  --role-arn arn:aws:iam::430045346560:role/DbDashCollectorRemoteRole \
  --role-session-name test > creds.json
ubuntu@ip-172-31-37-234:~$ cat creds.json
{
    "Credentials": {
        "AccessKeyId": "",
        "SecretAccessKey": "",
        "SessionToken": "",
        "Expiration": "2025-12-19T05:55:12+00:00"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": ":test",
        "Arn": "arn:aws:sts::430045346560:assumed-role/DbDashCollectorRemoteRole/test"
    }
}
ubuntu@ip-172-31-37-234:~$
```

Run below commands to get the STS credentials
```bash
export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' creds.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' creds.json)
export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' creds.json)
```

```bas
ubuntu@ip-172-31-37-234:~$ export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' creds.json)
ubuntu@ip-172-31-37-234:~$ export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' creds.json)
ubuntu@ip-172-31-37-234:~$ export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' creds.json)
ubuntu@ip-172-31-37-234:~$ env | grep AWS
AWS_SECRET_ACCESS_KEY=
AWS_ACCESS_KEY_ID=
AWS_SESSION_TOKEN=
ubuntu@ip-172-31-37-234:~$
```

Finally run below cmd's:
```bash
aws rds describe-db-instances --region us-east-1
```

```bash
ubuntu@ip-172-31-37-234:~$
ubuntu@ip-172-31-37-234:~$ aws rds describe-db-instances --region us-east-1
```

This ensures only that role in Account A can assume this role in Account B.

#### Python requirements
Make you have supported python version (Python 3.12 is recommended.) and make sure you install below packages.
```python
--8<-- "collector/requirements.txt"
```

#### Running Collectr Script
The collector script accepts one argument, which it uses from the ```.env``` file to get the metadata. The ```-awsacct``` argument is from the ```.env``` file ```aws-acct-1=arn:aws:iam::430045346560:role/DbDashCollectorRemoteRole```
```python
(pyvenv) dbdash@ip-172-31-37-234:/workspace/dbdash/dbdash/collector$ python collector.py -awsacct aws-acct-1
2025-12-21 01:11:26,773 | INFO | DbDash Collector | Starting RDS collection job
2025-12-21 01:11:26,773 | INFO | DbDash Collector | Account : aws-acct-1
2025-12-21 01:11:26,773 | INFO | DbDash Collector | Api Username : admin@dbdash.com
```


