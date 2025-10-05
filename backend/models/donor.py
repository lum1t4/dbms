from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional


class DonorBase(BaseModel):
    donor_name: str = Field(..., max_length=100, description="Donor's first name")
    donor_surname: str = Field(..., max_length=100, description="Donor's surname")
    donor_date_of_birth: date = Field(..., description="Donor's date of birth")
    donor_sex: str = Field(..., max_length=1, description="Donor's sex")

    @field_validator("donor_sex")
    @classmethod
    def validate_sex(cls, v: str) -> str:
        allowed_values = ["M", "F", "X"]
        if v not in allowed_values:
            raise ValueError(f"donor_sex must be one of {allowed_values}")
        return v


class DonorCreate(DonorBase):
    """Schema for creating a new donor"""
    pass


class DonorUpdate(DonorBase):
    """Schema for updating an existing donor"""
    donor_name: Optional[str] = Field(None, max_length=100)
    donor_surname: Optional[str] = Field(None, max_length=100)
    donor_date_of_birth: Optional[date] = None
    donor_sex: Optional[str] = Field(None, max_length=10)


class DonorResponse(DonorBase):
    """Schema for donor response"""
    donor_id: int = Field(..., description="Unique donor identifier")

    class Config:
        from_attributes = True
