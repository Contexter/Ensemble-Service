class TypesenseErrorResponse(BaseModel):
    errorCode: str = Field(...)
    retryAttempt: int = Field(...)
    message: str = Field(...)
    details: str = Field(...)
