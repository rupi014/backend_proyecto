from sqlalchemy.orm import Session
from models import *
from schemas import *

# Funciones para la gestion de jugadores
def get_players(db: Session):
    return db.query(Players).all()

def get_players_by_id(db: Session, player_id: int):
    return db.query(Players).filter(Players.id == player_id).first()

def create_players(db: Session, players: PlayerData):
    db_players = Players(name=players.name, role=players.role, bio=players.bio, image=players.image, twitter=players.twitter)
    db.add(db_players)
    db.commit()
    db.flush(db_players)
    return db_players

def delete_players(db: Session, player_id: int):
    db_players = db.query(Players).filter(Players.id == player_id).first() 
    if db_players:
        db.delete(db_players)
        db.commit()
        return True
    return False

def update_players(db: Session, player_id: int, players: PlayerData):
    db_players = db.query(Players).filter(Players.id == player_id).first() 
    if db_players:
        db_players.name = players.name
        db_players.role = players.role
        db_players.bio = players.bio
        db_players.image = players.image
        db_players.twitter = players.twitter
        db.commit()
        db.flush(db_players)
        return db_players
    return False