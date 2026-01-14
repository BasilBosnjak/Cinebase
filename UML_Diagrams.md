# Section 4: UML Diagrams

This section contains all UML diagrams for the Cinebase application. Each diagram is provided in PlantUML format.

## 4.1 Use Case Diagram

**File:** `usecase_diagram.puml`

```plantuml
@startuml Cinebase Use Case Diagram
left to right direction
skinparam packageStyle rectangle

actor "Job Seeker" as user
actor "System Administrator" as admin
actor "n8n Scheduler" as scheduler
actor "Hugging Face API" as hf
actor "Groq API" as groq
actor "Job Boards\n(Indeed/LinkedIn/Glassdoor)" as jobs

rectangle Cinebase {
  usecase "Login with Email" as UC1
  usecase "Upload PDF Resume" as UC2
  usecase "View Document List" as UC3
  usecase "Delete Document" as UC4
  usecase "View Dashboard Statistics" as UC5
  usecase "Find Matching Jobs" as UC6
  usecase "Receive Weekly Job Digest" as UC7

  usecase "Extract Text from PDF" as UC8
  usecase "Generate Vector Embedding" as UC9
  usecase "Extract Job Title from Resume" as UC10
  usecase "Search Jobs on Multiple Platforms" as UC11
  usecase "Calculate Similarity Scores" as UC12
  usecase "Rank and Present Job Results" as UC13
  usecase "Generate Weekly Digest" as UC14
  usecase "Send Email via SMTP" as UC15
}

user --> UC1
user --> UC2
user --> UC3
user --> UC4
user --> UC5
user --> UC6
user --> UC7

UC2 ..> UC8 : <<include>>
UC2 ..> UC9 : <<include>>
UC9 --> hf : uses

UC6 ..> UC10 : <<include>>
UC6 ..> UC11 : <<include>>
UC6 ..> UC12 : <<include>>
UC6 ..> UC13 : <<include>>

UC10 --> groq : uses
UC11 --> jobs : scrapes
UC12 --> hf : uses

scheduler --> UC14
UC14 ..> UC10 : <<include>>
UC14 ..> UC11 : <<include>>
UC14 ..> UC12 : <<include>>
UC14 ..> UC15 : <<include>>

admin --> Cinebase : manages

note right of UC9
  Background task
  Non-blocking
end note

note right of UC14
  Runs every Monday 9AM
end note

@enduml
```

---

## 4.2 Activity Diagram - Document CRUD Operations

**File:** `activity_document_crud.puml`

```plantuml
@startuml Document CRUD Operations
start

:User logs in with email;

if (Email exists in database?) then (yes)
  :Retrieve user data;
else (no)
  :Create new user record;
endif

:Display dashboard;

partition "Document Upload" {
  :User selects PDF file;

  if (File type is PDF?) then (no)
    :Display error "Only PDF files allowed";
    stop
  else (yes)
  endif

  if (File size < 10 MB?) then (no)
    :Display error "File too large";
    stop
  else (yes)
  endif

  :Upload file to server;
  :Save file to user directory;
  :Extract text content using pypdf;

  if (Extraction successful?) then (yes)
    :Store text in database;
    :Set status = "processed";
  else (no)
    :Store error message;
  endif

  :Create document record;
  :Return success response;

  fork
    :Start background task;
    :Truncate text to 8000 chars;
    :Call Hugging Face API;

    if (API call successful?) then (yes)
      :Receive 768-dim vector;
      :Store embedding in database;
    else (no)
      :Log error;
    endif
  end fork

  :Display document in list;
}

partition "Document Viewing" {
  :User views dashboard;
  :Query documents WHERE user_id = current_user;
  :Display document list\n(filename, date, size, status);
}

partition "Document Deletion" {
  :User clicks delete button;

  if (User owns document?) then (no)
    :Display error "Unauthorized";
    stop
  else (yes)
  endif

  :Delete file from storage;
  :Delete database record;
  :Display success message;
  :Refresh document list;
}

stop
@enduml
```

---

## 4.3 Activity Diagram - Job Matching, Filtering, and Ranking

**File:** `activity_job_matching.puml`

