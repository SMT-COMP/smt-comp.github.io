from typing import List

from pydantic.main import BaseModel
from pydantic.networks import AnyHttpUrl

class Solver(BaseModel):
    name: str
    authors: List[str]
    url: AnyHttpUrl


