from pydantic import BaseModel

class ConnectivityFilter(BaseModel):
    min_degree: int
    max_degree: int = None 
