from src.api.v1.controllers.summarization_controller import router as summarize_router
from src.api.v1.controllers.health_controller import router as health_router

routers = [summarize_router, health_router]