from fastapi import APIRouter, Body, Depends, Security, status
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder