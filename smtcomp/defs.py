from typing import List

from pydantic.main import BaseModel
from pydantic.networks import AnyHttpUrl


class Submission(BaseModel):
    name: str
    authors: List[str]
    url: AnyHttpUrl
