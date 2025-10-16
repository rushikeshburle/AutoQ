"""Create a default user for no-auth mode"""
from app.models.database import SessionLocal, init_db
from app.models.user import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_default_user():
    init_db()
    db = SessionLocal()
    
    try:
        # Check if default user exists
        existing_user = db.query(User).filter(User.id == 1).first()
        
        if not existing_user:
            # Create default user with simple password hash
            default_user = User(
                email="default@autoq.local",
                username="default",
                hashed_password=pwd_context.hash("default123"),
                full_name="Default User",
                role=UserRole.INSTRUCTOR,
                is_active=True
            )
            db.add(default_user)
            db.commit()
            print("OK: Default user created successfully!")
            print("   Username: default")
            print("   Password: default123")
        else:
            print("INFO: Default user already exists")
            
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_default_user()
