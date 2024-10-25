class ErrorResponse(BaseModel):
    errorCode: str = Field(None)
    message: str = Field(None)
    details: str = Field(None)