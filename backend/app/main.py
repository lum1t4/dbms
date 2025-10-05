import oracledb
import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import donor_router, tissue_router, drug_router, operations_router

dotenv.load_dotenv()


DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABSE_DSN = os.environ.get("DATABSE_DSN")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.connection = oracledb.connect(user=DATABASE_USER, password=DATABASE_PASSWORD, dsn=DATABSE_DSN)
    yield
    app.state.connection.close()


app = FastAPI(title="WHO Backend", version="1.0.0", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(donor_router)
app.include_router(tissue_router)
app.include_router(drug_router)
app.include_router(operations_router)


@app.get('/')
async def health():
    from datetime import timezone
    cursor: oracledb.Cursor = app.state.connection.cursor()
    cursor.execute("SELECT sysdate FROM dual")
    ts, = cursor.fetchone()
    return {"status": f"alive UTC {ts.astimezone(timezone.utc)}"}
