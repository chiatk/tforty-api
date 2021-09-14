from typing import Any, Dict, List
import base64
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..database.connection_mysql import connect
from ..models.user import users
from ..schemas.user import User, ResUser, ResListUser, ErrorUser, LoginUser, UpdateUser
from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session

from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()
key = base64.urlsafe_b64encode(b'\xbf\xd8\xf8\xaf`d0\x80\xdf\xc4\xc11\xdf\xc5se\xbfz\xafS\x12\x1a.\xa2\xe8\x04S\xb6\x85;\xa3\xff')
f = Fernet(key) 
conn: Session = connect()


@user.post('/users', tags=["users"], response_model=ResUser)
def create_user(user: User) -> Dict:
    try:
        new_user = {
            "name": user.name,
            "email": user.email,
            "chia_wallet": user.chia_wallet,
            "balance": user.balance,
            "active": user.active
        }
        new_user["hash_pw"] = f.encrypt(bytes(user.hash_pw,'utf-8'))
        result = conn.execute(users.insert().values(new_user))

        return { "status": True, "data": conn.execute(users.select().where(users.c.id == result.lastrowid)).first() }
 
    
    except SQLAlchemyError as error:
        print( { "Error": "mysql", "nameFunction": "create_user", "message": error.statement, "code": error.code } )
        raise HTTPException(status_code=422, detail="Error al crear usuario")



@user.get('/users', tags=["users"], response_model=ResListUser, responses={422: {"model": ErrorUser, "description": "Error list users"}})
def get_users() -> ResListUser:
    try:
        listUsers = conn.execute( users.select().where( users.c.active == True )  ).fetchall()
        if len(listUsers) ==  0:
            return JSONResponse(status_code=422, content={"status": False, "message": "lista de usuarios vacia" })


        return ResListUser(status=True, data=listUsers )
    except SQLAlchemyError as error:
        print( { "Error": "mysql", "name": "get_users", "message": error.statement, "code": error.code } )
        return JSONResponse(status_code=422, content={"status": False, "message": "Error al listar usuarios" })

@user.get('/users/{id}', tags=["users"], response_model=ResUser)
def get_one_user(id: int) -> Dict:
    try:
        user = conn.execute( users.select().where( users.c.id == id ) ).first()
        if user is None or user['active'] == False:
            return JSONResponse(status_code=400, content={"status": False, "message": "usuario no existe" })


        return ResUser(status= True, data= user)
    except SQLAlchemyError as error:
        print( { "Error": "mysql", "name": "get_one_user", "message": error } )
        return JSONResponse(status_code=400, content={"status": False, "message": "problema con el usuario" })

@user.post('/users/login', tags=["users"])
def login_user(loginUser: LoginUser):

    try:
        print( f"email-> {loginUser.email}" )
        if loginUser.email is None or loginUser.password is None:
            return { "status": -1, "message": "completa los campos requeridos" }

        profile = conn.execute( users.select().where( users.c.email == loginUser.email ) ).first()
        print(f"profile-> {profile}")

        if profile is None:
            return { "status": -1, "message": "el perfil no existe" }

        if profile['active'] == False:
            return { "status": -1, "message": "usuario no valido" }
        
    
   
        hash_pw = f.decrypt(bytes(profile.hash_pw,'utf-8'))

        if loginUser.password != hash_pw.decode():
            return { "status": -1, "message": "problemas con email o password" }
        

        return { "status": 1, "data": profile }
        
    except InvalidToken:
        return { "status": -1, "message": "token no valido, actualiza tu contraseña" }

    

# @user.delete('/delete/user/{id}')
# def delete_user(id: str):
#     conn.execute( users.delete().where( users.c.id == id ) )
#     return Response(status_code=HTTP_204_NO_CONTENT, )

@user.delete('/users/{id}', tags=["users"])
def logical_deletion_user(id: int) -> Dict:
    try:
        conn.execute(
            users.update()
            .values(
                active= False
            )
            .where( users.c.id == id )
        )
        return { "status": 1, "message": f" Se elimino correctamente usuario {id} " }
    except SQLAlchemyError as error:
        print( { "Error": "mysql", "name": "logical_deletion_user", "message": error } )
        return { "status": -1, "data": False }


@user.put('/users/{id}', tags=["users"])
def update_user(user: UpdateUser, id: int) -> Dict:
    try:
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
        return { "status": 1, "data": conn.execute( users.select().where( users.c.id == id ) ).first()}
    except SQLAlchemyError as error:
        print( { "Error": "mysql", "name": "update_user", "message": error } )
        return { "status": -1, "data": False }