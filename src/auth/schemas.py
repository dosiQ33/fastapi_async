from pydantic import BaseModel
from typing import Union, Optional


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenData(BaseModel):
    username: Union[str, None] = None