```plantuml
@startuml Job Matching Activity
start

:User clicks "Find Jobs" button;

if (Document has embedding?) then (no)
  :Display error\n"Embedding not generated yet";
  stop
else (yes)
endif

:Retrieve document content and embedding;

partition "Job Title Extraction" {
  :Truncate content to 3000 chars;
  :Create prompt for LLM;
  :Call Groq API;

  if (API call successful?) then (yes)
    :Parse job title from response;
    :Clean response\n(remove quotes, prefixes);

    if (Job title valid and < 50 chars?) then (yes)
      :Use extracted job title;
    else (no)
      :Use fallback "general";
    endif
  else (no)
    :Use fallback "general";
  endif
}

partition "Job Search" {
  :Call JobSpy library;
  :Parameters: search_term, location, results_wanted, is_remote;

  fork
    :Scrape Indeed;
  fork again
    :Scrape LinkedIn;
  fork again
    :Scrape Glassdoor;
  end fork

  :Aggregate results from all platforms;

  if (Jobs found?) then (no)
    :Return empty results with message;
    stop
  else (yes)
  endif
}

partition "Similarity Calculation" {
  repeat :For each job;
    :Combine title, company, description;
    :Truncate to 8000 chars;
    :Call Hugging Face API;

    if (API call successful?) then (yes)
      :Receive job embedding (768-dim);
      :Calculate cosine similarity\ndot(resume, job) / (norm(resume) * norm(job));
      :Round score to 4 decimals;
      :Store job with similarity score;
    else (no)
      :Log error;
      :Skip this job;
    endif
  repeat while (More jobs?)
}

partition "Ranking and Presentation" {
  :Sort jobs by similarity score DESC;
  :Truncate descriptions to 500 chars;
  :Format response JSON;
  :Return ranked job matches;
  :Display results table in UI;
}

:User reviews job matches;
:User clicks job URL to apply;

stop
@enduml
```

---

## 4.4 Sequence Diagram - Job Matching Process

**File:** `sequence_job_matching.puml`

```plantuml
@startuml Job Matching Sequence Diagram
actor User
participant "React Frontend" as UI
participant "FastAPI Backend" as API
participant "PostgreSQL Database" as DB
participant "Groq API" as LLM
participant "JobSpy Library" as JobSpy
participant "Indeed/LinkedIn/Glassdoor" as JobBoards
participant "Hugging Face API" as HF

User -> UI: Click "Find Jobs" button
UI -> API: POST /jobs/match\n{document_id, location, results_wanted, is_remote}

API -> DB: SELECT content, embedding\nFROM documents\nWHERE id = document_id
DB --> API: Return document data

alt No embedding found
  API --> UI: 404 Error\n"Embedding not generated"
  UI --> User: Display error message
else Embedding exists

  API -> LLM: POST /chat/completions\n{prompt: "Extract job title from CV"}
  LLM --> API: Job title (e.g., "Software Engineer")

  API -> JobSpy: scrape_jobs(\nsearch_term="Software Engineer",\nlocation="Remote",\nresults_wanted=10,\nis_remote=True)

  JobSpy -> JobBoards: Scrape job postings
  JobBoards --> JobSpy: Return job data
  JobSpy --> API: DataFrame with 25 jobs

  loop For each job
    API -> HF: POST /feature-extraction\n{inputs: job_text}
    HF --> API: 768-dim embedding vector
    API -> API: Calculate cosine similarity\n(resume_emb, job_emb)
  end

  API -> API: Sort jobs by similarity DESC
  API --> UI: JSON Response\n{query, total_jobs_fetched, matches[]}
  UI --> User: Display ranked job table

  User -> UI: Click job URL
  UI -> JobBoards: Open external link
end

@enduml
```

---

## 4.5 Class Diagram

**File:** `class_diagram.puml`

