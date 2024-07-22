from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker, registry
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()
IP_DB = os.getenv("IP_DB")

engine = create_engine(f'mysql+pymysql://root@{IP_DB}:3306/cinema')
mapper_registy = registry()
Base = mapper_registy.generate_base()
Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()

class Body(BaseModel):
    titulo: str
    genero: str
    ano: int

class Filmes(Base):
    __tablename__ = "filmes"

    titulo = Column(String, primary_key=True)
    genero = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Filme [titulo={self.titulo}, ano={self.ano}]"


@app.get("/")
async def get():
    data = session.query(Filmes).all()
    return (data)

@app.post("/")
async def post(body : Body):
    data_insert = Filmes(titulo=body.titulo, genero=body.genero, ano= body.ano)
    session.add(data_insert)
    session.commit()

@app.delete("/")
async def delete(body : Body):
    session.query(Filmes).filter(Filmes.titulo==body.titulo).delete()
    session.commit()    

@app.put("/titulo={titulo}")
async def put(body: Body,titulo):
    session.query(Filmes).filter(Filmes.titulo==titulo).update({"titulo":body.titulo,"genero":body.genero,"ano":body.ano})
    session.commit()
