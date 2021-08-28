from fastapi import APIRouter
from ..database.connection_mysql import conn
from ..models.user import users
from ..schemas.user import User
from cryptography.fernet import Fernet, InvalidToken
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key) 

@user.post('/users')
def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email,
        "chia_wallet": user.chia_wallet,
        "balance": user.balance,
        "active": user.active
    }
    new_user["hash_pw"] = f.encrypt(bytes(user.hash_pw,'utf-8'))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get('/users')
def get_users():
    return conn.execute( users.select() ).fetchall()

@user.get('/users/{id}')
def get_one_user(id: str):
    return conn.execute( users.select().where( users.c.id == id ) ).first()

@user.post('/users/login')
def login_user(email: str, password: str):

    try:
        if email is None or password is None:
            return { "message": "completa los campos requeridos" }

        profile = conn.execute( users.select().where( users.c.email == email ) ).first()
        print(f"profile-> {profile}")

        if profile is None:
            return { "message": "el perfil no existe" }

        if profile['active'] == False:
            return { "message": "usuario no valido" }
        
    
   
        hash_pw = f.decrypt(bytes(profile.hash_pw,'utf-8'))

        if password != hash_pw.decode():
            return { "message": "problemas con email o password" }
        

        return { "data": profile }
        
    except InvalidToken:
        return { "message": "token no valido, actualiza tu contraseña" }

    

@user.delete('/delete/user/{id}')
def delete_user(id: str):
    conn.execute( users.delete().where( users.c.id == id ) )
    return Response(status_code=HTTP_204_NO_CONTENT, )

@user.delete('/users/{id}')
def logical_deletion_user(id: str):
    conn.execute(
        users.update()
        .values(
            active= False
        )
        .where( users.c.id == id )
    )
    return { "message": f" Se elimino correctamente usuario {id} " }

@user.put('/users/{id}')
def update_user(user: User, id: int):
    conn.execute(
        users.update()
        .values(
            name=user.name,
            email=user.email,
            hash_pw=f.encrypt(bytes(user.hash_pw,'utf-8')),
            chia_wallet= user.chia_wallet,
            balance= user.balance,
            active= user.active
        )
        .where( users.c.id == id )
    )
    return conn.execute( users.select().where( users.c.id == id ) ).first()