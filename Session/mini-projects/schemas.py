from pydantic import BaseModel, Field, field_validator

class ToDoList(BaseModel):
    name : str          = Field(..., min_length=2)
    status : str
    percentage : float  = Field(..., ge=0, le=100)

    @field_validator("status")
    def status_must_be_valid(cls, value : str):
        striped_value = value.lower().strip()
        if striped_value != "open" and striped_value != "in-progress" and striped_value != "completed":
            raise ValueError("Status must be open, in-progress, or completed")
        return value

    @field_validator("percentage")
    def percentage_must_match_status(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Percentage must be between 0 and 100")
        return value
