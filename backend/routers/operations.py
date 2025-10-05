"""Special operation endpoints as per WHO requirements"""
from fastapi import APIRouter, HTTPException, Request, Query
import oracledb

from backend.db_utils import varray_to_list

router = APIRouter(prefix="/api/operations", tags=["operations"])


@router.get("/tissues-by-density")
async def get_tissues_by_density(
    request: Request,
    max_density: float = Query(..., description="Maximum density threshold"),
):
    """
    Operation 2: Print all organs and tissues below a certain density threshold
    Frequency: Once a month
    """
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        query = """
            SELECT t.tissue_id,
                   t.tissue_name,
                   t.tissue_description,
                   t.tissue_density,
                   t.tissue_is_vital
            FROM Tissues t
            WHERE t.tissue_density < :max_density
            ORDER BY t.tissue_density ASC
        """
        cursor.execute(query, {"max_density": max_density})

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

        return {
            "threshold": max_density,
            "count": len(tissues),
            "tissues": tissues,
        }

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("/cure-details/{cure_id}")
async def get_cure_details(cure_id: int, request: Request):
    """
    Operation 3: Request information on a specific cure, its list of drugs and possible linked allergies
    Frequency: Once a day
    """
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Query based on the SQL from README
        query = """
            SELECT cu.cure_id,
                   DEREF(VALUE(d)).drug_id         AS drug_id,
                   DEREF(VALUE(d)).drug_name       AS drug_name,
                   DEREF(VALUE(d)).drug_description AS drug_description,
                   DEREF(VALUE(d)).drug_allergies  AS drug_allergies
            FROM   Cures cu,
                   TABLE(cu.cure_composition) d
            WHERE  cu.cure_id = :cure_id
        """
        cursor.execute(query, {"cure_id": cure_id})

        drugs = []
        all_allergies = set()

        for row in cursor:
            allergies = varray_to_list(row[4])
            drugs.append(
                {
                    "drug_id": row[1],
                    "drug_name": row[2],
                    "drug_description": row[3],
                    "drug_allergies": allergies,
                }
            )
            all_allergies.update(allergies)

        if not drugs:
            raise HTTPException(status_code=404, detail=f"Cure with ID {cure_id} not found")

        return {
            "cure_id": cure_id,
            "drugs": drugs,
            "all_allergies": sorted(list(all_allergies)),
        }

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("/donors-vital-disease")
async def get_donors_vital_disease(
    request: Request,
    disease_id: int = Query(..., description="The specific disease to filter by"),
):
    """
    Operation 4: Print all donors with a specific disease affecting only organs/tissue required for life
    for which the system provided useful suggestions as future works
    Frequency: Once a month
    """
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Query based on the SQL from README
        query = """
            SELECT DISTINCT
                DEREF(A.condition.donor_ref).donor_id AS donor_id,
                DEREF(A.condition.donor_ref).donor_name AS donor_name,
                DEREF(A.condition.donor_ref).donor_surname AS donor_surname,
                DEREF(A.condition.donor_ref).donor_date_of_birth AS donor_date_of_birth,
                DEREF(A.condition.donor_ref).donor_sex AS donor_sex,
                DEREF(A.condition.tissue_ref).tissue_id AS tissue_id,
                DEREF(A.condition.tissue_ref).tissue_name AS tissue_name,
                DEREF(A.condition.tissue_ref).tissue_is_vital AS tissue_is_vital,
                DEREF(A.condition.condition_disease).disease_name AS disease_name
            FROM (
              SELECT DEREF(VALUE(f)) AS condition
              FROM FutureWorks fw,
                   TABLE(fw.future_work_suggested_by) f
            ) A
            WHERE
            DEREF(A.condition.tissue_ref).tissue_is_vital = 'Y'
            AND DEREF(A.condition.condition_disease).disease_id = :disease_id
        """
        cursor.execute(query, {"disease_id": disease_id})

        donors_map = {}
        disease_name = None

        for row in cursor:
            donor_id = row[0]
            disease_name = row[8]

            if donor_id not in donors_map:
                donors_map[donor_id] = {
                    "donor_id": donor_id,
                    "donor_name": row[1],
                    "donor_surname": row[2],
                    "donor_date_of_birth": row[3],
                    "donor_sex": row[4],
                    "affected_vital_tissues": [],
                }

            # Add tissue if not already added
            tissue_id = row[5]
            if not any(t["tissue_id"] == tissue_id for t in donors_map[donor_id]["affected_vital_tissues"]):
                donors_map[donor_id]["affected_vital_tissues"].append(
                    {
                        "tissue_id": tissue_id,
                        "tissue_name": row[6],
                        "tissue_is_vital": row[7],
                    }
                )

        return {
            "disease_id": disease_id,
            "disease_name": disease_name,
            "donors": list(donors_map.values()),
        }

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()


@router.get("/top-researchers-suggestions")
async def get_top_researchers_suggestions(
    request: Request,
    quality: str = Query("top", regex="^(top|middle|low)$", description="Journal quality filter"),
):
    """
    Operation 5: Print all useful suggestions provided to only researchers with top quality journals published
    Frequency: Once a month
    """
    cursor: oracledb.Cursor = request.app.state.connection.cursor()

    try:
        # Query based on the SQL from README
        query = """
            SELECT r.researcher_id,
                   r.researcher_name,
                   r.researcher_surname,
                   r.researcher_email,
                   r.researcher_institution,
                   p.publication_doi,
                   p.publication_title,
                   p.publication_journal,
                   p.publication_journal_quality,
                   fw.future_work_id,
                   fw.future_work_description
            FROM   Publications p,
                   TABLE(p.publication_authors) auth_tab,
                   Researchers r,
                   TABLE(r.researcher_recommended_works) rw,
                   FutureWorks fw
            WHERE  r.researcher_id = DEREF(VALUE(auth_tab)).researcher_id
              AND  fw.future_work_id = DEREF(VALUE(rw)).future_work_id
              AND  p.publication_journal_quality = :quality
        """
        cursor.execute(query, {"quality": quality})

        researchers_map = {}

        for row in cursor:
            researcher_id = row[0]

            if researcher_id not in researchers_map:
                researchers_map[researcher_id] = {
                    "researcher_id": researcher_id,
                    "researcher_name": row[1],
                    "researcher_surname": row[2],
                    "researcher_email": row[3],
                    "researcher_institution": row[4],
                    "top_publications": [],
                    "suggested_future_works": [],
                }

            # Add publication if not already added
            pub_doi = row[5]
            if not any(p["publication_doi"] == pub_doi for p in researchers_map[researcher_id]["top_publications"]):
                researchers_map[researcher_id]["top_publications"].append(
                    {
                        "publication_doi": pub_doi,
                        "publication_title": row[6],
                        "publication_journal": row[7],
                        "publication_journal_quality": row[8],
                    }
                )

            # Add future work if not already added
            fw_id = row[9]
            if not any(fw["future_work_id"] == fw_id for fw in researchers_map[researcher_id]["suggested_future_works"]):
                researchers_map[researcher_id]["suggested_future_works"].append(
                    {
                        "future_work_id": fw_id,
                        "future_work_description": row[10],
                    }
                )

        return {
            "journal_quality": quality,
            "researchers": list(researchers_map.values()),
        }

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
