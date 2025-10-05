# API Testing Guide - cURL Commands

This document contains cURL commands to test all implemented API endpoints.

**Base URL:** `http://127.0.0.1:8000`

---

## Health Check

```bash
curl -X 'GET' 'http://127.0.0.1:8000/' -H 'accept: application/json'
```

---

## 1. Donor Endpoints

### Create a Donor
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/donors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "donor_name": "John",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "Male"
}'
```

### Get All Donors
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/donors?limit=100&offset=0' \
  -H 'accept: application/json'
```

### Get All Donors with Filter (by sex)
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/donors?sex=F' \
  -H 'accept: application/json'
```

### Get Donor by ID
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/donors/1' \
  -H 'accept: application/json'
```

### Update Donor
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/donors/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "donor_name": "Jane",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "F"
}'
```

### Delete Donor
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/donors/1' \
  -H 'accept: application/json'
```

---

## 2. Tissue Endpoints

### Create a Tissue (Operation 1)
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tissues' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tissue_name": "Heart",
  "tissue_description": "Pumps blood through the body",
  "tissue_density": 1.05,
  "tissue_is_vital": "Y"
}'
```

### Create Multiple Tissues (for testing)
```bash
# Lung (low density, vital)
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tissues' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tissue_name": "Lung",
  "tissue_description": "Respiratory organ",
  "tissue_density": 0.26,
  "tissue_is_vital": "Y"
}'

# Fat tissue (low density, non-vital)
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tissues' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tissue_name": "Adipose Tissue",
  "tissue_description": "Fat storage tissue",
  "tissue_density": 0.92,
  "tissue_is_vital": "N"
}'

# Brain (vital)
curl -X 'POST' \
  'http://127.0.0.1:8000/api/tissues' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tissue_name": "Brain",
  "tissue_description": "Central nervous system organ",
  "tissue_density": 1.04,
  "tissue_is_vital": "Y"
}'
```

### Get All Tissues
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/tissues?limit=100&offset=0' \
  -H 'accept: application/json'
```

### Get Vital Tissues Only
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/tissues?is_vital=Y' \
  -H 'accept: application/json'
```

### Get Tissues Below Density Threshold
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/tissues?max_density=1.0' \
  -H 'accept: application/json'
```

### Get Tissue by ID
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/tissues/1' \
  -H 'accept: application/json'
```

### Update Tissue
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/tissues/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tissue_name": "Heart",
  "tissue_description": "Muscular organ that pumps blood throughout the circulatory system",
  "tissue_density": 1.06,
  "tissue_is_vital": "Y"
}'
```

### Delete Tissue
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/tissues/1' \
  -H 'accept: application/json'
```

---

## 3. Drug Endpoints

### Create a Drug
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/drugs' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "drug_name": "Aspirin",
  "drug_description": "Pain reliever and anti-inflammatory medication",
  "drug_allergies": ["Salicylate sensitivity", "Asthma-related reactions"]
}'
```

### Create Multiple Drugs (for testing)
```bash
# Ibuprofen
curl -X 'POST' \
  'http://127.0.0.1:8000/api/drugs' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "drug_name": "Ibuprofen",
  "drug_description": "Non-steroidal anti-inflammatory drug (NSAID)",
  "drug_allergies": ["NSAID hypersensitivity", "Aspirin allergy"]
}'

# Paracetamol (no known allergies)
curl -X 'POST' \
  'http://127.0.0.1:8000/api/drugs' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "drug_name": "Paracetamol",
  "drug_description": "Analgesic and antipyretic medication",
  "drug_allergies": []
}'

# Penicillin
curl -X 'POST' \
  'http://127.0.0.1:8000/api/drugs' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "drug_name": "Penicillin",
  "drug_description": "Beta-lactam antibiotic",
  "drug_allergies": ["Penicillin allergy", "Beta-lactam hypersensitivity", "Anaphylaxis risk"]
}'
```

### Get All Drugs
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/drugs?limit=100&offset=0' \
  -H 'accept: application/json'
```

### Search Drugs by Name
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/drugs?search=aspirin' \
  -H 'accept: application/json'
```

### Get Drug by ID
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/drugs/1' \
  -H 'accept: application/json'
```

### Update Drug
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/drugs/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "drug_name": "Aspirin",
  "drug_description": "Pain reliever, anti-inflammatory, and antiplatelet medication",
  "drug_allergies": ["Salicylate sensitivity", "Asthma-related reactions", "Bleeding disorders"]
}'
```

### Delete Drug
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/drugs/1' \
  -H 'accept: application/json'
```

---

## 4. Operation Endpoints

### Operation 2: Get Tissues Below Density Threshold
**Frequency:** Once a month

```bash
# Get all tissues with density < 1.0 g/cm³
curl -X 'GET' \
  'http://127.0.0.1:8000/api/operations/tissues-by-density?max_density=1.0' \
  -H 'accept: application/json'
```

```bash
# Get all tissues with density < 0.5 g/cm³
curl -X 'GET' \
  'http://127.0.0.1:8000/api/operations/tissues-by-density?max_density=0.5' \
  -H 'accept: application/json'
```

### Operation 3: Get Cure Details with Drugs and Allergies
**Frequency:** Once a day

```bash
# Get details for cure ID 1
curl -X 'GET' \
  'http://127.0.0.1:8000/api/operations/cure-details/1' \
  -H 'accept: application/json'
