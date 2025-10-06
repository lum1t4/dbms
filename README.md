

## Setup database

```bash
docker compose up -d database
docker exec -i oracle-xe sqlplus -S sys/$ORACLE_PWD@//localhost:1521/XEPDB1 as sysdba  <<< 'CREATE USER '$DATABASE_USER' IDENTIFIED BY "'$DATABASE_PASSWORD'" DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp QUOTA UNLIMITED ON users PROFILE DEFAULT ACCOUNT UNLOCK;'
docker exec -i oracle-xe sqlplus SYSTEM/${ORACLE_PWD}@localhost:1521/XEPDB1 @/dev/stdin < scripts/setup.sql
docker exec -i oracle-xe sqlplus ${DATABASE_USER}/${DATABASE_PASSWORD}@localhost:1521/XEPDB1 @/dev/stdin < scripts/schema.sql
docker exec -i oracle-xe sqlplus ${DATABASE_USER}/${DATABASE_PASSWORD}@localhost:1521/XEPDB1 < scripts/populate.sql
```


## Run backend
```bash
cd backend && uv run fastapi dev
```

## Healt check
```bash
curl -X 'GET' 'http://127.0.0.1:8000/' -H 'accept: application/json'
```

## Run frontend
```bash
cd frontend && bun dev
```

## Operations


- OP1: Recording an organ or tissue (10 times a day)
```sql
INSERT INTO Tissues VALUES (
    TissueType(4, 'Heart', 'Pumps blood through the body', 1.05, 'Y')
);
```

- OP2: Print all the organ and tissues below a certain density threshold (once a month)
```sql
SELECT t.tissue_id,
       t.tissue_name,
       t.tissue_description,
       t.tissue_density,
       t.tissue_is_vital
FROM   Tissues t
WHERE  t.tissue_density < 1.0;
```

-OP3: Request information on a specific cure, its list of drugs and the possible linked allergies (once a day)
```sql
SELECT cu.cure_id,
       DEREF(VALUE(d)).drug_id         AS drug_id,
       DEREF(VALUE(d)).drug_name       AS drug_name,
       DEREF(VALUE(d)).drug_description AS drug_description,
       DEREF(VALUE(d)).drug_allergies  AS drug_allergies
FROM   Cures cu, TABLE(cu.cure_composition) d
WHERE  cu.cure_id = 1;
```

- OP4: Print all the donors with a specific disease affecting only organs/tissue required for life for which the system
provided useful suggestions as future works (once a month)

```sql
SELECT DISTINCT
    DEREF(A.condition.donor_ref).donor_id AS donor_id,
    DEREF(A.condition.donor_ref).donor_name AS donor_id,
    DEREF(A.condition.donor_ref).donor_surname AS donor_id
FROM (
  SELECT DEREF(VALUE(f)) AS condition
  FROM FutureWorks fw,
       TABLE(fw.future_work_suggested_by) f
) A
WHERE
DEREF(A.condition.tissue_ref).tissue_is_vital = 'Y'
AND DEREF(A.condition.condition_disease).disease_id = 2;
```


- OP5: Print all the useful suggestions provided to only researchers with top quality journals published (once a month)
```sql
SELECT r.researcher_id,
       r.researcher_name,
       r.researcher_surname,
       p.publication_title,
       p.publication_journal_quality,
       fw.future_work_description
FROM   Publications p,
       TABLE(p.publication_authors) auth_tab,
       Researchers r,
       TABLE(r.researcher_recommended_works) rw,
       FutureWorks fw
WHERE  r.researcher_id = DEREF(VALUE(auth_tab)).researcher_id
  AND  fw.future_work_id = DEREF(VALUE(rw)).future_work_id
  AND  p.publication_journal_quality = 'top';
```