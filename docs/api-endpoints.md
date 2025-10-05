# WHO Database API Endpoints Design

## Overview

This document describes the REST API endpoints for the WHO disease monitoring system. The API provides CRUD operations for all entities and implements the 5 specific operations required.

## Base URL
```
http://localhost:8000
```

## Authentication
TBD (consider adding API key or OAuth2 later)

---

## 1. Donor Endpoints

### Create Donor
```
POST /api/donors
```
**Request Body:**
```json
{
  "donor_name": "John",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "Male"
}
```
**Response:** `201 Created`
```json
{
  "donor_id": 1,
  "donor_name": "John",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "Male"
}
```

### Get All Donors
```
GET /api/donors
```
**Query Parameters:**
- `limit` (optional, default: 100)
- `offset` (optional, default: 0)
- `sex` (optional, filter by sex)

**Response:** `200 OK`
```json
{
  "total": 150,
  "donors": [
    {
      "donor_id": 1,
      "donor_name": "John",
      "donor_surname": "Doe",
      "donor_date_of_birth": "1990-05-15",
      "donor_sex": "Male"
    }
  ]
}
```

### Get Donor by ID
```
GET /api/donors/{donor_id}
```
**Response:** `200 OK`
```json
{
  "donor_id": 1,
  "donor_name": "John",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "Male"
}
```

### Update Donor
```
PUT /api/donors/{donor_id}
```
**Request Body:**
```json
{
  "donor_name": "John",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "Male"
}
```
**Response:** `200 OK`

### Delete Donor
```
DELETE /api/donors/{donor_id}
```
**Response:** `204 No Content`

---

## 2. Tissue Endpoints

### Create Tissue
```
POST /api/tissues
```
**Request Body:**
```json
{
  "tissue_name": "Heart",
  "tissue_description": "Pumps blood through the body",
  "tissue_density": 1.05,
  "tissue_is_vital": "Y"
}
```
**Response:** `201 Created`
```json
{
  "tissue_id": 1,
  "tissue_name": "Heart",
  "tissue_description": "Pumps blood through the body",
  "tissue_density": 1.05,
  "tissue_is_vital": "Y"
}
```

### Get All Tissues
```
GET /api/tissues
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `is_vital` (optional, "Y" or "N")
- `max_density` (optional, filter tissues below this density)

**Response:** `200 OK`
```json
{
  "total": 50,
  "tissues": [
    {
      "tissue_id": 1,
      "tissue_name": "Heart",
      "tissue_description": "Pumps blood through the body",
      "tissue_density": 1.05,
      "tissue_is_vital": "Y"
    }
  ]
}
```

### Get Tissue by ID
```
GET /api/tissues/{tissue_id}
```
**Response:** `200 OK`

### Update Tissue
```
PUT /api/tissues/{tissue_id}
```
**Request Body:** Same as Create
**Response:** `200 OK`

### Delete Tissue
```
DELETE /api/tissues/{tissue_id}
```
**Response:** `204 No Content`

---

## 3. Drug Endpoints

### Create Drug
```
POST /api/drugs
```
**Request Body:**
```json
{
  "drug_name": "Aspirin",
  "drug_description": "Pain reliever and anti-inflammatory",
  "drug_allergies": ["Salicylate sensitivity", "Asthma"]
}
```
**Response:** `201 Created`
```json
{
  "drug_id": 1,
  "drug_name": "Aspirin",
  "drug_description": "Pain reliever and anti-inflammatory",
  "drug_allergies": ["Salicylate sensitivity", "Asthma"]
}
```

### Get All Drugs
```
GET /api/drugs
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `search` (optional, search by name)

**Response:** `200 OK`
```json
{
  "total": 200,
  "drugs": [
    {
      "drug_id": 1,
      "drug_name": "Aspirin",
      "drug_description": "Pain reliever and anti-inflammatory",
      "drug_allergies": ["Salicylate sensitivity", "Asthma"]
    }
  ]
}
```