```

**Note:** This requires Cures to be created first (Phase 2)

### Operation 4: Get Donors with Vital Tissue Disease
**Frequency:** Once a month

```bash
# Get donors with disease ID 2 affecting vital organs
curl -X 'GET' \
  'http://127.0.0.1:8000/api/operations/donors-vital-disease?disease_id=2' \
  -H 'accept: application/json'
```

**Note:** This requires Diseases, Conditions, and FutureWorks to be created (Phase 2 & 3)

### Operation 5: Get Top Researchers' Suggestions
**Frequency:** Once a month

```bash
# Get suggestions for researchers with top quality journals
curl -X 'GET' \
  'http://127.0.0.1:8000/api/operations/top-researchers-suggestions' \
  -H 'accept: application/json'
```

```bash
# Get suggestions for researchers with middle quality journals
curl -X 'GET' \
  'http://127.0.0.1:8000/api/operations/top-researchers-suggestions?quality=middle' \
  -H 'accept: application/json'
```

**Note:** This requires Publications, Researchers, and FutureWorks to be created (Phase 3)

---

## Testing Workflow

### 1. Basic CRUD Testing

```bash
# 1. Create entities
curl -X 'POST' 'http://127.0.0.1:8000/api/donors' \
  -H 'Content-Type: application/json' \
  -d '{"donor_name": "Test", "donor_surname": "User", "donor_date_of_birth": "1995-01-01", "donor_sex": "Male"}'

# 2. List all
curl -X 'GET' 'http://127.0.0.1:8000/api/donors'

# 3. Get specific (use ID from step 1 response)
curl -X 'GET' 'http://127.0.0.1:8000/api/donors/1'

# 4. Update
curl -X 'PUT' 'http://127.0.0.1:8000/api/donors/1' \
  -H 'Content-Type: application/json' \
  -d '{"donor_name": "Updated", "donor_surname": "User", "donor_date_of_birth": "1995-01-01", "donor_sex": "Male"}'

# 5. Verify update
curl -X 'GET' 'http://127.0.0.1:8000/api/donors/1'

# 6. Delete
curl -X 'DELETE' 'http://127.0.0.1:8000/api/donors/1'

# 7. Verify deletion (should return 404)
curl -X 'GET' 'http://127.0.0.1:8000/api/donors/1'
```

### 2. Operation 2 Testing (Tissues by Density)

```bash
# Create tissues with different densities
curl -X 'POST' 'http://127.0.0.1:8000/api/tissues' \
  -H 'Content-Type: application/json' \
  -d '{"tissue_name": "Lung", "tissue_description": "Low density tissue", "tissue_density": 0.26, "tissue_is_vital": "Y"}'

curl -X 'POST' 'http://127.0.0.1:8000/api/tissues' \
  -H 'Content-Type: application/json' \
  -d '{"tissue_name": "Bone", "tissue_description": "High density tissue", "tissue_density": 1.85, "tissue_is_vital": "N"}'

# Query tissues below threshold
curl -X 'GET' 'http://127.0.0.1:8000/api/operations/tissues-by-density?max_density=1.0'
```

### 3. Error Handling Testing

```bash
# Test 404 - Non-existent resource
curl -X 'GET' 'http://127.0.0.1:8000/api/donors/99999'

# Test 400 - Invalid data (invalid sex value)
curl -X 'POST' 'http://127.0.0.1:8000/api/donors' \
  -H 'Content-Type: application/json' \
  -d '{"donor_name": "Test", "donor_surname": "User", "donor_date_of_birth": "1995-01-01", "donor_sex": "Invalid"}'

# Test 400 - Invalid vital flag
curl -X 'POST' 'http://127.0.0.1:8000/api/tissues' \
  -H 'Content-Type: application/json' \
  -d '{"tissue_name": "Test", "tissue_description": "Test", "tissue_density": 1.0, "tissue_is_vital": "X"}'

# Test 400 - Too many allergies (> 50)
curl -X 'POST' 'http://127.0.0.1:8000/api/drugs' \
  -H 'Content-Type: application/json' \
  -d '{
    "drug_name": "Test Drug",
    "drug_description": "Test",
    "drug_allergies": ["allergy1", "allergy2", ... "allergy51"]
  }'
```

---

## Viewing API Documentation

FastAPI provides interactive API documentation:

### Swagger UI
Open in browser: `http://127.0.0.1:8000/docs`

### ReDoc
Open in browser: `http://127.0.0.1:8000/redoc`

---

## Pretty JSON Output

To format JSON output, pipe curl through `jq`:

```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/donors' | jq '.'
```

Or use curl's `-s` (silent) flag with Python:

```bash
curl -s -X 'GET' 'http://127.0.0.1:8000/api/donors' | python -m json.tool
```

---

## Response Examples

### Successful Donor Creation (201)
```json
{
  "donor_id": 1,
  "donor_name": "John",
  "donor_surname": "Doe",
  "donor_date_of_birth": "1990-05-15",
  "donor_sex": "Male"
}
```

### List Response (200)
```json
{
  "total": 10,
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

### Error Response (404)
```json
{
  "detail": "Donor with ID 999 not found"
}
```

### Error Response (400)
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "donor_sex"],
      "msg": "Value error, donor_sex must be one of ['Male', 'Female', 'Other']",
      "input": "Invalid"
    }
  ]
}
```
