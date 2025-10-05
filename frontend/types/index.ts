// Donor types
export interface Donor {
  donor_id: number;
  donor_name: string;
  donor_surname: string;
  donor_date_of_birth: string;
  donor_sex: 'M' | 'F' | 'X';
}

export interface DonorCreate {
  donor_name: string;
  donor_surname: string;
  donor_date_of_birth: string;
  donor_sex: 'M' | 'F' | 'X';
}

export interface DonorUpdate extends Partial<DonorCreate> {}

// Tissue types
export interface Tissue {
  tissue_id: number;
  tissue_name: string;
  tissue_description: string;
  tissue_density: number;
  tissue_is_vital: 'Y' | 'N';
}

export interface TissueCreate {
  tissue_name: string;
  tissue_description: string;
  tissue_density: number;
  tissue_is_vital: 'Y' | 'N';
}

export interface TissueUpdate extends Partial<TissueCreate> {}

// Drug types
export interface Drug {
  drug_id: number;
  drug_name: string;
  drug_description: string;
  drug_allergies: string[];
}

export interface DrugCreate {
  drug_name: string;
  drug_description: string;
  drug_allergies: string[];
}

export interface DrugUpdate extends Partial<DrugCreate> {}

// API Response types
export interface PaginatedResponse<T> {
  total: number;
  [key: string]: T[] | number;
}

export interface DonorsResponse extends PaginatedResponse<Donor> {
  donors: Donor[];
}

export interface TissuesResponse extends PaginatedResponse<Tissue> {
  tissues: Tissue[];
}

export interface DrugsResponse extends PaginatedResponse<Drug> {
  drugs: Drug[];
}

// Operation types
export interface TissuesByDensityResponse {
  threshold: number;
  count: number;
  tissues: Tissue[];
}

export interface CureDetail {
  cure_id: number;
  drugs: Drug[];
  all_allergies: string[];
}

export interface DonorVitalDisease {
  donor_id: number;
  donor_name: string;
  donor_surname: string;
  donor_date_of_birth: string;
  donor_sex: string;
  affected_vital_tissues: {
    tissue_id: number;
    tissue_name: string;
    tissue_is_vital: string;
  }[];
}

export interface DonorsVitalDiseaseResponse {
  disease_id: number;
  disease_name: string | null;
  donors: DonorVitalDisease[];
}

export interface Publication {
  publication_doi: string;
  publication_title: string;
  publication_journal: string;
  publication_journal_quality: string;
}

export interface FutureWork {
  future_work_id: number;
  future_work_description: string;
}

export interface TopResearcher {
  researcher_id: number;
  researcher_name: string;
  researcher_surname: string;
  researcher_email: string;
  researcher_institution: string;
  top_publications: Publication[];
  suggested_future_works: FutureWork[];
}

export interface TopResearchersResponse {
  journal_quality: string;
  researchers: TopResearcher[];
}

// API Error type
export interface APIError {
  detail: string | { msg: string; type: string }[];
}
