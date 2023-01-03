import uvicorn
from v1.router import router as v1
from v2.router import router as v2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="Sipenca",
    version="0.0.1",
    prefix="/api"
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://sipenca.my.id"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse("https://0f9vta.deta.dev/docs")


app.include_router(v2)

if __name__ == "__main__":
    uvicorn.run(app)

