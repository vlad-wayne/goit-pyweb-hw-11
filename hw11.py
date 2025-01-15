from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


DATABASE_URL = "postgresql://user:password@localhost:5432/contacts_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date)
    extra_info = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    extra_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


def create_contact(db, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db):
    return db.query(Contact).all()


app = FastAPI()

@app.post("/contacts/", response_model=ContactResponse)
def create_contact_endpoint(contact: ContactCreate, db = Depends(get_db)):
    return create_contact(db, contact)

@app.get("/contacts/", response_model=list[ContactResponse])
def read_contacts(db = Depends(get_db)):
    return get_contacts(db)
