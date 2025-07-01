from fastapi import FastAPI

from .database import engine, Base
from .routers import auth, company_master, counter_guarantee, delivery_procedure, discrepancy, event, health, item_master, liquidated_damages, lot_monitoring, material_performance_guarantee, order_detail, order_event, order_item_detail, performance_guarantee, post_tender_clarification, pre_tender_clarification, product_master, tender_company_item, tendering_companies, tender
from .models import (
    CompanyMaster, CounterGuarantee, DeliveryProcedure, Discrepancy, Event,
    ItemMaster, LiquidatedDamages, LotMonitoring, MaterialPerformanceGuarantee,
    OrderDetail, OrderEvent, OrderItemDetail, PerformanceGuarantee,
    PostTenderClarification, PreTenderClarification, ProductMaster,
    TenderCompanyItem, TenderingCompanies, Tender, User
)

# DEV: auto-create tables; in prod use Alembic migrations
# Base.metadata.create_all(bind=engine)
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