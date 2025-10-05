"""Database utility functions for Oracle object-relational operations"""
import oracledb
from typing import Optional, List, Any, Dict


def get_next_id(cursor: oracledb.Cursor, sequence_name: str) -> int:
    """Get next value from an Oracle sequence"""
    cursor.execute(f"SELECT {sequence_name}.NEXTVAL FROM DUAL")
    result = cursor.fetchone()
    return result[0] if result else None


def create_varray(cursor: oracledb.Cursor, type_name: str, values: List[str]) -> Any:
    """Create an Oracle VARRAY object

    Args:
        cursor: Oracle cursor
        type_name: Name of the VARRAY type (e.g., 'AllergyListType')
        values: List of string values

    Returns:
        Oracle VARRAY object
    """
    if not values:
        return None

    obj_type = cursor.connection.gettype(type_name)
    return obj_type.newobject(values)


def varray_to_list(varray: Any) -> List[str]:
    """Convert Oracle VARRAY to Python list

    Args:
        varray: Oracle VARRAY object

    Returns:
        List of strings
    """
    if varray is None:
        return []
    return list(varray.aslist())


def get_donor_by_id(cursor: oracledb.Cursor, donor_id: int) -> Optional[Dict]:
    """Fetch donor by ID and convert to dictionary"""
    query = """
        SELECT d.donor_id,
               d.donor_name,
               d.donor_surname,
               d.donor_date_of_birth,
               d.donor_sex
        FROM Donors d
        WHERE d.donor_id = :donor_id
    """
    cursor.execute(query, {"donor_id": donor_id})
    row = cursor.fetchone()

    if not row:
        return None

    return {
        "donor_id": row[0],
        "donor_name": row[1],
        "donor_surname": row[2],
        "donor_date_of_birth": row[3],
        "donor_sex": row[4]
    }


def get_tissue_by_id(cursor: oracledb.Cursor, tissue_id: int) -> Optional[Dict]:
    """Fetch tissue by ID and convert to dictionary"""
    query = """
        SELECT t.tissue_id,
               t.tissue_name,
               t.tissue_description,
               t.tissue_density,
               t.tissue_is_vital
        FROM Tissues t
        WHERE t.tissue_id = :tissue_id
    """
    cursor.execute(query, {"tissue_id": tissue_id})
    row = cursor.fetchone()

    if not row:
        return None

    return {
        "tissue_id": row[0],
        "tissue_name": row[1],
        "tissue_description": row[2],
        "tissue_density": row[3],
        "tissue_is_vital": row[4]
    }


def get_drug_by_id(cursor: oracledb.Cursor, drug_id: int) -> Optional[Dict]:
    """Fetch drug by ID and convert to dictionary"""
    query = """
        SELECT d.drug_id,
               d.drug_name,
               d.drug_description,
               d.drug_allergies
        FROM Drugs d
        WHERE d.drug_id = :drug_id
    """
    cursor.execute(query, {"drug_id": drug_id})
    row = cursor.fetchone()

    if not row:
        return None

    return {
        "drug_id": row[0],
        "drug_name": row[1],
        "drug_description": row[2],
        "drug_allergies": varray_to_list(row[3])
    }


def get_ref_by_id(cursor: oracledb.Cursor, table_name: str, id_field: str, id_value: int) -> Any:
    """Get a REF to an object by its ID

    Args:
        cursor: Oracle cursor
        table_name: Name of the object table
        id_field: Name of the ID field
        id_value: Value of the ID

    Returns:
        REF to the object
    """
    query = f"""
        SELECT REF(o)
        FROM {table_name} o
        WHERE o.{id_field} = :id_value
    """
    cursor.execute(query, {"id_value": id_value})
    result = cursor.fetchone()
    return result[0] if result else None
