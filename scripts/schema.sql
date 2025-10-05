SET DEFINE OFF;
-- ========================
-- Collection Types
-- ========================

CREATE OR REPLACE TYPE AllergyListType AS VARRAY(50) OF VARCHAR2(200);
/

-- ========================
-- Base Object Types
-- ========================

CREATE OR REPLACE TYPE DonorType AS OBJECT (
  donor_id             NUMBER,
  donor_name           VARCHAR2(100),
  donor_surname        VARCHAR2(100),
  donor_date_of_birth  DATE,
  donor_sex            VARCHAR2(10)
);
/

CREATE OR REPLACE TYPE TissueType AS OBJECT (
  tissue_id           NUMBER,
  tissue_name         VARCHAR2(100),
  tissue_description  CLOB,
  tissue_density      NUMBER,          -- e.g., g/cm3
  tissue_is_vital     CHAR(1)          -- 'Y' or 'N'
);
/

CREATE OR REPLACE TYPE DrugType AS OBJECT (
  drug_id             NUMBER,
  drug_name           VARCHAR2(200),
  drug_description    CLOB,
  drug_allergies      AllergyListType   -- list of possible allergies
);
/

-- ========================
-- Collections of REFs (must follow base object definitions)
-- ========================

CREATE OR REPLACE TYPE DrugListType AS TABLE OF REF DrugType;
/

-- Cure depends on DrugListType
CREATE OR REPLACE TYPE CureType AS OBJECT (
  cure_id            NUMBER,
  cure_composition   DrugListType
);
/

-- ========================
-- Disease Type (depends on Cure)
-- ========================

CREATE OR REPLACE TYPE DiseaseType AS OBJECT (
  disease_id             NUMBER,
  disease_name           VARCHAR2(200),
  disease_discovery      DATE,   -- date & time
  disease_description    CLOB,
  disease_treatable      CHAR(1), -- 'Y' or 'N'
  disease_cure_ref       REF CureType
);
/

-- ========================
-- Condition Type (depends on Disease, Donor, Tissue, Cure)
-- ========================

CREATE OR REPLACE TYPE ConditionType AS OBJECT (
  condition_id        NUMBER,
  condition_status    VARCHAR2(10),  -- 'control' or 'disease'
  condition_disease   REF DiseaseType,
  donor_ref           REF DonorType,
  tissue_ref          REF TissueType,
  treatment_ref       REF CureType,
  treatment_effect    VARCHAR2(50)    -- 'improved','worsened','neutral'
);
/

-- Collection of REF Conditions
CREATE OR REPLACE TYPE ConditionListType AS TABLE OF REF ConditionType;
/

-- ========================
-- Future Work
-- ========================

CREATE OR REPLACE TYPE FutureWorkType AS OBJECT (
  future_work_id            NUMBER,
  future_work_description   CLOB,
  future_work_suggested_by  ConditionListType
);
/

-- Collection of REF FutureWorks
CREATE OR REPLACE TYPE FutureWorkListType AS TABLE OF REF FutureWorkType;
/

-- ========================
-- Researcher
-- ========================

CREATE OR REPLACE TYPE ResearcherType AS OBJECT (
  researcher_id               NUMBER,
  researcher_name             VARCHAR2(100),
  researcher_surname          VARCHAR2(100),
  researcher_email            VARCHAR2(320),
  researcher_institution      VARCHAR2(200),
  researcher_recommended_works FutureWorkListType
);
/

-- Collection of REF Researchers
CREATE OR REPLACE TYPE ResearcherListType AS TABLE OF REF ResearcherType;
/

-- ========================
-- Publication
-- ========================

CREATE OR REPLACE TYPE PublicationType AS OBJECT (
  publication_doi             VARCHAR2(100),
  publication_title           VARCHAR2(400),
  publication_journal         VARCHAR2(200),
  publication_year            NUMBER(4),
  publication_journal_quality VARCHAR2(10),  -- 'top'|'middle'|'low'
  publication_authors         ResearcherListType,
  publication_proposed_works  FutureWorkListType
);
/

-- ========================
-- Object Tables
-- ========================

CREATE TABLE Donors OF DonorType (
  CONSTRAINT pk_donors PRIMARY KEY (donor_id)
);

CREATE TABLE Tissues OF TissueType (
  CONSTRAINT pk_tissues PRIMARY KEY (tissue_id)
);

CREATE TABLE Drugs OF DrugType (
  CONSTRAINT pk_drugs PRIMARY KEY (drug_id)
);

CREATE TABLE Cures OF CureType (
  CONSTRAINT pk_cures PRIMARY KEY (cure_id)
)
NESTED TABLE cure_composition STORE AS cure_composition_nt;
ALTER TABLE cure_composition_nt ADD (SCOPE FOR (COLUMN_VALUE) IS Drugs);

CREATE TABLE Diseases OF DiseaseType (
  CONSTRAINT pk_diseases PRIMARY KEY (disease_id),
  SCOPE FOR (disease_cure_ref) IS Cures
);

CREATE TABLE Conditions OF ConditionType (
  CONSTRAINT pk_conditions PRIMARY KEY (condition_id),
  SCOPE FOR (condition_disease) IS Diseases,
  SCOPE FOR (donor_ref) IS Donors,
  SCOPE FOR (tissue_ref) IS Tissues,
  SCOPE FOR (treatment_ref) IS Cures
);

CREATE TABLE FutureWorks OF FutureWorkType (
  CONSTRAINT pk_futureworks PRIMARY KEY (future_work_id)
)
NESTED TABLE future_work_suggested_by STORE AS future_work_suggested_by_nt;
ALTER TABLE future_work_suggested_by_nt ADD (SCOPE FOR (COLUMN_VALUE) IS Conditions);

CREATE TABLE Researchers OF ResearcherType (
  CONSTRAINT pk_researchers PRIMARY KEY (researcher_id)
) NESTED TABLE researcher_recommended_works STORE AS researcher_recommended_works_nt;
ALTER TABLE researcher_recommended_works_nt ADD (SCOPE FOR (COLUMN_VALUE) IS FutureWorks);

CREATE TABLE Publications OF PublicationType (
  CONSTRAINT pk_publications PRIMARY KEY (publication_doi)
) NESTED TABLE publication_authors STORE AS publication_authors_nt
NESTED TABLE publication_proposed_works STORE AS publication_proposed_works_nt;

ALTER TABLE publication_authors_nt ADD (SCOPE FOR (COLUMN_VALUE) IS Researchers);
ALTER TABLE publication_proposed_works_nt ADD (SCOPE FOR (COLUMN_VALUE) IS FutureWorks);



CREATE SEQUENCE donor_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE tissue_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE drug_seq START WITH 1 INCREMENT BY 1;