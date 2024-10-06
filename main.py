from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.databases import SessionLocal, Base, engine
from models.user import UserModel, UserCreate, User
from typing import List
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio
    Base.metadata.create_all(bind=engine)
    yield
    # Aquí puedes agregar lógica para el cierre, si es necesario

# Asignar el manejador de eventos de lifespan
app = FastAPI(lifespan=lifespan)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return {'mensaje': 'Bienvenidos a la API de Usuarios'}

# Endpoint para obtener todos los usuarios
@app.get('/user/', response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

#Endpoint para tener 1 solo usuario por id
@app.get('/user/{user_id}', response_model=User)
def read_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user

#Endpoint para tener 1 solo usuario por nombre
@app.get('/user/{user_name}', response_model=User)
def read_users(user_name: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.name == user_name).first()
    return user


# Endpoint para crear un nuevo usuario
@app.post('/user/', response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Endpoint para actualizar un usuario existente
@app.put('/user/{user_id}', response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in user.model_dump().items():  # Cambiar dict() a model_dump()
        setattr(db_user, key, value)
    db.commit()
    return db_user

# Endpoint para borrar un usuario
@app.delete('/user/{user_id}', response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return db_user

@app.get("/favicon.ico")
async def favicon():
    return {}