### Get Drug by ID
```
GET /api/drugs/{drug_id}
```
**Response:** `200 OK`

### Update Drug
```
PUT /api/drugs/{drug_id}
```
**Request Body:** Same as Create
**Response:** `200 OK`

### Delete Drug
```
DELETE /api/drugs/{drug_id}
```
**Response:** `204 No Content`

---

## 4. Cure Endpoints

### Create Cure
```
POST /api/cures
```
**Request Body:**
```json
{
  "cure_composition": [1, 3, 5]  // Array of drug_ids
}
```
**Response:** `201 Created`
```json
{
  "cure_id": 1,
  "cure_composition": [
    {
      "drug_id": 1,
      "drug_name": "Aspirin",
      "drug_description": "Pain reliever",
      "drug_allergies": ["Salicylate sensitivity"]
    },
    {
      "drug_id": 3,
      "drug_name": "Ibuprofen",
      "drug_description": "Anti-inflammatory",
      "drug_allergies": []
    }
  ]
}
```

### Get All Cures
```
GET /api/cures
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)

**Response:** `200 OK`
```json
{
  "total": 75,
  "cures": [
    {
      "cure_id": 1,
      "cure_composition": [...]
    }
  ]
}
```

### Get Cure by ID (with full drug details)
```
GET /api/cures/{cure_id}
```
**Response:** `200 OK`
```json
{
  "cure_id": 1,
  "cure_composition": [
    {
      "drug_id": 1,
      "drug_name": "Aspirin",
      "drug_description": "Pain reliever",
      "drug_allergies": ["Salicylate sensitivity"]
    }
  ]
}
```

### Update Cure
```
PUT /api/cures/{cure_id}
```
**Request Body:**
```json
{
  "cure_composition": [1, 2, 4]  // Updated drug_ids
}
```
**Response:** `200 OK`

### Delete Cure
```
DELETE /api/cures/{cure_id}
```
**Response:** `204 No Content`

---

## 5. Disease Endpoints

### Create Disease
```
POST /api/diseases
```
**Request Body:**
```json
{
  "disease_name": "COVID-19",
  "disease_discovery": "2019-12-01T00:00:00",
  "disease_description": "Respiratory illness caused by SARS-CoV-2",
  "disease_treatable": "Y",
  "disease_cure_ref": 1  // cure_id, optional
}
```
**Response:** `201 Created`
```json
{
  "disease_id": 1,
  "disease_name": "COVID-19",
  "disease_discovery": "2019-12-01T00:00:00",
  "disease_description": "Respiratory illness caused by SARS-CoV-2",
  "disease_treatable": "Y",
  "disease_cure": {
    "cure_id": 1,
    "cure_composition": [...]
  }
}
```

### Get All Diseases
```
GET /api/diseases
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `treatable` (optional, "Y" or "N")
- `search` (optional, search by name)

**Response:** `200 OK`
```json
{
  "total": 120,
  "diseases": [
    {
      "disease_id": 1,
      "disease_name": "COVID-19",
      "disease_discovery": "2019-12-01T00:00:00",
      "disease_description": "...",
      "disease_treatable": "Y",
      "disease_cure": {...}
    }
  ]
}
```

### Get Disease by ID
```
GET /api/diseases/{disease_id}
```
**Response:** `200 OK`

### Update Disease
```
PUT /api/diseases/{disease_id}
```
**Request Body:** Same as Create
**Response:** `200 OK`

### Delete Disease
```
DELETE /api/diseases/{disease_id}
```
**Response:** `204 No Content`

---

## 6. Condition Endpoints

