import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import users, budgets, currency, categories, operations


app = FastAPI()
app.include_router(users.router)
app.include_router(budgets.router)
app.include_router(currency.router)
app.include_router(categories.router)
app.include_router(operations.router)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=9999,
        workers=1,
    )