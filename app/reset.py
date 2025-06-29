# In a Python shell or a quick script
from .database import engine, Base
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)