### Create Condition
```
POST /api/conditions
```
**Request Body:**
```json
{
  "condition_status": "disease",  // "control" or "disease"
  "condition_disease": 1,  // disease_id, optional
  "donor_ref": 1,  // donor_id
  "tissue_ref": 1,  // tissue_id
  "treatment_ref": 1,  // cure_id, optional
  "treatment_effect": "improved"  // "improved", "worsened", "neutral"
}
```
**Response:** `201 Created`
```json
{
  "condition_id": 1,
  "condition_status": "disease",
  "condition_disease": {
    "disease_id": 1,
    "disease_name": "COVID-19",
    ...
  },
  "donor": {
    "donor_id": 1,
    "donor_name": "John",
    ...
  },
  "tissue": {
    "tissue_id": 1,
    "tissue_name": "Heart",
    ...
  },
  "treatment": {
    "cure_id": 1,
    ...
  },
  "treatment_effect": "improved"
}
```

### Get All Conditions
```
GET /api/conditions
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `status` (optional, "control" or "disease")
- `donor_id` (optional)
- `disease_id` (optional)
- `tissue_id` (optional)
- `treatment_effect` (optional)

**Response:** `200 OK`

### Get Condition by ID
```
GET /api/conditions/{condition_id}
```
**Response:** `200 OK`

### Update Condition
```
PUT /api/conditions/{condition_id}
```
**Request Body:** Same as Create
**Response:** `200 OK`

### Delete Condition
```
DELETE /api/conditions/{condition_id}
```
**Response:** `204 No Content`

---

## 7. Future Work Endpoints

### Create Future Work
```
POST /api/future-works
```
**Request Body:**
```json
{
  "future_work_description": "Investigate combination therapy with drugs X and Y",
  "future_work_suggested_by": [1, 2, 5]  // Array of condition_ids
}
```
**Response:** `201 Created`
```json
{
  "future_work_id": 1,
  "future_work_description": "Investigate combination therapy with drugs X and Y",
  "future_work_suggested_by": [
    {
      "condition_id": 1,
      "condition_status": "disease",
      ...
    }
  ]
}
```

### Get All Future Works
```
GET /api/future-works
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `search` (optional, search in description)

**Response:** `200 OK`

### Get Future Work by ID
```
GET /api/future-works/{future_work_id}
```
**Response:** `200 OK`

### Update Future Work
```
PUT /api/future-works/{future_work_id}
```
**Request Body:** Same as Create
**Response:** `200 OK`

### Delete Future Work
```
DELETE /api/future-works/{future_work_id}
```
**Response:** `204 No Content`

---

## 8. Researcher Endpoints

### Create Researcher
```
POST /api/researchers
```
**Request Body:**
```json
{
  "researcher_name": "Jane",
  "researcher_surname": "Smith",
  "researcher_email": "jane.smith@example.com",
  "researcher_institution": "MIT",
  "researcher_recommended_works": [1, 2]  // Array of future_work_ids
}
```
**Response:** `201 Created`
```json
{
  "researcher_id": 1,
  "researcher_name": "Jane",
  "researcher_surname": "Smith",
  "researcher_email": "jane.smith@example.com",
  "researcher_institution": "MIT",
  "researcher_recommended_works": [
    {
      "future_work_id": 1,
      "future_work_description": "...",
      ...
    }
  ]
}
```

