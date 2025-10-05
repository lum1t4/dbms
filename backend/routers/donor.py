"""Donor CRUD endpoints"""
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
import oracledb

from backend.models.donor import DonorCreate, DonorResponse, DonorUpdate
from backend.db_utils import get_donor_by_id

router = APIRouter(prefix="/api/donors", tags=["donors"])


@router.post("", response_model=DonorResponse, status_code=201)
async def create_donor(donor: DonorCreate, request: Request):
    """Create a new donor (Operation 1 equivalent for donors)"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Get next donor_id from sequence
        cursor.execute("SELECT donor_seq.NEXTVAL FROM DUAL")
        donor_id = cursor.fetchone()[0]

        # Insert using object type constructor
        insert_query = """
            INSERT INTO Donors VALUES (
                DonorType(
                    :donor_id,
                    :donor_name,
                    :donor_surname,
                    :donor_date_of_birth,
                    :donor_sex
                )
            )
        """
        cursor.execute(
            insert_query,
            {
                "donor_id": donor_id,
                "donor_name": donor.donor_name,
                "donor_surname": donor.donor_surname,
                "donor_date_of_birth": donor.donor_date_of_birth,
                "donor_sex": donor.donor_sex,
            },
        )
        request.app.state.connection.commit()

        # Fetch and return the created donor
        created_donor = get_donor_by_id(cursor, donor_id)
        return DonorResponse(**created_donor)

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("", response_model=dict)
async def get_donors(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sex: Optional[str] = None,
):
    """Get all donors with optional filtering"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Build query with optional filters
        where_clause = ""
        params = {}

        if sex:
            where_clause = "WHERE d.donor_sex = :sex"
            params["sex"] = sex

        # Get total count
        count_query = f"SELECT COUNT(*) FROM Donors d {where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]

        # Get donors (use literal values for OFFSET/FETCH as Oracle doesn't support bind params there)
        query = f"""
            SELECT d.donor_id,
                   d.donor_name,
                   d.donor_surname,
                   d.donor_date_of_birth,
                   d.donor_sex
            FROM Donors d
            {where_clause}
            ORDER BY d.donor_id
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """
        cursor.execute(query, params)

        donors = []
        for row in cursor:
            donors.append(
                {
                    "donor_id": row[0],
                    "donor_name": row[1],
                    "donor_surname": row[2],
                    "donor_date_of_birth": row[3],
                    "donor_sex": row[4],
                }
            )

        return {"total": total, "donors": donors}

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("/{donor_id}", response_model=DonorResponse)
async def get_donor(donor_id: int, request: Request):
    """Get a specific donor by ID"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        donor = get_donor_by_id(cursor, donor_id)

        if not donor:
            raise HTTPException(status_code=404, detail=f"Donor with ID {donor_id} not found")

        return DonorResponse(**donor)

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.put("/{donor_id}", response_model=DonorResponse)
async def update_donor(donor_id: int, donor: DonorUpdate, request: Request):
    """Update an existing donor"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Check if donor exists
        existing = get_donor_by_id(cursor, donor_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Donor with ID {donor_id} not found")

        # Build update query for only provided fields
        update_fields = []
        params = {"donor_id": donor_id}

        if donor.donor_name is not None:
            update_fields.append("d.donor_name = :donor_name")
            params["donor_name"] = donor.donor_name

        if donor.donor_surname is not None:
            update_fields.append("d.donor_surname = :donor_surname")
            params["donor_surname"] = donor.donor_surname

        if donor.donor_date_of_birth is not None:
            update_fields.append("d.donor_date_of_birth = :donor_date_of_birth")
            params["donor_date_of_birth"] = donor.donor_date_of_birth

        if donor.donor_sex is not None:
            update_fields.append("d.donor_sex = :donor_sex")
            params["donor_sex"] = donor.donor_sex

        if not update_fields:
            # No fields to update, return existing donor
            return DonorResponse(**existing)

        update_query = f"""
            UPDATE Donors d
            SET {', '.join(update_fields)}
            WHERE d.donor_id = :donor_id
        """
        cursor.execute(update_query, params)
        request.app.state.connection.commit()

        # Fetch and return updated donor
        updated_donor = get_donor_by_id(cursor, donor_id)
        return DonorResponse(**updated_donor)

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.delete("/{donor_id}", status_code=204)
async def delete_donor(donor_id: int, request: Request):
    """Delete a donor"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Check if donor exists
        existing = get_donor_by_id(cursor, donor_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Donor with ID {donor_id} not found")

        # Delete donor
        delete_query = "DELETE FROM Donors d WHERE d.donor_id = :donor_id"
        cursor.execute(delete_query, {"donor_id": donor_id})
        request.app.state.connection.commit()

        return None

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
