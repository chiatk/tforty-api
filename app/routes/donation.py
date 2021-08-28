from fastapi import APIRouter
from sqlalchemy.sql.expression import and_
from ..database.connection_mysql import conn
from ..models.donation import donations
from ..schemas.donation import Donation

donation = APIRouter()

@donation.post('/donations')
def create_donation( donation: Donation ):
    new_donation = {
        "campaing_id": donation.campaing_id,
        "user_id": donation.user_id,
        "perk_id": donation.perk_id,
        "amount": donation.amount,
        "state_id" : donation.state_id
    }
    result = conn.execute( donations.insert().values(new_donation) )
    return conn.execute(donations.select().where( donations.c.id == result.lastrowid )).first()


@donation.get('/donations/{user_id}')
def get_donations(user_id: int):
    donation = conn.execute( donations.select().where( and_(donations.c.user_id == user_id, donations.c.state_id == 1))).fetchall()
    if len(donation) == 0:
        return { "message": "donation del usuario no existe" }
    return donation


@donation.get('/donations/findOne/{id}')
def find_one_donation(id: int):
    donation = conn.execute(donations.select().where( donations.c.id == id )).first()
    if donation is None or donation['state_id'] == 0:
        return { "message": "donation no existe" }
    return donation


@donation.put('/donations/{id}')
def update_donation( donation: Donation, id: int ):
    conn.execute(
        donations.update().values(
            campaing_id= donation.campaing_id,
            user_id= donation.user_id,
            perk_id= donation.perk_id,
            amount= donation.amount,
            state_id= donation.state_id
        ).where( donations.c.id == id )
    )
    return conn.execute( donations.select().where( donations.c.id == id )).first()

@donation.delete('/donations/{id}')
def logical_deletion_donation(id: int):
    conn.execute(
        donations.update()
        .values(
            state_id= 0
        )
        .where( donations.c.id == id )
    )
    return { "message": f" Se elimino correctamente donación {id} " }