### Get All Researchers
```
GET /api/researchers
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `institution` (optional)
- `search` (optional, search by name)

**Response:** `200 OK`

### Get Researcher by ID
```
GET /api/researchers/{researcher_id}
```
**Response:** `200 OK`

### Update Researcher
```
PUT /api/researchers/{researcher_id}
```
**Request Body:** Same as Create
**Response:** `200 OK`

### Delete Researcher
```
DELETE /api/researchers/{researcher_id}
```
**Response:** `204 No Content`

---

## 9. Publication Endpoints

### Create Publication
```
POST /api/publications
```
**Request Body:**
```json
{
  "publication_doi": "10.1234/example.2024",
  "publication_title": "Novel Treatment Approaches for COVID-19",
  "publication_journal": "Nature Medicine",
  "publication_year": 2024,
  "publication_journal_quality": "top",  // "top", "middle", "low"
  "publication_authors": [1, 2, 3],  // Array of researcher_ids
  "publication_proposed_works": [1, 2]  // Array of future_work_ids
}
```
**Response:** `201 Created`
```json
{
  "publication_doi": "10.1234/example.2024",
  "publication_title": "Novel Treatment Approaches for COVID-19",
  "publication_journal": "Nature Medicine",
  "publication_year": 2024,
  "publication_journal_quality": "top",
  "publication_authors": [
    {
      "researcher_id": 1,
      "researcher_name": "Jane",
      "researcher_surname": "Smith",
      ...
    }
  ],
  "publication_proposed_works": [
    {
      "future_work_id": 1,
      "future_work_description": "...",
      ...
    }
  ]
}
```

### Get All Publications
```
GET /api/publications
```
**Query Parameters:**
- `limit` (optional)
- `offset` (optional)
- `year` (optional)
- `journal_quality` (optional, "top", "middle", "low")
- `search` (optional, search by title or journal)

**Response:** `200 OK`

### Get Publication by DOI
```
GET /api/publications/{doi}
```
**Note:** DOI should be URL-encoded
**Response:** `200 OK`

### Update Publication
```
PUT /api/publications/{doi}
```
**Request Body:** Same as Create (excluding DOI)
**Response:** `200 OK`

### Delete Publication
```
DELETE /api/publications/{doi}
```
**Response:** `204 No Content`

---

## 10. Special Operations

### Operation 1: Record Tissue/Organ
```
POST /api/tissues
```
**Note:** This is the standard Create Tissue endpoint (see section 2)
**Frequency:** 10 times/day

---

### Operation 2: Get Tissues Below Density Threshold
```
GET /api/operations/tissues-by-density
```
**Query Parameters:**
- `max_density` (required, float) - Maximum density threshold

**Example:**
```
GET /api/operations/tissues-by-density?max_density=1.0
```

**Response:** `200 OK`
```json
{
  "threshold": 1.0,
  "count": 15,
  "tissues": [
    {
      "tissue_id": 2,
      "tissue_name": "Lung",
      "tissue_description": "...",
      "tissue_density": 0.26,
      "tissue_is_vital": "Y"
    },
    {
      "tissue_id": 5,
      "tissue_name": "Fat tissue",
      "tissue_description": "...",
      "tissue_density": 0.92,
      "tissue_is_vital": "N"
    }
  ]
}
```
**Frequency:** Once/month

---

### Operation 3: Get Cure Details with Drugs and Allergies
```
GET /api/operations/cure-details/{cure_id}
```
**Example:**
```
GET /api/operations/cure-details/1
```

**Response:** `200 OK`
```json
{
  "cure_id": 1,
  "drugs": [
    {
      "drug_id": 1,
      "drug_name": "Aspirin",
      "drug_description": "Pain reliever and anti-inflammatory",
      "drug_allergies": [
        "Salicylate sensitivity",
        "Asthma"
      ]
    },
    {
      "drug_id": 3,
      "drug_name": "Ibuprofen",
      "drug_description": "NSAID anti-inflammatory",
      "drug_allergies": [
        "NSAID hypersensitivity"
      ]
    }
  ],
  "all_allergies": [
    "Salicylate sensitivity",
    "Asthma",
    "NSAID hypersensitivity"
  ]
}
```
**Frequency:** Once/day

**Alternative:** Can also use standard `GET /api/cures/{cure_id}` endpoint

---

### Operation 4: Get Donors with Disease Affecting Vital Organs (with Future Work Suggestions)
```
GET /api/operations/donors-vital-disease
```
**Query Parameters:**
- `disease_id` (required) - The specific disease to filter by

**Example:**
```
GET /api/operations/donors-vital-disease?disease_id=2
```

**Response:** `200 OK`
```json
{
  "disease_id": 2,
  "disease_name": "Heart Disease",
  "donors": [
    {
      "donor_id": 5,
      "donor_name": "John",
      "donor_surname": "Doe",
      "donor_date_of_birth": "1990-05-15",
      "donor_sex": "Male",
      "affected_vital_tissues": [
        {
          "tissue_id": 1,
          "tissue_name": "Heart",
          "tissue_is_vital": "Y"
        }
      ],
      "related_future_works": [
        {
          "future_work_id": 3,
          "future_work_description": "Investigate stem cell therapy for heart regeneration"
        }
      ]
    }
  ]
}
```
**Frequency:** Once/month

---

### Operation 5: Get Future Work Suggestions for Top-Quality Researchers
```
GET /api/operations/top-researchers-suggestions
```
**Query Parameters:**
- `quality` (optional, default: "top") - Journal quality filter

**Example:**
```
GET /api/operations/top-researchers-suggestions
```

**Response:** `200 OK`
```json
{
  "journal_quality": "top",
  "researchers": [
    {
      "researcher_id": 1,
      "researcher_name": "Jane",
      "researcher_surname": "Smith",
      "researcher_email": "jane.smith@example.com",
      "researcher_institution": "MIT",
      "top_publications": [
        {
          "publication_doi": "10.1234/example.2024",
          "publication_title": "Novel Treatment Approaches",
          "publication_journal": "Nature Medicine",
          "publication_journal_quality": "top"
        }
      ],
      "suggested_future_works": [
        {
          "future_work_id": 1,
          "future_work_description": "Investigate combination therapy with drugs X and Y",
          "suggested_by_conditions_count": 5
        }
      ]
    }
  ]
}
```
**Frequency:** Once/month

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid input data",
  "details": {
    "field": "donor_sex",
    "issue": "Must be 'Male' or 'Female'"
  }
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Donor with ID 999 not found"
}
```

