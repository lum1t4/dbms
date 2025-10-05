from pydantic import BaseModel, Field, field_validator
from typing import Optional


class TissueBase(BaseModel):
    tissue_name: str = Field(..., max_length=100, description="Tissue/organ name")
    tissue_description: str = Field(..., description="Detailed description of the tissue")
    tissue_density: float = Field(..., ge=0, description="Tissue density in g/cm3")
    tissue_is_vital: str = Field(..., max_length=1, description="Is tissue vital for life (Y/N)")

    @field_validator("tissue_is_vital")
    @classmethod
    def validate_is_vital(cls, v: str) -> str:
        if v not in ["Y", "N"]:
            raise ValueError("tissue_is_vital must be 'Y' or 'N'")
        return v


class TissueCreate(TissueBase):
    """Schema for creating a new tissue"""
    pass


class TissueUpdate(TissueBase):
    """Schema for updating an existing tissue"""
    tissue_name: Optional[str] = Field(None, max_length=100)
    tissue_description: Optional[str] = None
    tissue_density: Optional[float] = Field(None, ge=0)
    tissue_is_vital: Optional[str] = Field(None, max_length=1)


class TissueResponse(TissueBase):
    """Schema for tissue response"""
    tissue_id: int = Field(..., description="Unique tissue identifier")

    class Config:
        from_attributes = True
