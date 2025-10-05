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
  "donor_sex": "M"
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
  'http://127.0.0.1:8000/api/donors/3' \
  -H 'accept: application/json'
```