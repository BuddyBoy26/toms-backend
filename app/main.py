from fastapi import FastAPI

from .database import engine, Base
from .routers import health, tender, auth, company_master, item_master, product_master, tendering_companies, tender_company_item, order_detail, order_item_detail
from .models import (
    User,
    CompanyMaster,
    ProductMaster,
    ItemMaster,
    Tender,
    TenderingCompanies,
    TenderCompanyItem,
    OrderDetail,
    OrderItemDetail
)

# DEV: auto-create tables; in prod use Alembic migrations
Base.metadata.create_all(bind=engine)
print("Database tables created.")

app = FastAPI(title="Tender Backend")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(tender.router, prefix="/api")
app.include_router(product_master.router, prefix="/api")
app.include_router(company_master.router, prefix="/api")
app.include_router(item_master.router, prefix="/api")
app.include_router(tendering_companies.router, prefix="/api")
app.include_router(tender_company_item.router, prefix="/api")
app.include_router(order_detail.router, prefix="/api")
app.include_router(order_item_detail.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)