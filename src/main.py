from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.api.v1.routes_cars import router as cars_router
from src.api.v1.routes_uploads import router as uploads_router

app = FastAPI(title="Car Recommender API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    # Redirect root to Swagger UI
    return RedirectResponse(url="/docs")

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

app.include_router(cars_router, prefix="/api/v1/cars", tags=["cars"])
app.include_router(uploads_router, prefix="/api/v1/upload", tags=["uploads"])
