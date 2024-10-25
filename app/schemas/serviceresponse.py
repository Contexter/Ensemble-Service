class ServiceResponse(BaseModel):
    id: str = Field(None)
    name: str = Field(None)
    description: str = Field(None)
    openapi_url: str = Field(None)
    tags: List[str] = Field(None)