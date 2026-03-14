from app.database import SessionLocal, engine, Base
from app.models.models import Tenant, User
from app.models import models
from app.utils.auth import hash_password

def seed_data():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        existing_tenant = db.query(Tenant).first()
        if existing_tenant:
            print("Data already exists")
            return
        
        tenant = Tenant(
            name="Empresa Demo",
            ruc="12345678901",
            address="Ciudad de Panama",
            phone="+507 0000-0000"
        )
        db.add(tenant)
        db.flush()
        
        admin = User(
            email="admin@contabilidad.com",
            name="Administrador",
            password_hash=hash_password("admin123"),
            tenant_id=tenant.id,
            role="admin"
        )
        db.add(admin)
        db.commit()
        
        print("Seed data created successfully!")
        print(f"Tenant: {tenant.name} (RUC: {tenant.ruc})")
        print(f"Admin user: {admin.email} / admin123")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
