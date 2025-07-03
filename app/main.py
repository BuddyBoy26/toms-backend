from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, company_master, counter_guarantee, delivery_procedure, discrepancy, event, health, item_master, liquidated_damages, lot_monitoring, material_performance_guarantee, order_detail, order_event, order_item_detail, performance_guarantee, post_tender_clarification, pre_tender_clarification, product_master, tender_company_item, tendering_companies, tender, user
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

origins = [
    "http://localhost:3000",   # your Next.js dev server
    # "https://your-production-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # or ["*"] to allow any origin
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Authorization, Content-Type, etc.
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(company_master.router, prefix="/api/company_master")
app.include_router(counter_guarantee.router, prefix="/api/counter_guarantee")
app.include_router(delivery_procedure.router, prefix="/api/delivery_procedure")
app.include_router(discrepancy.router, prefix="/api/discrepancy")
app.include_router(event.router, prefix="/api/event")
app.include_router(health.router, prefix="/api/health")
app.include_router(item_master.router, prefix="/api/item_master")
app.include_router(liquidated_damages.router, prefix="/api/liquidated_damages")
app.include_router(lot_monitoring.router, prefix="/api/lot_monitoring")
app.include_router(material_performance_guarantee.router, prefix="/api/material_performance_guarantee")
app.include_router(order_detail.router, prefix="/api/order_detail")
app.include_router(order_event.router, prefix="/api/order_event")
app.include_router(order_item_detail.router, prefix="/api/order_item_detail")
app.include_router(performance_guarantee.router, prefix="/api/performance_guarantee")
app.include_router(post_tender_clarification.router, prefix="/api/post_tender_clarification")
app.include_router(pre_tender_clarification.router, prefix="/api/pre_tender_clarification")
app.include_router(product_master.router, prefix="/api/product_master")
app.include_router(tender_company_item.router, prefix="/api/tender_company_item")
app.include_router(tendering_companies.router, prefix="/api/tendering_companies")
app.include_router(tender.router, prefix="/api/tender")
app.include_router(user.router, prefix="/api/user")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)