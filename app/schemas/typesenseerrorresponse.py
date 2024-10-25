class TypesenseErrorResponse(BaseModel):
    errorCode: str = Field(None)
    retryAttempt: int = Field(None)
    message: str = Field(None)
    details: str = Field(None)