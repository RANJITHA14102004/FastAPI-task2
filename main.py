from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Todo, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()


@app.post("/todos")
def create_todo(task: str, db: Session = Depends(get_db)):
    todo = Todo(task=task, done=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/todos/{id}")
def update_todo(id: int, task: str, done: bool, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.task = task
    todo.done = done
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
