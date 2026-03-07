# Architecture

## Overview
DbDash has simple client-server architecture and uses api endpoints to manipulate data. The frontend is developed by react and backend is developed by python.

<pre>
+------------------+        +---------------------+        +--------------------+
|                  |        |                     |        |                    |
|   Data Collector | -----> |     Backend API     | -----> |     Frontend UI    |
|  (Python Service)|        |   (FastAPI, Python) |        |    (React.js)      |
|                  |        |                     |        |                    |
+------------------+        +----------+----------+        +----------+---------+
                                      |                               
                                      |                               
                           +----------v----------+                    
                           |                     |                    
                           |   PostgreSQL DB     |                    
                           | (Partitioned Data)  |                    
                           |                     |                    
                           +---------------------+                    
</pre>


The basic folder structure is as below, and this will be described seperately in different section. The backend and frontend can be seperated and deploued seperately. It's share for overview only during the development of the project.

<pre>
dbdash/
├── backend/
│   ├── src/
│   │   ├── auth/
│   │   ├── rds/
│   │   ├── config.py
│   │   ├── __init__.py
│   │   ├── middleware.py        
│   │   ..... so on
│   ├── .env
│   ├── requirement.txt
│   ├── alembic.ini
│    ..... so on
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ..... so on
│   │   ├── App.jsx
│   │   ├── main.jsx
        ..... so on
</pre>
