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
  'http://127.0.0.1:8000/api/tissues/4' \
  -H 'accept: application/json'
```

### Update Tissue
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/tissues/4' \
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
  'http://127.0.0.1:8000/api/tissues/4' \
  -H 'accept: application/json'
```