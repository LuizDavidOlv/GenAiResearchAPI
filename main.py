import logging
import uvicorn
from fastapi import FastAPI, Request
from src.api import routers as routers_dict

app = FastAPI(
    title = "Summarization API",
    version = "1.0.0",
    docs_url = '/docs',
    #root_path = "summarization"
)

for version, routers in routers_dict.items():
    for router in routers:
        app.include_router(router, prefix=f"/{version}")

        
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080)
