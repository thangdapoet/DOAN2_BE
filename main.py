from fastapi import FastAPI
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import history

# Create tables if not using Alembic yet (will rely on migrations later)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + SQL Server Demo")

app.include_router(history.router)

# ==== Add CORS middleware ====
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",            # Allowed domains
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE...
    allow_headers=["*"],              # Authorization, Content-Type...
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + SQL Server!"}
