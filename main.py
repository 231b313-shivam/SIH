# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "postgresql://username:password@localhost/migrant_health"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Migrant Health Records API")

# ------------------ Database Models ------------------
class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    aadhaar_id = Column(String, unique=True, index=True)
    language = Column(String, default="Hindi")

class HealthRecord(Base):
    __tablename__ = "health_records"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    doctor_name = Column(String, nullable=False)
    diagnosis = Column(Text)
    prescription = Column(Text)

Base.metadata.create_all(bind=engine)

# ------------------ Schemas ------------------
class WorkerCreate(BaseModel):
    name: str
    aadhaar_id: str
    language: str

class RecordCreate(BaseModel):
    worker_id: int
    doctor_name: str
    diagnosis: str
    prescription: str

# ------------------ Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ Routes ------------------
@app.post("/register_worker/")
def register_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    new_worker = Worker(**worker.dict())
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return {"msg": "Worker registered", "worker": new_worker.id}

@app.post("/add_record/")
def add_record(record: RecordCreate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == record.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    new_record = HealthRecord(**record.dict())
    db.add(new_record)
    db.commit()
    return {"msg": "Health record added"}

@app.get("/worker/{worker_id}")
def get_worker_records(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    records = db.query(HealthRecord).filter(HealthRecord.worker_id == worker_id).all()
    return {"worker": worker.name, "language": worker.language, "records": records}
