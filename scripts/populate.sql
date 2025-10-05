-- ========================
-- Donors
-- ========================
INSERT INTO Donors VALUES (DonorType(1, 'Alice', 'Smith', DATE '1980-05-12', 'F'));
INSERT INTO Donors VALUES (DonorType(2, 'Bob', 'Johnson', DATE '1975-02-20', 'M'));

-- ========================
-- Tissues
-- ========================
INSERT INTO Tissues VALUES (TissueType(1, 'Brain', 'Central organ of the nervous system', 1.04, 'Y'));
INSERT INTO Tissues VALUES (TissueType(2, 'Liver', 'Metabolic organ', 1.06, 'Y'));
INSERT INTO Tissues VALUES (TissueType(3, 'Fat Tissue', 'Adipose storage tissue', 0.92, 'N'));

-- ========================
-- Drugs
-- ========================
INSERT INTO Drugs VALUES (DrugType(1, 'Aspirin', 'Anti-inflammatory drug', AllergyListType('NSAID sensitivity')));
INSERT INTO Drugs VALUES (DrugType(2, 'Cisplatin', 'Chemotherapy drug', AllergyListType('Nausea', 'Kidney damage')));
INSERT INTO Drugs VALUES (DrugType(3, 'Paracetamol', 'Pain reliever and fever reducer', AllergyListType('Liver risk')));

-- ========================
-- Cures
-- ========================
DECLARE
  d1 REF DrugType;
  d2 REF DrugType;
BEGIN
  SELECT REF(d) INTO d1 FROM Drugs d WHERE d.drug_id = 1;
  SELECT REF(d) INTO d2 FROM Drugs d WHERE d.drug_id = 3;

  INSERT INTO Cures VALUES (
    CureType(1, DrugListType(d1, d2))
  );
END;
/

DECLARE
  d3 REF DrugType;
BEGIN
  SELECT REF(d) INTO d3 FROM Drugs d WHERE d.drug_id = 2;

  INSERT INTO Cures VALUES (
    CureType(2, DrugListType(d3))
  );
END;
/

-- ========================
-- Diseases
-- ========================
DECLARE
  c1 REF CureType;
  c2 REF CureType;
BEGIN
  SELECT REF(c) INTO c1 FROM Cures c WHERE c.cure_id = 1;
  SELECT REF(c) INTO c2 FROM Cures c WHERE c.cure_id = 2;

  INSERT INTO Diseases VALUES (
    DiseaseType(1, 'Migraine', DATE '1990-01-01', 'Neurological disorder causing headaches', 'Y', c1)
  );

  INSERT INTO Diseases VALUES (
    DiseaseType(2, 'Liver Cancer', DATE '1985-06-15', 'Malignant tumor of the liver', 'N', c2)
  );
END;
/

-- ========================
-- Conditions
-- ========================
DECLARE
  d1 REF DonorType;
  d2 REF DonorType;
  t1 REF TissueType;
  t2 REF TissueType;
  dis1 REF DiseaseType;
  dis2 REF DiseaseType;
  c1 REF CureType;
  c2 REF CureType;
BEGIN
  SELECT REF(d) INTO d1 FROM Donors d WHERE d.donor_id = 1;
  SELECT REF(d) INTO d2 FROM Donors d WHERE d.donor_id = 2;

  SELECT REF(t) INTO t1 FROM Tissues t WHERE t.tissue_id = 1;
  SELECT REF(t) INTO t2 FROM Tissues t WHERE t.tissue_id = 2;

  SELECT REF(ds) INTO dis1 FROM Diseases ds WHERE ds.disease_id = 1;
  SELECT REF(ds) INTO dis2 FROM Diseases ds WHERE ds.disease_id = 2;

  SELECT REF(c) INTO c1 FROM Cures c WHERE c.cure_id = 1;
  SELECT REF(c) INTO c2 FROM Cures c WHERE c.cure_id = 2;

  INSERT INTO Conditions VALUES (
    ConditionType(1, 'disease', dis1, d1, t1, c1, 'improved')
  );

  INSERT INTO Conditions VALUES (
    ConditionType(2, 'disease', dis2, d2, t2, c2, 'worsened')
  );