### 409 Conflict
```json
{
  "error": "Conflict",
  "message": "Publication with DOI '10.1234/example.2024' already exists"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Database connection failed"
}
```

---

## Notes

1. **ID Generation**: All numeric IDs are auto-generated using Oracle sequences
2. **Date Formats**: ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`)
3. **Pagination**: Default limit is 100 items, max is 1000
4. **Nested Objects**: When creating/updating entities with REF fields, only provide the ID; responses will include full nested objects
5. **Validation**:
   - `tissue_is_vital` must be "Y" or "N"
   - `disease_treatable` must be "Y" or "N"
   - `condition_status` must be "control" or "disease"
   - `treatment_effect` must be "improved", "worsened", or "neutral"
   - `publication_journal_quality` must be "top", "middle", or "low"
6. **Array Limits**:
   - `drug_allergies` max 50 items (VARRAY limit)
7. **Soft Deletes**: Consider implementing soft deletes for critical entities instead of hard deletes

---

## Implementation Priority

### Phase 1 (High Priority - Core CRUD)
1. Donors (simple, no nested structures)
2. Tissues (simple, no nested structures)
3. Drugs (has VARRAY allergies)
4. Cures (has nested table of drug refs)

### Phase 2 (Medium Priority)
5. Diseases (references Cures)
6. Conditions (references multiple entities)
7. Operation 1 (Create Tissue - already covered)
8. Operation 2 (Tissues by density)
9. Operation 3 (Cure details)

### Phase 3 (Complex structures)
10. Future Works (has nested conditions)
11. Researchers (has nested future works)
12. Publications (has multiple nested tables)
13. Operation 4 (Complex query with joins)
14. Operation 5 (Complex query with multiple joins)

---

## Next Steps

1. Create Pydantic models for request/response validation
2. Implement database helper functions for DEREF and nested table operations
3. Create router files for each entity group
4. Implement error handling and validation
5. Add request/response logging
6. Write integration tests for each endpoint
7. Add API documentation using FastAPI's built-in Swagger UI
