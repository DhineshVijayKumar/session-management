from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.sessions import router as sessionsRouter

app=FastAPI()

origins = [
    "http://localhost:3000",  # Add your frontend's URL here
    "http://127.0.0.1:3000",  # For local dev, if running on different port
]

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(sessionsRouter)

@app.get("/test")
async def read_root():
    return {"message": "Hello from FastAPI!"}

#uvicorn main:app --reload