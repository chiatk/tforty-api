from fastapi import APIRouter
from sqlalchemy.sql.expression import and_
from ..database.connection_mysql import connect
from ..models.perk import perks
from ..schemas.perk import Perk

conn = connect()
perk = APIRouter()

@perk.post('/perks', tags=["perks"])
def create_perk( perk: Perk ):
    new_perk = {
        "campaing_id": perk.campaing_id,
        "active" : perk.active,
        "title": perk.title,
        "image_url": perk.image_url,
        "price": perk.price,
        "included_items": perk.included_items,
        "description": perk.description,
        "quantity_available": perk.quantity_available,
    }
    result = conn.execute( perks.insert().values(new_perk) )
    return conn.execute(perks.select().where( perks.c.id == result.lastrowid )).first()

@perk.get('/perks/{campaing_id}', tags=["perks"])
def get_perks(campaing_id: int):
    perk = conn.execute( perks.select().where( and_(perks.c.campaing_id == campaing_id, perks.c.active == True ) )).fetchall()
    
    if len(perk) == 0:
        return { "message": "recompensa de la campaña no existe" }

    return perk

@perk.get('/perks/findOne/{id}', tags=["perks"])
def find_one_perk(id: int):
    perk = conn.execute(perks.select().where( perks.c.id == id )).first()
    if perk is None or perk['active'] == False:
        return { "message": "recompensa no existe" }
    return perk

@perk.put('/perks/{id}', tags=["perks"])
def update_perk( perk: Perk, id: int ):
    conn.execute(
        perks.update().values(
            campaing_id= perk.campaing_id,
            active= perk.active,
            title= perk.title,
            image_url= perk.image_url,
            price= perk.price,
            included_items= perk.included_items,
            description= perk.description,
            quantity_available= perk.quantity_available
        ).where( perks.c.id == id )
    )
    return conn.execute( perks.select().where( perks.c.id == id )).first()

@perk.delete('/perks/{id}', tags=["perks"])
def logical_deletion_perk(id: int):
    conn.execute(
        perks.update()
        .values(
            active= False
        )
        .where( perks.c.id == id )
    )
    return { "message": f" Se elimino correctamente perk {id} " }