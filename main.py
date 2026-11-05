from fastapi import FastAPI

from routes import solicitudes, responsables, reportes

app = FastAPI()

app.include_router(solicitudes.router)
app.include_router(responsables.router)
app.include_router(reportes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
