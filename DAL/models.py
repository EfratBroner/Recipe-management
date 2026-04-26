from pydantic import BaseModel

class Recipe(BaseModel):
    id: int | None = None
    name: str
    category: str
    ingredients: str
    instructions: str
    prep_time: int
