"""Tissue CRUD endpoints"""
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
import oracledb

from backend.models.tissue import TissueCreate, TissueResponse, TissueUpdate
from backend.db_utils import get_tissue_by_id

router = APIRouter(prefix="/api/tissues", tags=["tissues"])


@router.post("", response_model=TissueResponse, status_code=201)
async def create_tissue(tissue: TissueCreate, request: Request):
    """Create a new tissue/organ (Operation 1: Recording an organ or tissue - 10 times a day)"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Get next tissue_id from sequence
        cursor.execute("SELECT tissue_seq.NEXTVAL FROM DUAL")
        tissue_id = cursor.fetchone()[0]

        # Insert using object type constructor
        insert_query = """
            INSERT INTO Tissues VALUES (
                TissueType(
                    :tissue_id,
                    :tissue_name,
                    :tissue_description,
                    :tissue_density,
                    :tissue_is_vital
                )
            )
        """
        cursor.execute(
            insert_query,
            {
                "tissue_id": tissue_id,
                "tissue_name": tissue.tissue_name,
                "tissue_description": tissue.tissue_description,
                "tissue_density": tissue.tissue_density,
                "tissue_is_vital": tissue.tissue_is_vital,
            },
        )
        request.app.state.connection.commit()

        # Fetch and return the created tissue
        created_tissue = get_tissue_by_id(cursor, tissue_id)
        return TissueResponse(**created_tissue)

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("", response_model=dict)
async def get_tissues(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    is_vital: Optional[str] = Query(None, regex="^[YN]$"),
    max_density: Optional[float] = None,
):
    """Get all tissues with optional filtering"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Build query with optional filters
        where_clauses = []
        params = {}

        if is_vital:
            where_clauses.append("t.tissue_is_vital = :is_vital")
            params["is_vital"] = is_vital

        if max_density is not None:
            where_clauses.append("t.tissue_density < :max_density")
            params["max_density"] = max_density

        where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        # Get total count
        count_query = f"SELECT COUNT(*) FROM Tissues t {where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]

        # Get tissues (use literal values for OFFSET/FETCH as Oracle doesn't support bind params there)
        query = f"""
            SELECT t.tissue_id,
                   t.tissue_name,
                   t.tissue_description,
                   t.tissue_density,
                   t.tissue_is_vital
            FROM Tissues t
            {where_clause}
            ORDER BY t.tissue_id
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """
        cursor.execute(query, params)

        tissues = []
        for row in cursor:
            tissues.append(
                {
                    "tissue_id": row[0],
                    "tissue_name": row[1],
                    "tissue_description": row[2],
                    "tissue_density": row[3],
                    "tissue_is_vital": row[4],
                }
            )

        return {"total": total, "tissues": tissues}

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("/{tissue_id}", response_model=TissueResponse)
async def get_tissue(tissue_id: int, request: Request):
    """Get a specific tissue by ID"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        tissue = get_tissue_by_id(cursor, tissue_id)

        if not tissue:
            raise HTTPException(status_code=404, detail=f"Tissue with ID {tissue_id} not found")

        return TissueResponse(**tissue)

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.put("/{tissue_id}", response_model=TissueResponse)
async def update_tissue(tissue_id: int, tissue: TissueUpdate, request: Request):
    """Update an existing tissue"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Check if tissue exists
        existing = get_tissue_by_id(cursor, tissue_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Tissue with ID {tissue_id} not found")

        # Build update query for only provided fields
        update_fields = []
        params = {"tissue_id": tissue_id}

        if tissue.tissue_name is not None:
            update_fields.append("t.tissue_name = :tissue_name")
            params["tissue_name"] = tissue.tissue_name

        if tissue.tissue_description is not None:
            update_fields.append("t.tissue_description = :tissue_description")
            params["tissue_description"] = tissue.tissue_description

        if tissue.tissue_density is not None:
            update_fields.append("t.tissue_density = :tissue_density")
            params["tissue_density"] = tissue.tissue_density

        if tissue.tissue_is_vital is not None:
            update_fields.append("t.tissue_is_vital = :tissue_is_vital")
            params["tissue_is_vital"] = tissue.tissue_is_vital

        if not update_fields:
            # No fields to update, return existing tissue
            return TissueResponse(**existing)

        update_query = f"""
            UPDATE Tissues t
            SET {', '.join(update_fields)}
            WHERE t.tissue_id = :tissue_id
        """
        cursor.execute(update_query, params)
        request.app.state.connection.commit()

        # Fetch and return updated tissue
        updated_tissue = get_tissue_by_id(cursor, tissue_id)
        return TissueResponse(**updated_tissue)

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.delete("/{tissue_id}", status_code=204)
async def delete_tissue(tissue_id: int, request: Request):
    """Delete a tissue"""
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Check if tissue exists
        existing = get_tissue_by_id(cursor, tissue_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Tissue with ID {tissue_id} not found")

        # Delete tissue
        delete_query = "DELETE FROM Tissues t WHERE t.tissue_id = :tissue_id"
        cursor.execute(delete_query, {"tissue_id": tissue_id})
        request.app.state.connection.commit()

        return None

    except oracledb.DatabaseError as e:
        request.app.state.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
