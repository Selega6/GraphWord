from pydantic import BaseModel


class NodePair(BaseModel):
    source: str
    target: str