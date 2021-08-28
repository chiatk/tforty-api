from fastapi import FastAPI
from .routes.user import user
from .routes.campaign import campaign
from .routes.perk import perk
from .routes.donation import donation

app = FastAPI()

@app.get('/')
def main():
    return { "message": "Welcome to the api" }

app.include_router(user)
app.include_router(campaign)
app.include_router(perk)
app.include_router(donation)