from Config import Settings
from Database import MongoDB

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import logging

logger = logging.getLogger("imdb_bot")

settings = Settings()

# MongoDB setup
db = MongoDB()
db.set_collection("university_assignment")

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def render_html_page(request: Request):
    try:
        # Convert the request_id to ObjectId
        response = db.get_by_id(request.query_params.get("request_id"))
        logger.info(response)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Invalid request ID format. Must be a valid MongoDB ObjectId.")

    if not response:
        raise HTTPException(status_code=404, detail="Request not found")

    return templates.TemplateResponse("index.html", {"request": response})

app.mount("/static/", StaticFiles(directory="static"), name="static")


def main():
    import uvicorn
    print("Starting FastAPI server...")
    config = uvicorn.Config(app, host=settings.host,
                            port=settings.port, reload=True)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
