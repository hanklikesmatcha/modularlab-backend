import json
from fastapi import FastAPI, Request
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware
from routers import users, items

from database import Base, engine

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3001",
    "http://0.0.0.0:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)

Base.metadata.create_all(bind=engine)

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {"code": 500, "message": f"Internal Server Error - {exc}"}
        ),
    )

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
