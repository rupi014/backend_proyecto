from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PlayerData
import crud.players_crud as players_crud
from database import engine, SessionLocal
from models import Base

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close

router = APIRouter(prefix="/players", tags=["Players"], responses={404: {"description": "No encontrado"}})  

Base.metadata.create_all(bind=engine)

@router.post("/", response_model=PlayerData)
async def create_players(players: PlayerData, db: Session = Depends(get_db)):
    check_players = players_crud.get_players_by_id(db, player_id=players.id)
    if check_players:
        raise HTTPException(status_code=400, detail="El jugador ya existe")
    return players_crud.create_players(db=db, players=players)

@router.get("/", response_model=list[PlayerData])
async def get_players(db: Session = Depends(get_db)):
    players = players_crud.get_players(db)
    if not players:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores")
    return players

@router.get("/{players_id}", response_model=PlayerData)
async def get_players_by_id(players_id: int, db: Session = Depends(get_db)):
    players = players_crud.get_players_by_id(db, players_id)
    if not players:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return players

@router.delete("/{players_id}", response_model=dict)
async def delete_players(players_id: int, db: Session = Depends(get_db)):
    success = players_crud.delete_players(db, players_id)
    if not success:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": f"Jugador con ID {players_id} eliminado correctamente"}       

@router.put("/{players_id}", response_model=PlayerData)
async def update_players(players_id: int, players: PlayerData, db: Session = Depends(get_db)):
    updated_players = players_crud.update_players(db, players_id, players)
    if not updated_players:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return updated_players


