import contextlib
import uvicorn
from fastapi import FastAPI
from db.database import create_test_db_and_tables
from api import routers


# @contextlib.asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_test_db_and_tables()
#     yield


app = FastAPI()

app.include_router(router=routers.auth_router, prefix="/auth", tags=["auth"])
app.include_router(router=routers.task_router, prefix="/api", tags=["Tasks"])
app.include_router(router=routers.task_history_router, prefix="/api", tags=["Task History"])

    

if __name__  == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
    )
