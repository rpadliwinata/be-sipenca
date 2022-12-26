from fastapi import FastAPI
from deta import Deta


deta = Deta("c09hsnq1_2fYiQJSFaLZsvumyNTeTggexyrE4Mvxb")
db = deta.Base("db_user")

app = FastAPI(title="Sipenca")


@app.get("/")
async def home():
    res = db.fetch()
    
