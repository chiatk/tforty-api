from fastapi import APIRouter
from ..database.connection_mysql import conn
from ..models.perk import perks
from ..schemas.perk import Perk

perk = APIRouter()

@perk.post('/perks')
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

@perk.get('/perks/{campaing_id}')
def get_perks(campaing_id: int):
    return conn.execute( perks.select().where( perks.c.campaing_id == campaing_id )).fetchall()

@perk.get('/perks/findOne/{id}')
def find_one_perk(id: int):
    return conn.execute(perks.select().where( perks.c.id == id )).first()

@perk.put('/perks/{id}')
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

@perk.delete('/perks/{id}')
def logical_deletion_perk(id: int):
    conn.execute(
        perks.update()
        .values(
            active= False
        )
        .where( perks.c.id == id )
    )
    return { "message": f" Se elimino correctamente perk {id} " }