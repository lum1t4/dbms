## 3. Drug Endpoints

### Create a Drug
```bash
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
  'http://127.0.0.1:8000/api/drugs/3' \
  -H 'accept: application/json'
```