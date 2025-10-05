


---

**“WHO”**

La “WHO” organization has implemented a system for monitoring diseases with detailed descriptions.
The system allows WHO storing biological data that could refer to tissues or organs with their description.
Specifically, the tissues and organs are described through the donor details, a general condition (control, disease) and, when affected, the specific disease.
Furthermore, the system saves the organ/tissue name, textual description, position within the human body, density, if it is required for life (e.g., the brain, the heart and so on).
The donors are described through name, surname, date of birth, age, sex. The company has the storage about the diseases and their descriptions: name, discovery date and time, a textual description, whether it is treatable or not, the possible cure. A cure is described with a treatment, a list of drugs to be taken, while the drugs have the name, description, a percentage of success for a specific disease, a list of possible allergies linked to such a drug. For each organ/tissue, the system saves the sequence of treatments with specific drugs and the effects observed. For each positive observed effect, the system could suggest a possible new cure/treatment to be investigated and it suggests possible future works to the list of researchers registered. The system maintains the information of the registered researchers. Specifically, it saves the name, surname, list of publications. A publication is described via a DOI identifier, title, journal, or conference with a degree of quality (top, middle, low).


Operation 1: Recording an organ or tissue (10 times a day)
Operation 2: Print all the organ and tissues below a certain density threshold (once a month)
Operation 3: Request information on a specific cure, its list of drugs and the possible linked allergies (once a day)
Operation 4: Print all the donors with a specific disease affecting only organs/tissue required for life for which the system
provided useful suggestions as future works (once a month)
Operation 5: Print all the useful suggestions provided to only researchers with top quality journals published (once a
month)


My solution:


## ER SCHEMA

### Entities:
Donor(id; int, name: str, surname: str, date_of_birth: date, sex: str)
Tissue(id: int, name: str, description: str, density: float, vital: bool)
Condition(id: int, status: Optional[Literal[control, disease]])
Cure(id: int)
Disease(id: int, name: str, discovery_date: date, description: str, treatable: bool)
Researcher(id: int, name: str, surname: str, email: str, institution: str)
Drug(id: int, name: str, description: str, allergies: list)
Publication(DOI: str, title: str, journal: str, year: int, journal_quality: Literal[top, middle, low])
FutureWork(id: int, description: str)


### Relationships:
R(Donor, Condition) = Observation
R(Condition, Tissue) = Impact
R(Condition, Disease) = Manifestation
R(Condition, Cure) = Treatment(effect {improved, worsened, neutral})
R(Cure, Drug) = Prescription
R(Drug, Disease) = Statistics(effectiveness %)
R(Disease, Cure) = Remedy
R(Researcher, FutureWork) = Recommendation
R(Researcher, Publication) = Contribution
R(Publication, FutureWork) = Proposal
R(Condition, FutureWork) = Suggestion



## Reification and Object-Relational Schema

Donor(id; int, name: str, surname: str, date_of_birth: date, sex: str)
Tissue(id: int, name: str, description: str, density: float, vital: bool)
Condition(id: int, status: Optional[Literal[control, disease]], donor_ref: REF Donor, tissue_ref: REF Tissue, treatment: REF Cure, effect: Literal[improved, worsened, neutral])
Cure(id: int, drugs: NESTED TABLE OF REF Drug)
Drug(id: int, name: str, description: str, allergies: VARRAY OF str)
Disease(id: int, name: str, discovery_date: date, description: str, treatable: bool, cure: REF Cure)
FutureWork(id: int, description: str, suggested_by: Optional[NESTED TABLE OF REF Condition])
Researcher(id: int, name: str, surname: str, email: str, institution: str, recommended_works: NESTED TABLE OF REF FutureWork)
Publication(DOI: str, title: str, journal: str, year: int, journal_quality: Literal[top, middle, low], authors: NESTED TABLE OF REF Researcher, proposed_works: NESTED TABLE OF REF FutureWork)



Note:
- Statistics has been removed since it can be derived and no (frequent) operation requires it.



