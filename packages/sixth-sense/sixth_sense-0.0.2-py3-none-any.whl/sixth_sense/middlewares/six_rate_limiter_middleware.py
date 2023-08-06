from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi import FastAPI,Depends,Response,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import time
import json
from sixth_sense import schemas
import re
import requests
from dotenv import load_dotenv
import os
import ast


class SixRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, apikey: str, fastapi_app: FastAPI, project_config: schemas.ProjectConfig):
        super().__init__(app)
        self._config = project_config
        self._log_dict = {}
        self._app = app
        self._apikey = apikey
        for route in fastapi_app.routes:
            new_route = re.sub(r'\W+', '~', route.path)
            self._log_dict[str(new_route)] = {}

    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}
        request._receive = receive
        
    def _is_rate_limit_reached(self, uid, route):
        timestamp = time.time()
        requests = self._log_dict[route].get(uid, None)
        rate_limit = self._config.rate_limiter[route].rate_limit
        interval = self._config.rate_limiter[route].interval
        if requests == None:
            self._log_dict[route][uid] = []
        if len(self._log_dict[route].get(uid)) < rate_limit:
            self._log_dict[route].get(uid, []).append(timestamp)
            return True
            
        new_req = [new_req for new_req in self._log_dict[route][uid] if new_req > timestamp-interval]
        
        if len(new_req) < rate_limit:
            self._log_dict[route][uid].append(timestamp)
            return True
        else: 
            self._log_dict[route][uid].append(timestamp)
            return False
        
    async def _parse_bools(self, string: bytes)-> str:
        string = string.decode("utf-8")
        string = string.replace(' ', "")
        string = string.replace('true,', "True,")
        string = string.replace(",true", "True,")
        string = string.replace('false,', "False,")
        string = string.replace(",false", "False,")
        out=ast.literal_eval(string)
        return out
        
    async def dispatch(self,request: Request,call_next) -> None:
        host = request.client.host
        route = request.scope["path"]
        route = re.sub(r'\W+', '~', route)
        print(route)
        rate_limit_resp = requests.get("https://backend.withsix.co/project-config/config/get-route-rate-limit/"+self._apikey+"/"+route)
        print(rate_limit_resp.json())        

        if rate_limit_resp.status_code == 200:
            rate_limit = schemas.RateLimiter.parse_obj(rate_limit_resp.json())
            print(self._config," config is bte" ,rate_limit, route)
            self._config.rate_limiter[route] = rate_limit
            preferred_id = host if self._config.rate_limiter[route].unique_id == "" or self._config.rate_limiter[route].unique_id == "host" else body[self._config.rate_limiter[route].unique_id]
            _response = await call_next(request)
            if self._is_rate_limit_reached(preferred_id, route): 
                return _response
            else:
                output={
                    "message": "max request reached"
                }
                _response.headers["content-length"]= str(len(str(output).encode()))
                return Response(json.dumps(output), status_code=401, headers=_response.headers)
        else:
            output={
                    "message": "something went wrong"
                }
            _response.headers["content-length"]= str(len(str(output).encode()))
            return Response(json.dumps(output), status_code=500)