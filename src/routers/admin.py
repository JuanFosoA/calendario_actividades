from fastapi import APIRouter, Body, status, Query, Path
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from src.auth.has_access import security
from fastapi.responses import JSONResponse
from typing import List
from src.config.database import SessionLocal
from src.schemas.UserSchema import Admin
from fastapi.encoders import jsonable_encoder
from src.auth import auth_handler
