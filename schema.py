from pydantic import BaseModel


class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_type: str
    notes: str


class InteractionResponse(BaseModel):
    interaction_id: int
    hcp_id: int
    interaction_type: str
    notes: str
    summary: str

    class Config:
        orm_mode = True