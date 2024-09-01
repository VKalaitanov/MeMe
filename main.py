# API Python
# Сторонние API
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Наши API
from oauth.oauth import router as oauth
from swipe.swipe import router as swipe

app = FastAPI()
app.include_router(router=oauth, prefix='/user')
app.include_router(router=swipe, prefix='/swipe')


@app.get('/')
def main():
    return {"success": "Hello world"}


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=5000, reload=True)
