# DBDash – Full Stack Installation Guide

This document explains how to install, build, and run the complete DBDash stack using Docker and Docker Compose.

## Stack Overview

The stack consists of:

* UI: React (Vite) served by Nginx
* API: Backend service (FastAPI / Flask )
* Database: PostgreSQL
* Reverse Proxy: Nginx (inside UI container)
* Container Orchestration: Docker Compose

```text
dbdash/
├── docker-compose.yml
├── databse/                # PostgreSQL (custom image)
│   ├── Dockerfile
│   └── init-seed/
│       └── init_seed.sql
├── backend/             # API service
│   ├── Dockerfile
│   ├── .env
│   └── src/
├── frontend/            # React (Vite) UI
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── .env
│   ├── .env.production
│   └── src/
```

## Prerequisites

Ensure the following are installed:
* Docker ≥ 24.x
* Docker Compose ≥ v2
* Git

Verify installation:

```bash
docker --version
docker compose version
git --version
```

## Environment Configuration
### Backend & Database Environment

Create or edit:
```backend/.env```

Example:
```bash
DATABASE_URL=postgresql+asyncpg://apiuser:supersecret@192.168.96.128:5432/dbdash
JWT_SECRET=A3f9C7bE1D4aF082
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRY=3600
REFRESH_TOKEN_EXPIRY=2
FILE_DIRECTORY = "uploadfiles"
FILE_DIRECTORY_DP = "uploadfiles/dpicture"
FILE_DIRECTORY_DP_EXPOSE = "/static/profile/img"
```
Adjust the envs accordingly. FILE_* can be ignored for this version, it still needs some functionality which is still being worked on.

### Frontend Environment (Vite)
Create or edit:
```frontend/.env```

Example:
```bash
VITE_API_URL=http://localhost:8000/api/v1
```

## Docker Compose Configuration

Key services:

* db → PostgreSQL
* api → Backend API
* ui → React + Nginx frontend

All services run on the same Docker bridge network.

## Custom Installation
DbDash can be installed seperately without using docker too. For this you need do this seperately and update the configs (mostly env's) accordingly. 

If you want to have database in seperate, then the env for api should be populated with correct host, port and database details.

If you want to have api in seperate host, make sure you have python version >= 3.11 and all the packages in requirement.txt are installed and database should be reachable through to the specified port.

If you want to have ui/frontend to be in seperate host, then you need to do the following:

1. make sure node.js is installed with version >=20.x
2. install nginx
3. install all the nodejs dependencies (package.json)
4. Export the VITE_API_URL environment variable, pointing to api endpoint.
5. Build the app using npm
6. Copy the build nginx directory
7. Configure the nginx config
8. Start the nginx service

## Seed the database with custom data.
The repo comes with a script to seed the database with temporary data, which can be used to check the funcationality of the entire stack and later the data can be truncated. The Script creates a temporary container and runs the data load job and cleanups everything.

To seed the database with temporary data, you need to run the script with below command, which was discussed in quick installation. 
```bash
./dbdash.sh seed
```

### Prerequisite for seeding.
Environment file will be needed containing the api endpoints and credentials to work and seed the data and its format should look like below:
```bash
RDSAPI_URL = ""
RDSPARAMS_URL = ""
RDSSECRULES_URL = ""
API_USERNAME = "admin@dbdash.com"
API_PASSWORD = "Test@1234"
API_TOKEN_URL = "http://api:8000/api/v1/auth/login"
API_AZ_URL = "http://api:8000/api/v1/aws/org/byaccount"
API_BASE_URL = "http://api:8000/api/v1"
```

The data seeded are completely random but they comply with the motive with which the app was made.