```plantuml
@startuml Cinebase Class Diagram
' Models/Entities
class User {
  - id: UUID {PK}
  - email: String {unique}
  - created_at: DateTime
  --
  + __init__(email: str)
  + __repr__(): str
}

class Document {
  - id: UUID {PK}
  - user_id: UUID {FK}
  - file_path: String
  - original_filename: String
  - file_size: Integer
  - mime_type: String
  - title: String (nullable)
  - content: Text
  - status: String
  - embedding: Vector(768) (nullable)
  - created_at: DateTime
  - updated_at: DateTime
  --
  + __init__(...)
  + __repr__(): str
}

' Pydantic Schemas
class DocumentCreate <<Schema>> {
  + user_id: UUID
  + file_path: str
  + original_filename: str
  + file_size: int
  + mime_type: str
  + title: Optional[str]
  + content: str
}

class DocumentResponse <<Schema>> {
  + id: UUID
  + user_id: UUID
  + file_path: str
  + original_filename: str
  + file_size: int
  + status: str
  + created_at: datetime
  + updated_at: datetime
}

class JobMatchRequest <<Schema>> {
  + document_id: str
  + location: Optional[str]
  + results_wanted: Optional[int]
  + is_remote: Optional[bool]
}

class JobMatch <<Schema>> {
  + id: str
  + title: str
  + company: str
  + location: str
  + job_url: str
  + description: str
  + salary_min: Optional[float]
  + salary_max: Optional[float]
  + similarity_score: float
}

class JobMatchResponse <<Schema>> {
  + query: str
  + total_jobs_fetched: int
  + matches: List[JobMatch]
}

' Services
class AIService <<Service>> {
  + get_embedding(text: str): List[float]
  + generate_text(prompt: str, max_tokens: int, temperature: float): str
  + extract_job_title(cv_content: str): str
}

class FileStorage <<Service>> {
  + save_uploaded_file(user_id: UUID, file: UploadFile, upload_dir: str): dict
  + delete_file(file_path: str): bool
}

class PDFExtractor <<Service>> {
  + extract_text_from_pdf(file_path: str): str
}

class JobMatchingService <<Service>> {
  - cosine_similarity(vec1: List[float], vec2: List[float]): float
  - search_jobs_sync(...): List[dict]
  + search_jobs_async(...): List[dict]
  + process_jobs_with_embeddings(...): List[JobMatch]
}

' Routers/Controllers
class AuthRouter <<Router>> {
  + login(email: EmailStr, db: Session): User
}

class UsersRouter <<Router>> {
  + get_user_documents(user_id: UUID, db: Session): List[DocumentResponse]
  + upload_document(user_id: UUID, file: UploadFile, ...): DocumentResponse
  + get_user_stats(user_id: UUID, db: Session): StatsResponse
  - generate_document_embedding(document_id: str, content: str): void
}

class JobsRouter <<Router>> {
  + match_jobs(request: JobMatchRequest, db: Session): JobMatchResponse
  + get_weekly_digest(top_n: int, ...): WeeklyDigestResponse
  + search_jobs(search_term: str, ...): dict
}

' Database
class Database <<Singleton>> {
  - engine: Engine
  - SessionLocal: sessionmaker
  - Base: DeclarativeMeta
  --
  + get_db(): Generator[Session]
}

' Relationships
User "1" -- "0..*" Document : owns >

DocumentCreate ..> Document : creates
Document ..> DocumentResponse : serializes to

UsersRouter --> FileStorage : uses
UsersRouter --> PDFExtractor : uses
UsersRouter --> AIService : uses
UsersRouter --> Database : queries

JobsRouter --> AIService : uses
JobsRouter --> JobMatchingService : uses
JobsRouter --> Database : queries

JobMatchingService --> AIService : calls
AuthRouter --> Database : queries

JobMatchRequest ..> JobMatchResponse : processed into
JobMatch --o JobMatchResponse : contains

@enduml
```

---

## 4.6 Entity Relationship Diagram (ERD)

**File:** `erd_diagram.puml`

```plantuml
@startuml Cinebase ERD
!define table(x) class x << (T,#FFAAAA) >>
!define primary_key(x) <color:red><b>x</b></color>
!define foreign_key(x) <color:blue><i>x</i></color>
!define unique(x) <color:green>x</color>

hide methods
hide stereotypes

table(users) {
  primary_key(id): UUID
  unique(email): VARCHAR(255)
  created_at: TIMESTAMP
}

table(documents) {
  primary_key(id): UUID
  foreign_key(user_id): UUID
  file_path: VARCHAR(500)
  original_filename: VARCHAR(255)
  file_size: INTEGER
  mime_type: VARCHAR(100)
  title: VARCHAR(255) NULL
  content: TEXT
  status: VARCHAR(50)
  embedding: VECTOR(768) NULL
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
}

users ||--o{ documents : "owns"

note right of users
  **Primary Key:** id (UUID, auto-generated)
  **Unique Constraint:** email
  **Index:** email (for login queries)
end note

note right of documents
  **Primary Key:** id (UUID, auto-generated)
  **Foreign Key:** user_id → users(id) ON DELETE CASCADE
  **Indexes:**
    - user_id (for user document queries)
    - created_at (for sorting)
  **Vector Extension:** embedding uses pgvector
end note

@enduml
```

---

## 4.7 Converting PlantUML to PDF

To convert these diagrams to PDF format:

**Method 1: Command Line (Linux/Mac)**
```bash
# Install PlantUML
sudo apt-get install plantuml  # Ubuntu/Debian
brew install plantuml          # macOS

# Convert to PDF
plantuml -tpdf usecase_diagram.puml
plantuml -tpdf activity_document_crud.puml
plantuml -tpdf activity_job_matching.puml
plantuml -tpdf sequence_job_matching.puml
plantuml -tpdf class_diagram.puml
plantuml -tpdf erd_diagram.puml
```

**Method 2: Online Tool**
1. Visit http://www.plantuml.com/plantuml/uml/
2. Paste the PlantUML code
3. Click "Submit"
4. Download as PDF

**Method 3: VS Code Extension**
1. Install "PlantUML" extension in VS Code
2. Open `.puml` file
3. Press `Alt+D` to preview
4. Right-click preview → Export → PDF

---

**End of Section 4: UML Diagrams**
