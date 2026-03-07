# Environment Variables

This section describes the different format of env files the application uses, i.e. for api, collector and seeding data in application for demo.

.apienv
```bash
DATABASE_URL=postgresql+asyncpg://username:password@db:5432/dbdash
JWT_SECRET=SomeSecret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRY=3600
REFRESH_TOKEN_EXPIRY=2
FILE_DIRECTORY = "uploadfiles"
FILE_DIRECTORY_DP = "uploadfiles/dpicture"
FILE_DIRECTORY_DP_EXPOSE = "/static/profile/img"
```
.seedenv
```bash
aws-acct-1=arn:aws:iam::430066545360:role/DbDashCollectorRemoteRole
aws-acct-2=arn:aws:iam::357674324541:role/DbDashCollectorRole

RDSAPI_URL = "/aws/rds/instance"
RDSMAPAPI_URL = "/aws/rds/instance/map"
RDSPARAMSAPI_URL = "/aws/rds/instance/parameter"
RDSSECRULESAPI_URL = "/aws/rds/instance/secrules"
API_USERNAME = "admin@dbdash.com"
API_PASSWORD = "Test@1234"
API_TOKEN_URL = "http://host:port/api/v1/auth/login"
API_AZ_URL = "http://host:port/api/v1/aws/org/byaccount"
API_BASE_URL = "http://host:port/api/v1"
```
