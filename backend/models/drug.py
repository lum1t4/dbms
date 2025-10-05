from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class DrugBase(BaseModel):
    drug_name: str = Field(..., max_length=200, description="Drug name")
    drug_description: str = Field(..., description="Detailed description of the drug")
    drug_allergies: List[str] = Field(
        default_factory=list,
        max_length=50,
        description="List of possible allergies (max 50 items)"
    )

    @field_validator("drug_allergies")
    @classmethod
    def validate_allergies_length(cls, v: List[str]) -> List[str]:
        if len(v) > 50:
            raise ValueError("drug_allergies cannot contain more than 50 items (VARRAY limit)")
        for allergy in v:
            if len(allergy) > 200:
                raise ValueError(f"Each allergy must be max 200 characters, got {len(allergy)}")
        return v


class DrugCreate(DrugBase):
    """Schema for creating a new drug"""
    pass


class DrugUpdate(DrugBase):
    """Schema for updating an existing drug"""
    drug_name: Optional[str] = Field(None, max_length=200)
    drug_description: Optional[str] = None
    drug_allergies: Optional[List[str]] = None


class DrugResponse(DrugBase):
    """Schema for drug response"""
    drug_id: int = Field(..., description="Unique drug identifier")

    class Config:
        from_attributes = True
