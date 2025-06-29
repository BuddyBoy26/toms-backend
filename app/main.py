from fastapi import FastAPI
from .database import engine, Base
from .routers import health, tenders, auth, company_master
from . import models

# DEV: auto-create tables; in prod use Alembic migrations
Base.metadata.create_all(bind=engine)
print("Database tables created.")

app = FastAPI(title="Tender Backend")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(tenders.router, prefix="/api")
app.include_router(company_master.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)