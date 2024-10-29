class ErrorResponse(BaseModel):
    errorCode: str = Field(...)
    message: str = Field(...)
    details: str = Field(...)
