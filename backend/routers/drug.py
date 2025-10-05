"""Drug CRUD endpoints"""
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
import oracledb

from backend.models.drug import DrugCreate, DrugResponse, DrugUpdate
from backend.db_utils import get_drug_by_id, create_varray, varray_to_list

router = APIRouter(prefix="/api/drugs", tags=["drugs"])


@router.post("", response_model=DrugResponse, status_code=201)
async def create_drug(drug: DrugCreate, request: Request):
    """Create a new drug"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Get next drug_id from sequence
        cursor.execute("SELECT drug_seq.NEXTVAL FROM DUAL")
        drug_id = cursor.fetchone()[0]

        # Create VARRAY for allergies
        allergies_varray = None
        if drug.drug_allergies:
            allergies_varray = create_varray(cursor, "AllergyListType", drug.drug_allergies)

        # Insert using object type constructor
        insert_query = """
            INSERT INTO Drugs VALUES (
                DrugType(
                    :drug_id,
                    :drug_name,
                    :drug_description,
                    :drug_allergies
                )
            )
        """
        cursor.execute(
            insert_query,
            {
                "drug_id": drug_id,
                "drug_name": drug.drug_name,
                "drug_description": drug.drug_description,
                "drug_allergies": allergies_varray,
            },
        )
        request.app.state.connection.commit()

        # Fetch and return the created drug
        created_drug = get_drug_by_id(cursor, drug_id)
        return DrugResponse(**created_drug)

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("", response_model=dict)
async def get_drugs(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    search: Optional[str] = None,
):
    """Get all drugs with optional filtering"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Build query with optional filters
        where_clause = ""
        params = {}

        if search:
            where_clause = "WHERE UPPER(d.drug_name) LIKE UPPER(:search)"
            params["search"] = f"%{search}%"

        # Get total count
        count_query = f"SELECT COUNT(*) FROM Drugs d {where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]

        # Get drugs (use literal values for OFFSET/FETCH as Oracle doesn't support bind params there)
        query = f"""
            SELECT d.drug_id,
                   d.drug_name,
                   d.drug_description,
                   d.drug_allergies
            FROM Drugs d
            {where_clause}
            ORDER BY d.drug_id
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """
        cursor.execute(query, params)

        drugs = []
        for row in cursor:
            drugs.append(
                {
                    "drug_id": row[0],
                    "drug_name": row[1],
                    "drug_description": row[2],
                    "drug_allergies": varray_to_list(row[3]),
                }
            )

        return {"total": total, "drugs": drugs}

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("/{drug_id}", response_model=DrugResponse)
async def get_drug(drug_id: int, request: Request):
    """Get a specific drug by ID"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        drug = get_drug_by_id(cursor, drug_id)

        if not drug:
            raise HTTPException(status_code=404, detail=f"Drug with ID {drug_id} not found")

        return DrugResponse(**drug)

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.put("/{drug_id}", response_model=DrugResponse)
async def update_drug(drug_id: int, drug: DrugUpdate, request: Request):
    """Update an existing drug"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Check if drug exists
        existing = get_drug_by_id(cursor, drug_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Drug with ID {drug_id} not found")

        # Build update query for only provided fields
        update_fields = []
        params = {"drug_id": drug_id}

        if drug.drug_name is not None:
            update_fields.append("d.drug_name = :drug_name")
            params["drug_name"] = drug.drug_name

        if drug.drug_description is not None:
            update_fields.append("d.drug_description = :drug_description")
            params["drug_description"] = drug.drug_description

        if drug.drug_allergies is not None:
            update_fields.append("d.drug_allergies = :drug_allergies")
            allergies_varray = create_varray(cursor, "AllergyListType", drug.drug_allergies)
            params["drug_allergies"] = allergies_varray

        if not update_fields:
            # No fields to update, return existing drug
            return DrugResponse(**existing)

        update_query = f"""
            UPDATE Drugs d
            SET {', '.join(update_fields)}
            WHERE d.drug_id = :drug_id
        """
        cursor.execute(update_query, params)
        request.app.state.connection.commit()

        # Fetch and return updated drug
        updated_drug = get_drug_by_id(cursor, drug_id)
        return DrugResponse(**updated_drug)

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.delete("/{drug_id}", status_code=204)
async def delete_drug(drug_id: int, request: Request):
    """Delete a drug"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Check if drug exists
        existing = get_drug_by_id(cursor, drug_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Drug with ID {drug_id} not found")

        # Delete drug
        delete_query = "DELETE FROM Drugs d WHERE d.drug_id = :drug_id"
        cursor.execute(delete_query, {"drug_id": drug_id})
        request.app.state.connection.commit()

        return None

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
