class ServiceRegistration(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    openapi_url: str = Field(...)
    tags: List[str] = Field(None)