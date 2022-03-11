from fastapi import FastAPI
import uvicorn

from depart.routes import position


def prepare_application(debug=False):
    app = FastAPI(debug=debug)
    app.include_router(position.router)
    return app


def run_server():
    app = prepare_application()
    uvicorn.run(
        app,
        host="0.0.0.0",
        # port=config.port,
    )
