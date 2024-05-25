from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.api.endpoints import critical_rules, firewall_rules, user
from src.common.exceptions.httpexc_provider import IHTTPExceptionProvider

api = FastAPI(
    title='Firewall Rule Prediction API',
    version='1.0.0'
)

api.include_router(critical_rules.router)
api.include_router(firewall_rules.router)
api.include_router(user.router)


@api.get('/')
async def root():
    return RedirectResponse(url='/docs')


origins = ["http://localhost:3000", "http://0.0.0.0:3000"]


api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@api.exception_handler(IHTTPExceptionProvider)
async def handle_db_exceptions(_: Request, exc: IHTTPExceptionProvider):
    http_exc = exc.get_http_exception()
    return JSONResponse(status_code=http_exc.status_code, content={'detail': http_exc.detail})