END;
/

-- ========================
-- Future Works
-- ========================
DECLARE
  cond1 REF ConditionType;
  cond2 REF ConditionType;
BEGIN
  SELECT REF(c) INTO cond1 FROM Conditions c WHERE c.condition_id = 1;
  SELECT REF(c) INTO cond2 FROM Conditions c WHERE c.condition_id = 2;

  INSERT INTO FutureWorks VALUES (
    FutureWorkType(1, 'Investigate alternative migraine therapies', ConditionListType(cond1))
  );

  INSERT INTO FutureWorks VALUES (
    FutureWorkType(2, 'Study resistance mechanisms in liver cancer', ConditionListType(cond2))
  );
END;
/

-- ========================
-- Researchers
-- ========================
DECLARE
  fw1 REF FutureWorkType;
  fw2 REF FutureWorkType;
BEGIN
  SELECT REF(f) INTO fw1 FROM FutureWorks f WHERE f.future_work_id = 1;
  SELECT REF(f) INTO fw2 FROM FutureWorks f WHERE f.future_work_id = 2;

  INSERT INTO Researchers VALUES (
    ResearcherType(1, 'Dr. Emily', 'White', 'emily.white@who.org', 'WHO Institute',
                   FutureWorkListType(fw1))
  );

  INSERT INTO Researchers VALUES (
    ResearcherType(2, 'Dr. John', 'Miller', 'john.miller@who.org', 'WHO Institute',
                   FutureWorkListType(fw2))
  );
END;
/

-- ========================
-- Publications
-- ========================
DECLARE
  r1 REF ResearcherType;
  r2 REF ResearcherType;
  fw1 REF FutureWorkType;
BEGIN
  SELECT REF(r) INTO r1 FROM Researchers r WHERE r.researcher_id = 1;
  SELECT REF(r) INTO r2 FROM Researchers r WHERE r.researcher_id = 2;

  SELECT REF(f) INTO fw1 FROM FutureWorks f WHERE f.future_work_id = 1;

  INSERT INTO Publications VALUES (
    PublicationType('10.1000/migraine01', 'Migraine Research Advances',
                    'Neurology Journal', 2020, 'top',
                    ResearcherListType(r1),
                    FutureWorkListType(fw1))
  );

  INSERT INTO Publications VALUES (
    PublicationType('10.1000/livercancer01', 'Liver Cancer Challenges',
                    'Oncology Reports', 2019, 'middle',
                    ResearcherListType(r2),
                    FutureWorkListType())
  );
END;
/

COMMIT;

-- ========================
-- Reset Sequences to avoid conflicts with API inserts
-- ========================
DECLARE
    v_max_id NUMBER;
BEGIN
    -- Reset donor_seq to start after existing data
    SELECT NVL(MAX(donor_id), 0) INTO v_max_id FROM Donors;
    EXECUTE IMMEDIATE 'DROP SEQUENCE donor_seq';
    EXECUTE IMMEDIATE 'CREATE SEQUENCE donor_seq START WITH ' || (v_max_id + 1) || ' INCREMENT BY 1';

    -- Reset tissue_seq to start after existing data
    SELECT NVL(MAX(tissue_id), 0) INTO v_max_id FROM Tissues;
    EXECUTE IMMEDIATE 'DROP SEQUENCE tissue_seq';
    EXECUTE IMMEDIATE 'CREATE SEQUENCE tissue_seq START WITH ' || (v_max_id + 1) || ' INCREMENT BY 1';

    -- Reset drug_seq to start after existing data
    SELECT NVL(MAX(drug_id), 0) INTO v_max_id FROM Drugs;
    EXECUTE IMMEDIATE 'DROP SEQUENCE drug_seq';
    EXECUTE IMMEDIATE 'CREATE SEQUENCE drug_seq START WITH ' || (v_max_id + 1) || ' INCREMENT BY 1';

    DBMS_OUTPUT.PUT_LINE('All sequences reset successfully');
END;
/
