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

