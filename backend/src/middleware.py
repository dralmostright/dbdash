from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

#logger = logging.getLogger('uvicorn.access')
#logger.disabled = True
def register_middleware(api: FastAPI):
    
    @api.middleware('http')
    async def custom_logging(request:Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time= time.time()-start_time
        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} - time taken {processing_time}s"
        print(message)
        return response
    """    
    allow_origins=[
    "http://localhost:5173",
    "http://10.0.4.15:5173",
    ]
    """

    api.add_middleware(
        CORSMiddleware,
        allow_origins= ["*"],
        allow_methods= ["*"],
        allow_headers = ["*"],
        allow_credentials=True
    )
    
    api.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]
    )