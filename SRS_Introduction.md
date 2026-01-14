# Software Requirements Specification
## Cinebase: CV/Resume Management and Job Matching Platform
Github repository: https://github.com/BasilBosnjak/Cinebase
Deployed application: https://cinebase-sepia.vercel.app/

**Version:** 1.0
**Date:** January 13, 2026
**Status:** Draft

---

# 1. Introduction

## 1.1 Purpose

This Software Requirements Specification (SRS) document provides a comprehensive description of the requirements for **Cinebase**, an intelligent CV/resume management and job matching platform. The document specifies the functional and non-functional requirements, system features, constraints, and dependencies necessary for the development, deployment, and maintenance of the application.

The intended audience for this document includes:
- **Development Team:** Software engineers, frontend and backend developers responsible for implementing the system
- **Project Stakeholders:** Product owners, project managers overseeing development progress
- **Quality Assurance Team:** Testers validating system functionality against specified requirements
- **System Administrators:** DevOps engineers responsible for deployment and infrastructure management
- **End Users:** Job seekers requiring guidance on system capabilities and expected behavior

## 1.2 Scope

**Cinebase** is a full-stack web application designed to assist job seekers in managing their CVs/resumes and discovering relevant job opportunities through AI-powered semantic matching. The platform addresses the challenge of manual job searching by automating the process of finding positions that align with a user's qualifications and experience.

### 1.2.1 Product Overview

Cinebase enables users to:
- Upload and store their CVs/resumes in PDF format
- Automatically extract and process resume content using text extraction and AI analysis
- Generate vector embeddings from resume content for semantic comparison
- Search for jobs across multiple job boards (Indeed, LinkedIn, Glassdoor) using intelligent query generation
- Receive ranked job recommendations based on semantic similarity between resume and job descriptions
- Subscribe to weekly automated job digest emails with top-matched opportunities

### 1.2.2 Target Users

The primary target audience consists of:
- **Active Job Seekers:** Individuals currently searching for employment opportunities
- **Passive Job Seekers:** Employed professionals monitoring the job market for better opportunities
- **Recent Graduates:** Students transitioning from education to professional employment
- **Career Changers:** Professionals seeking opportunities in different industries or roles

Users typically struggle with:
- Manually searching multiple job boards for relevant positions
- Identifying jobs that match their specific skills and experience
- Staying updated on new job postings without constant manual checking
- Understanding which positions best align with their qualifications

### 1.2.3 System Benefits

The application provides the following benefits:
- **Time Efficiency:** Automated job searching eliminates manual searches across multiple platforms
- **Improved Matching Quality:** Semantic similarity algorithms identify jobs based on meaning, not just keywords
- **Centralized Resume Storage:** Single source of truth for user CV/resume documents
- **Proactive Notifications:** Weekly email digests keep users informed of new opportunities
- **Data-Driven Insights:** Similarity scores help users prioritize job applications

### 1.2.4 Product Features (High-Level)

**User Management:**
- Email-based authentication (no password required)
- User profile creation and management

**Document Management:**
- PDF upload and storage
- Text extraction from uploaded documents
- Document metadata tracking (filename, size, upload date)
- Document deletion and update capabilities

**AI-Powered Processing:**
- Automatic resume content analysis using large language models (LLMs)
- Vector embedding generation for semantic search (768-dimensional embeddings)
- Intelligent job title extraction from resume content

**Job Matching:**
- Multi-platform job search (Indeed, LinkedIn, Glassdoor)
- Semantic similarity calculation between resume and job descriptions
- Ranked job results with similarity scores (0-1 scale)
- Customizable search parameters (location, remote status, number of results)

**Automation:**
- Background embedding generation (non-blocking upload process)
- Weekly job digest email automation via workflow orchestration
- Automatic job relevance scoring

### 1.2.5 Out of Scope

The following features are explicitly excluded from the current version:
- Password-based authentication or OAuth integration
- Resume editing or creation tools within the platform
- Application tracking or job application submission
- Direct messaging with employers
- Resume optimization or feedback features
- Support for document formats other than PDF
- Mobile native applications (iOS/Android)
- Multi-language support (English only)
- Payment processing or premium features

## 1.3 Definitions, Acronyms, and Abbreviations

This section provides comprehensive definitions for all technical terms, acronyms, and abbreviations used throughout this Software Requirements Specification document.

### 1.3.1 General Terms and Concepts

| Term | Definition |
|------|------------|
| **API** | Application Programming Interface - A set of protocols, tools, and definitions for building application software and enabling communication between different software components |
| **Async/Asynchronous** | Programming paradigm where operations run independently without blocking the main execution thread, allowing multiple tasks to progress concurrently |
| **Authentication** | The process of verifying the identity of a user, device, or system attempting to access a resource |
| **Authorization** | The process of determining what actions an authenticated user is permitted to perform |
| **Background Task** | An operation that executes independently of the main application flow, typically used for long-running or non-critical processes |
| **CDN** | Content Delivery Network - A geographically distributed network of servers that deliver web content to users based on their location for improved performance |
| **Client-Server Architecture** | A distributed application structure where tasks are divided between service providers (servers) and service requesters (clients) |
| **Cold Start** | The delay experienced when a serverless or container-based application starts after a period of inactivity |
| **CRUD** | Create, Read, Update, Delete - The four basic operations for persistent storage |
| **CV** | Curriculum Vitae - A comprehensive document containing a summary of a person's education, professional qualifications, work experience, skills, and achievements |
| **Deployment** | The process of making an application available for use in a production environment |
| **Endpoint** | A specific URL path in an API where a particular resource or service can be accessed |
| **Environment Variable** | A dynamic named value that can affect how running processes behave on a computer, often used for configuration |
| **Job Board** | An online platform where employers post job openings and job seekers search for employment opportunities (examples: Indeed, LinkedIn, Glassdoor) |
| **Localhost** | A hostname that refers to the current computer used to access it, typically resolving to IP address 127.0.0.1 |
| **Metadata** | Data that provides information about other data, such as file size, creation date, or author |
| **Microservices** | An architectural style where an application is composed of small, independent services that communicate via APIs |
| **Middleware** | Software that acts as a bridge between an operating system or database and applications, especially on a network |
| **Migration** | The process of changing a database schema or moving data from one system to another |
| **Payload** | The actual data transmitted in a network communication, excluding headers and metadata |
| **Query String** | Part of a URL that contains parameters passed to web applications, typically following a question mark (?) |
| **Resume** | A concise document summarizing work experience, skills, education, and qualifications (American English equivalent of CV) |
| **RESTful API** | Representational State Transfer API - An architectural style for networked applications using HTTP requests to access and manipulate data |
| **Session** | A temporary interactive information exchange between two or more communicating devices, or between a computer and user |
| **SPA** | Single Page Application - A web application that loads a single HTML page and dynamically updates content as the user interacts with the app |
| **SRS** | Software Requirements Specification - A comprehensive description of the intended purpose, requirements, and functionality of a software system |
| **Stateless** | A design principle where each request from client to server must contain all information needed to understand the request, with no stored session state |
| **UUID** | Universally Unique Identifier - A 128-bit number used to uniquely identify information in computer systems, represented as 32 hexadecimal characters |
| **Web Scraping** | The automated process of extracting data from websites using software tools |
| **Webhook** | An HTTP callback that occurs when something happens, allowing one application to provide real-time information to another |

### 1.3.2 Backend Technologies (Python/FastAPI)

| Term | Definition |
|------|------------|
| **ASGI** | Asynchronous Server Gateway Interface - A spiritual successor to WSGI, providing a standard interface between async-capable Python web servers and applications |
| **BackgroundTasks** | FastAPI feature for running tasks asynchronously after returning a response, without blocking the client |
| **Dependency Injection** | A design pattern in FastAPI where dependencies are provided to route handlers automatically through function parameters |
| **FastAPI** | Modern, high-performance Python web framework for building APIs with automatic interactive documentation, based on standard Python type hints |
| **Gunicorn** | Green Unicorn - A Python WSGI HTTP Server for UNIX, commonly used to serve Python web applications in production |
| **httpx** | A fully featured HTTP client library for Python with both sync and async APIs |
| **ORM** | Object-Relational Mapping - A technique that lets you query and manipulate data from a database using an object-oriented paradigm |
| **Pydantic** | Data validation library for Python that uses type annotations to validate, serialize, and document data structures |
| **pypdf** | Python library for reading and manipulating PDF files, used for extracting text content from uploaded resumes |
| **Python Virtual Environment** | An isolated Python environment that allows package installation without affecting the system-wide Python installation |
| **requirements.txt** | A file listing all Python package dependencies with their versions for reproducible installations |
| **Router** | In FastAPI, a way to organize related endpoints into groups with shared prefixes and tags |
| **SQLAlchemy** | The Python SQL toolkit and Object-Relational Mapping (ORM) library that provides a full suite of enterprise-level persistence patterns |
| **Type Hints** | Python syntax for annotating function parameters and return types, used by FastAPI for automatic validation and documentation |
| **Uvicorn** | Lightning-fast ASGI server implementation for Python, built on uvloop and httptools |
| **WSGI** | Web Server Gateway Interface - A standard interface between web servers and Python web applications or frameworks |

### 1.3.3 Frontend Technologies (React/Vite)

| Term | Definition |
|------|------------|
| **Component** | A reusable, self-contained piece of UI in React that can accept props and manage its own state |
| **Context API** | React feature for sharing state across the component tree without prop drilling |
| **DOM** | Document Object Model - A programming interface for HTML documents, representing the page structure as a tree of objects |
| **ES6** | ECMAScript 2015 - The sixth version of JavaScript, introducing features like arrow functions, classes, modules, and promises |
| **Hook** | A React function that lets you "hook into" React features like state and lifecycle from function components |
| **JSX** | JavaScript XML - A syntax extension for JavaScript that allows writing HTML-like code in React components |
| **LocalStorage** | Web Storage API that allows JavaScript to store key-value pairs in a web browser with no expiration time |
| **npm** | Node Package Manager - The default package manager for Node.js, used to install and manage JavaScript dependencies |
| **package.json** | A file containing metadata about a Node.js project, including dependencies, scripts, and version information |
| **Props** | Properties passed from parent components to child components in React |
| **React** | A JavaScript library for building user interfaces, maintained by Meta (Facebook), focusing on component-based architecture |
| **React Router** | A collection of navigational components for React applications, enabling client-side routing in single-page applications |
| **State** | An object in React components that holds data that may change over the lifetime of the component |
| **Tailwind CSS** | A utility-first CSS framework that provides low-level utility classes for building custom designs without leaving HTML |
| **Virtual DOM** | React's lightweight copy of the actual DOM, used to efficiently update the UI by comparing changes before applying them |
| **Vite** | Next-generation frontend build tool that provides fast development server with hot module replacement and optimized production builds |

### 1.3.4 Database Technologies

| Term | Definition |
|------|------------|
| **ACID** | Atomicity, Consistency, Isolation, Durability - A set of properties guaranteeing database transaction reliability |
| **CASCADE** | A referential action in foreign key constraints that automatically deletes or updates dependent rows when the parent row is deleted or updated |
| **Connection Pool** | A cache of database connections maintained to improve performance by reusing connections rather than creating new ones |
| **Foreign Key** | A field in a database table that uniquely identifies a row of another table, creating a relationship between tables |
| **Index** | A database structure that improves the speed of data retrieval operations at the cost of additional storage and slower writes |
| **pgvector** | PostgreSQL extension that adds support for vector similarity search, enabling storage and querying of high-dimensional vectors |
| **PostgreSQL** | Open-source relational database management system emphasizing extensibility and SQL compliance |
| **Primary Key** | A unique identifier for a database record, ensuring each row can be uniquely identified |
| **RDBMS** | Relational Database Management System - A database management system based on the relational model where data is stored in tables |
| **Schema** | The structure of a database, defining tables, fields, relationships, and constraints |
| **SQL** | Structured Query Language - A standard language for managing and manipulating relational databases |
| **Supabase** | Open-source Firebase alternative providing managed PostgreSQL databases with additional features like authentication and real-time subscriptions |
| **Transaction** | A sequence of database operations that are executed as a single logical unit of work |
| **Vector** | In the context of pgvector, an array of floating-point numbers representing a point in high-dimensional space |
| **Vector Database** | A database optimized for storing and efficiently searching high-dimensional vector embeddings |

### 1.3.5 AI and Machine Learning Terms

| Term | Definition |
|------|------------|
| **Cosine Similarity** | A metric used to measure how similar two vectors are, calculated as the cosine of the angle between them (range: -1 to 1) |
| **Embedding** | A dense vector representation of text in continuous high-dimensional space (768 dimensions in Cinebase) that captures semantic meaning |
| **Feature Extraction** | The process of transforming raw data into numerical features that can be processed by machine learning algorithms |
| **Groq** | Cloud-based AI inference platform providing ultra-fast LLM API access using custom LPU (Language Processing Unit) hardware |
| **Hugging Face** | AI company and platform providing pre-trained models, datasets, and tools for natural language processing and machine learning |
| **Inference** | The process of using a trained machine learning model to make predictions on new, unseen data |
| **LLM** | Large Language Model - An AI model trained on vast amounts of text data to understand and generate human-like text |
| **llama-3.1-8b-instant** | A fast, instruction-tuned language model with 8 billion parameters, optimized for rapid inference via Groq |
| **Model** | In machine learning, a mathematical representation learned from data that can make predictions or generate outputs |
| **NLP** | Natural Language Processing - A field of AI focused on enabling computers to understand, interpret, and generate human language |
| **nomic-embed-text-v1.5** | A text embedding model that converts text into 768-dimensional vectors, optimized for semantic similarity tasks |
| **Prompt** | Input text given to a language model to generate a response or perform a specific task |
| **RAG** | Retrieval-Augmented Generation - An AI technique that combines information retrieval with text generation to produce more accurate responses |
| **Semantic Similarity** | A measure of how similar two pieces of text are in meaning rather than in exact wording (scored 0 to 1) |
| **Temperature** | A parameter controlling randomness in LLM output generation (0 = deterministic, higher = more creative/random) |
| **Token** | A basic unit of text (word, subword, or character) processed by language models; also used for API rate limiting |
| **Vector Space** | A mathematical space where vectors exist, used in embeddings to represent text in a way that preserves semantic relationships |

### 1.3.6 Networking and Protocols

| Term | Definition |
|------|------------|
| **CORS** | Cross-Origin Resource Sharing - A security feature that allows or restricts web pages from making requests to a different domain |
| **DNS** | Domain Name System - A hierarchical system that translates human-readable domain names into IP addresses |
| **HTTPS** | Hypertext Transfer Protocol Secure - An extension of HTTP that uses encryption (TLS/SSL) for secure communication |
| **HTTP Methods** | Standard request methods including GET (retrieve), POST (create), PUT (update), DELETE (remove), PATCH (partial update) |
| **IP Address** | Internet Protocol address - A numerical label assigned to each device connected to a computer network |
| **IPv4** | Internet Protocol version 4 - The fourth version of IP, using 32-bit addresses (e.g., 192.168.1.1) |
| **IPv6** | Internet Protocol version 6 - The most recent version of IP, using 128-bit addresses to accommodate more devices |
| **JSON** | JavaScript Object Notation - A lightweight data-interchange format that is easy for humans to read and machines to parse |
| **Port** | A numerical identifier in networking that allows multiple services to run on the same IP address (e.g., 80 for HTTP, 443 for HTTPS) |
| **REST** | Representational State Transfer - An architectural style for distributed systems using stateless communication via HTTP |
| **SMTP** | Simple Mail Transfer Protocol - A protocol for sending email messages between servers (default port: 25, TLS port: 587) |
| **SSL/TLS** | Secure Sockets Layer / Transport Layer Security - Cryptographic protocols for secure communication over a computer network |
| **TCP/IP** | Transmission Control Protocol / Internet Protocol - Fundamental suite of protocols for internet communication |
| **URL** | Uniform Resource Locator - A reference to a web resource specifying its location and protocol (e.g., https://example.com/path) |
| **WebSocket** | A protocol providing full-duplex communication channels over a single TCP connection, enabling real-time data exchange |

### 1.3.7 Development and Testing Tools

| Term | Definition |
|------|------------|
| **CI/CD** | Continuous Integration / Continuous Deployment - Automated practices for integrating code changes and deploying to production |
| **Git** | Distributed version control system for tracking changes in source code during software development |
| **GitHub** | Web-based platform for version control and collaboration using Git, providing repository hosting and project management tools |
| **Hot Reload** | Development feature that automatically updates the running application when code changes are detected, without full restart |
| **IDE** | Integrated Development Environment - Software application providing comprehensive facilities for software development |
| **Linting** | The process of analyzing code for potential errors, bugs, and style violations using automated tools |
| **Repository (Repo)** | A storage location for software packages, typically containing source code and version history |
| **Swagger** | A set of tools for designing, building, and documenting RESTful APIs, integrated with FastAPI for automatic API documentation |
| **Version Control** | The practice of tracking and managing changes to software code over time |

### 1.3.8 Deployment and DevOps

| Term | Definition |
|------|------------|
| **Container** | A lightweight, standalone executable package that includes everything needed to run an application (code, runtime, libraries) |
| **Docker** | Platform for developing, shipping, and running applications in isolated containers |
| **Environment** | A collection of configuration settings and resources where an application runs (development, staging, production) |
| **PaaS** | Platform as a Service - A cloud computing model providing a platform for developing, running, and managing applications |
| **Render** | Cloud platform (PaaS) for hosting web applications, databases, and background workers with automatic deployment from Git |
| **Serverless** | Cloud computing execution model where the cloud provider manages server infrastructure, billing based on actual usage |
| **Static Site** | A website with fixed content delivered to users exactly as stored, without server-side processing |
| **Supabase** | Open-source Backend-as-a-Service (BaaS) providing managed PostgreSQL databases with additional features like authentication |
| **Vercel** | Cloud platform for static sites and serverless functions, optimized for frontend frameworks like React |

### 1.3.9 Security and Authentication

| Term | Definition |
|------|------------|
| **API Key** | A unique identifier used to authenticate requests to an API, serving as both identifier and secret token |
| **Bearer Token** | An authentication token sent in the HTTP Authorization header (format: "Bearer <token>") |
| **Credentials** | Information used to verify identity, such as usernames, passwords, or API keys |
| **Encryption** | The process of encoding information so that only authorized parties can access it |
| **OAuth** | An open standard for access delegation, commonly used for token-based authentication (not used in Cinebase) |
| **Session Token** | A unique identifier assigned to a user session, used to maintain authentication state |
| **TLS** | Transport Layer Security - Cryptographic protocol providing secure communication over a network |

### 1.3.10 File Formats and Standards

| Term | Definition |
|------|------------|
| **.env** | Environment file containing configuration variables in KEY=VALUE format, typically excluded from version control |
| **CSV** | Comma-Separated Values - A plain text file format for tabular data where values are separated by commas |
| **HTML** | Hypertext Markup Language - The standard markup language for creating web pages |
| **JSON** | JavaScript Object Notation - A lightweight data format using human-readable text to store and transmit data objects |
| **Markdown** | A lightweight markup language for formatting plain text, commonly used for documentation |
| **MIME Type** | Multipurpose Internet Mail Extensions type - A standard indicating the nature and format of a file (e.g., application/pdf) |
| **PDF** | Portable Document Format - A file format for presenting documents independently of software, hardware, or operating systems |
| **UTF-8** | Unicode Transformation Format - 8-bit - A variable-width character encoding capable of encoding all possible characters |

### 1.3.11 Project-Specific Terms

| Term | Definition |
|------|------------|
| **Cinebase** | The name of this CV/Resume management and job matching platform |
| **Document** | In Cinebase context, refers to an uploaded PDF resume/CV file and its associated metadata and embeddings |
| **Job Digest** | A weekly automated email containing top job matches for a user based on their resume |
| **Job Matching** | The process of finding and ranking job postings based on semantic similarity to a user's resume |
| **JobSpy** | Python library (python-jobspy v1.1.75) for scraping job postings from multiple job boards simultaneously |
| **Match Score** | The semantic similarity score (0-1) indicating how well a job posting matches a user's resume |
| **n8n** | Open-source workflow automation tool used in Cinebase for scheduling weekly job digest emails |
| **Similarity Score** | A numerical value (0 to 1) representing how semantically similar a job description is to a resume (1 = perfect match) |

### 1.3.12 External Services and APIs

| Service/API | Description |
|-------------|-------------|
| **Glassdoor** | Job search website where users can search for jobs, review companies, and view salary information |
| **Gmail SMTP** | Email sending service provided by Google, accessible via SMTP protocol (smtp.gmail.com:587) |
| **Groq API** | Cloud-based LLM inference API providing ultra-fast text generation using llama-3.1-8b-instant model |
| **Hugging Face Inference API** | Cloud API for running machine learning models, used for generating text embeddings with nomic-embed-text-v1.5 |
| **Indeed** | One of the world's largest job search websites, aggregating job postings from thousands of websites |
| **LinkedIn** | Professional networking platform that includes job posting and job search functionality |

## 1.4 References

The following documents and resources are referenced in this SRS:

**Technical Documentation:**
1. FastAPI Documentation - https://fastapi.tiangolo.com/
2. React Documentation - https://react.dev/
3. PostgreSQL pgvector Extension - https://github.com/pgvector/pgvector
4. Hugging Face Inference API - https://huggingface.co/docs/api-inference/
5. Groq API Documentation - https://console.groq.com/docs
6. JobSpy Library - https://github.com/Bunsly/JobSpy
7. n8n Workflow Automation - https://docs.n8n.io/

**Project Documentation:**
1. `CLAUDE.md` - Project implementation guide and architecture overview
2. `CLAUDE_AGENT_SETUP_DOCUMENTATION.md` - Development agent configuration
3. GitHub Repository - https://github.com/BasilBosnjak/Cinebase

**Standards and Best Practices:**
1. IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
2. RESTful API Design Principles
3. OWASP Top 10 Web Application Security Risks

**Deployment Environments:**
1. Production Frontend - https://cinebase-sepia.vercel.app
2. Production Backend - https://cinebase-backend.onrender.com
3. Production Database - Supabase (PostgreSQL with pgvector)

## 1.5 Overview

This Software Requirements Specification is organized into the following sections:

**Section 1: Introduction** (This Section)
Provides an overview of the SRS document, including purpose, scope, definitions, references, and document organization.

**Section 2: Overall Description**
Describes the general factors affecting the product and its requirements, including:
- Product perspective and system interfaces
- User characteristics and personas
- Operating environment and constraints
- Assumptions and dependencies

**Section 3: Specific Requirements**
Details the functional and non-functional requirements, including:
- Functional requirements for each system component
- External interface requirements (user, hardware, software, communications)
- Performance requirements
- Security requirements
- Quality attributes (reliability, availability, maintainability)

**Section 4: System Features**
Provides detailed descriptions of each major system feature:
- User authentication and management
- Document upload and storage
- AI-powered embedding generation
- Job search and matching algorithms
- Weekly digest automation

**Section 5: Non-Functional Requirements**
Specifies constraints and quality attributes:
- Performance benchmarks (response times, throughput)
- Security requirements (data protection, authentication)
- Usability requirements (user experience, accessibility)
- Scalability and reliability expectations

**Section 6: Other Requirements**
Covers additional considerations:
- Database schema and data models
- API endpoint specifications
- Deployment architecture
- Maintenance and support requirements

**Appendices:**
Supplementary information including:
- Appendix A: Use Case Diagrams
- Appendix B: Data Flow Diagrams
- Appendix C: Database Schema
- Appendix D: API Endpoint Reference
- Appendix E: Glossary

---

**Document Control:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | Development Team | Initial draft - Introduction chapter |

**Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Manager | _______________ | _______________ | ________ |
| Lead Developer | _______________ | _______________ | ________ |
| QA Lead | _______________ | _______________ | ________ |
| Product Owner | _______________ | _______________ | ________ |

---

# 2. Detailed Scope

## 2.1 Product Perspective

**Cinebase** is a standalone, web-based application that operates as an independent system within the broader job search ecosystem. The platform does not replace existing job boards but rather aggregates and enhances them by providing intelligent matching capabilities.

### 2.1.1 System Context

The system exists within the following context:

**External Systems Integration:**
- **Job Board Platforms:** Cinebase integrates with Indeed, LinkedIn, and Glassdoor via the JobSpy library to scrape publicly available job postings
- **AI Service Providers:** The system relies on cloud-based AI APIs (Hugging Face for embeddings, Groq for language processing) for natural language understanding
- **Email Infrastructure:** Weekly digest emails are delivered through standard SMTP protocols (Gmail SMTP server)
- **Cloud Infrastructure:** Frontend hosted on Vercel, backend on Render, database on Supabase

**Data Flow:**
1. User uploads CV/resume → System stores PDF and extracts text
2. Text content → AI service generates 768-dimensional vector embedding
3. User requests job search → System extracts job title from resume using LLM
4. Job title → JobSpy library scrapes job boards for matching postings
5. Job descriptions → AI service generates embeddings for each job
6. System calculates similarity scores → Ranked results returned to user
7. Weekly automation → System fetches jobs, scores them, and emails results

### 2.1.2 System Boundaries

**What the System Does:**
- Stores and manages user CV/resume documents
- Processes documents using text extraction and AI analysis
- Performs semantic matching between resumes and job postings
- Aggregates jobs from multiple external job boards
- Provides ranked job recommendations with similarity scores
- Automates weekly job digest email delivery

**What the System Does NOT Do:**
- Create, edit, or format resumes/CVs
- Submit job applications on behalf of users
- Communicate directly with employers
- Track application status or interview scheduling
- Provide career counseling or resume feedback
- Store job application history
- Process payments or offer premium features

### 2.1.3 User Interfaces

The application provides a modern, responsive web interface accessible through standard web browsers:

**Authentication Interface:**
- Email-only login form (no password required)
- Simple, clean design with minimal friction

**Dashboard Interface:**
- Document upload area with drag-and-drop support
- List of uploaded CV/resume documents with metadata (filename, upload date, file size)
- Statistics display showing total documents and recent uploads
- "Find Jobs" action button for each document
- Delete/manage document options

**Job Matching Interface:**
- Job search parameters form (location, remote preference, number of results)
- Loading indicator during job search and matching process
- Results table displaying:
  - Job title and company name
  - Location and remote status
  - Similarity score (0-100% match)
  - Job description preview
  - Salary information (when available)
  - Direct link to original job posting
- Results sorted by similarity score (highest to lowest)

**Visual Design:**
- Clean, modern interface using Tailwind CSS
- Mobile-responsive layout (accessible on tablets and smartphones)
- Consistent color scheme and typography
- Loading states and error messages for all async operations

### 2.1.4 Hardware Interfaces

As a web-based application, Cinebase has no direct hardware interfaces. The system operates through standard web browsers and requires:

**Client-Side (User):**
- Device capable of running a modern web browser (desktop, laptop, tablet, smartphone)
- Internet connection (minimum 1 Mbps recommended)
- Display resolution of at least 360px width (mobile) or 1024px (desktop recommended)

**Server-Side (Infrastructure):**
- Cloud-hosted backend servers (Render platform) running Linux containers
- PostgreSQL database server with pgvector extension (Supabase managed service)
- Static file hosting for frontend (Vercel CDN)

### 2.1.5 Software Interfaces

**Frontend Dependencies:**
- **Browser Requirements:** Modern browsers with ES6+ support (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **JavaScript Framework:** React 18.x for user interface rendering
- **Build Tool:** Vite 4.x for development and production builds
- **HTTP Client:** Fetch API for backend communication
- **Styling:** Tailwind CSS 3.x for responsive design

**Backend Dependencies:**
- **Runtime Environment:** Python 3.11.7
- **Web Framework:** FastAPI 0.104.1 for REST API implementation
- **Database ORM:** SQLAlchemy 2.0.23 for database operations
- **PDF Processing:** pypdf 3.17.4 for text extraction from uploaded documents
- **Job Scraping:** python-jobspy 1.1.75 for aggregating jobs from multiple boards
- **HTTP Client:** httpx 0.25.2 for async API calls to AI services

**Database:**
- **RDBMS:** PostgreSQL 15+ with pgvector extension
- **Vector Extension:** pgvector 0.2.4 for storing and querying 768-dimensional embeddings
- **Connection:** psycopg2-binary 2.9.9 for database connectivity

**External API Services:**
- **Hugging Face Inference API:**
  - Endpoint: `https://router.huggingface.co/pipeline/feature-extraction/nomic-ai/nomic-embed-text-v1.5`
  - Authentication: Bearer token (API key)
  - Purpose: Generate 768-dimensional embeddings from text
  - Rate Limits: Subject to Hugging Face free tier limits

- **Groq LLM API:**
  - Endpoint: `https://api.groq.com/openai/v1/chat/completions`
  - Model: llama-3.1-8b-instant
  - Authentication: Bearer token (API key)
  - Purpose: Extract job titles and analyze resume content
  - Rate Limits: Subject to Groq free tier limits

**Workflow Automation:**
- **n8n Platform:** Self-hosted workflow automation (optional for development)
- **Trigger:** Cron schedule (Monday 9:00 AM weekly)
- **Action:** HTTP request to backend `/jobs/weekly-digest` endpoint
- **Email Delivery:** SMTP (Gmail) for sending formatted job digest emails

### 2.1.6 Communication Interfaces

**Client-Server Communication:**
- **Protocol:** HTTPS (TLS 1.2+) for secure data transmission
- **Data Format:** JSON for all API requests and responses
- **API Architecture:** RESTful design with standard HTTP methods (GET, POST, DELETE)
- **CORS Policy:** Configured to allow frontend domain (https://cinebase-sepia.vercel.app) and localhost for development

**Email Communication:**
- **Protocol:** SMTP over TLS (port 587)
- **Provider:** Gmail SMTP server (smtp.gmail.com)
- **Authentication:** App-specific password
- **Content Type:** HTML emails with fallback to plain text

**Database Communication:**
- **Protocol:** PostgreSQL wire protocol over SSL
- **Connection Pooling:** Supabase connection pooler (port 6543) for IPv4 compatibility
- **Connection String Format:** `postgresql://user:password@host:6543/database`

### 2.1.7 Memory and Storage

**Client-Side Storage:**
- **Browser LocalStorage:** User authentication state (user ID, email, login timestamp)
- **Storage Limit:** 5-10 MB (browser-dependent)
- **Persistence:** Data persists across browser sessions until manual logout

**Server-Side Storage:**
- **File Storage:** User-uploaded PDF files stored on Render ephemeral filesystem
  - Path structure: `uploads/{user_id}/{document_id}.pdf`
  - Maximum file size: 10 MB per document
  - Lifecycle: Files persist for application lifetime (may be lost on container restart)

- **Database Storage:**
  - User records: ~200 bytes per user (UUID, email, timestamps)
  - Document records: ~500 bytes + ~3 KB for embedding vector per document
  - Estimated storage: 3-4 KB per uploaded resume
  - Text content: Up to 50 KB per document (extracted text from PDF)

## 2.2 Product Functions

This section details the major functions of the Cinebase system, organized by functional area.

### 2.2.1 User Authentication and Management

**Function:** Email-Based Authentication
- **Description:** Users authenticate using only their email address without requiring password creation or OAuth integration
- **Input:** Email address (valid format validated client-side and server-side)
- **Process:**
  1. User enters email on login page
  2. System checks if email exists in users table
  3. If exists, user data retrieved and returned
  4. If not exists, system automatically creates new user record
  5. User session established and stored in browser localStorage
- **Output:** User authentication token (user ID, email, creation timestamp)
- **Business Logic:** No password validation, no email verification, no CAPTCHA
- **Error Handling:** Invalid email format rejected with error message

**Function:** User Session Management
- **Description:** Maintain user authentication state across page refreshes and navigation
- **Storage:** Browser localStorage persists user ID and email
- **Session Lifecycle:** Remains active until explicit logout or localStorage cleared
- **Protected Routes:** Dashboard and document management pages require valid session

### 2.2.2 Document Upload and Management

**Function:** PDF Upload
- **Description:** Users upload their CV/resume in PDF format for processing and storage
- **Input:** PDF file via file input or drag-and-drop interface
- **Validation:**
  - File type must be `application/pdf` (validated by MIME type)
  - File size must not exceed 10 MB
  - User must be authenticated
- **Process:**
  1. User selects PDF file from local filesystem
  2. Frontend validates file type and size
  3. File uploaded to backend via multipart/form-data POST request
  4. Backend saves file to user-specific directory: `uploads/{user_id}/{document_id}.pdf`
  5. Text extraction performed using pypdf library
  6. Document record created in database with metadata
  7. Background task initiated to generate embedding
- **Output:**
  - Document record with unique UUID
  - File path, original filename, file size, MIME type
  - Extracted text content stored in database
  - Status: "processed" after successful text extraction
- **Background Processing:** Embedding generation occurs asynchronously without blocking upload response

**Function:** Text Extraction from PDF
- **Description:** Extract readable text content from uploaded PDF files
- **Input:** PDF file path on server filesystem
- **Technology:** pypdf library for Python
- **Process:**
  1. Open PDF file using pypdf
  2. Iterate through all pages
  3. Extract text from each page
  4. Concatenate text with page breaks
  5. Store full text in document.content field (TEXT type)
- **Output:** Plain text string (up to ~50 KB typical)
- **Error Handling:** If extraction fails, store error message in content field
- **Character Encoding:** UTF-8 for all text content

**Function:** Vector Embedding Generation
- **Description:** Generate semantic vector representation of resume content for similarity matching
- **Input:** Extracted text content (first 8000 characters)
- **Technology:** Hugging Face Inference API with nomic-embed-text-v1.5 model
- **Process:**
  1. Background task triggered after document creation
  2. Text content truncated to 8000 characters (API limit)
  3. HTTP POST request to Hugging Face API with text payload
  4. API returns 768-dimensional float vector
  5. Vector stored in database using pgvector extension
  6. Database UPDATE query sets embedding column: `UPDATE documents SET embedding = :embedding::vector WHERE id = :document_id`
- **Output:** 768-dimensional vector stored in PostgreSQL
- **Execution Mode:** Non-blocking background task using FastAPI BackgroundTasks
- **Logging:** Success/failure logged with document ID for debugging
- **Retry Logic:** None (single attempt per upload)

**Function:** Document Listing
- **Description:** Display all documents uploaded by the authenticated user
- **Input:** User ID from session
- **Query:** `SELECT * FROM documents WHERE user_id = :user_id ORDER BY created_at DESC`
- **Output:** Array of document records with:
  - Document ID, filename, upload date, file size
  - Processing status
  - Embedding generation status (true/false)
- **UI Display:** Cards or table rows showing document metadata
- **Actions Available:** Find Jobs button (if embedding exists), Delete button

**Function:** Document Deletion
- **Description:** Remove document record and associated file from system
- **Input:** Document ID and user ID
- **Authorization:** User can only delete their own documents
- **Process:**
  1. Verify document belongs to authenticated user
  2. Delete file from filesystem: `os.remove(file_path)`
  3. Delete database record: `DELETE FROM documents WHERE id = :document_id AND user_id = :user_id`
- **Output:** Success confirmation message
- **Error Handling:** 404 if document not found, 403 if unauthorized

**Function:** User Statistics
- **Description:** Display aggregate statistics about user's documents
- **Metrics Calculated:**
  - Total number of documents uploaded
  - Documents by processing status (processed, failed, etc.)
  - Number of documents uploaded in last 7 days
- **Query:** Aggregate queries using COUNT() and GROUP BY
- **Display:** Dashboard statistics cards showing metrics
- **Refresh:** Updated on each page load and after document upload/deletion

### 2.2.3 AI-Powered Job Matching

**Function:** Job Title Extraction from Resume
- **Description:** Automatically determine the most relevant job title based on resume content using LLM
- **Input:** Resume text content (first 3000 characters)
- **Technology:** Groq LLM API with llama-3.1-8b-instant model
- **Prompt Template:**
  ```
  Based on this CV/resume content, what is the most relevant job title this person should search for?
  Return ONLY the job title (2-4 words max), nothing else.
  Examples: "Software Engineer", "Data Analyst", "Marketing Specialist"

  CV Content: {content}

  Job title:
  ```
- **Process:**
  1. Send prompt to Groq API with low temperature (0.1) for deterministic output
  2. Receive text response (max 20 tokens)
  3. Clean response: strip quotes, remove prefixes like "Based on", "The"
  4. Validate length (must be < 50 characters)
- **Output:** Job title string (e.g., "Software Engineer", "Marketing Specialist")
- **Fallback:** Return "general" if extraction fails or response invalid
- **Logging:** Extracted job title logged for debugging

**Function:** Multi-Platform Job Search
- **Description:** Search for jobs across Indeed, LinkedIn, and Glassdoor based on extracted job title
- **Input:**
  - Search term (job title from resume)
  - Location (default: "Remote")
  - Number of results wanted (default: 10)
  - Remote preference (default: true)
- **Technology:** python-jobspy library (v1.1.75)
- **Process:**
  1. Call `scrape_jobs()` function with parameters
  2. Library scrapes specified job boards in parallel
  3. Results returned as pandas DataFrame
  4. DataFrame converted to list of dictionaries
  5. Each job includes: id, title, company, location, job_url, description, salary (if available)
- **Execution:** Run in background thread pool executor (synchronous library in async context)
- **Supported Platforms:** Indeed, LinkedIn, Glassdoor
- **Country Filter:** USA (configurable via country_indeed parameter)
- **Rate Limiting:** Subject to job board rate limits (handled by JobSpy library)

**Function:** Job Description Embedding Generation
- **Description:** Generate semantic vector for each job description to enable similarity comparison
- **Input:** Job text (concatenation of title, company, and description)
- **Technology:** Same as resume embedding (Hugging Face + nomic-embed-text-v1.5)
- **Process:**
  1. For each job in search results:
     - Combine: `{title} at {company}. {description}`
     - Truncate to 8000 characters
     - Send to Hugging Face API
     - Receive 768-dimensional vector
  2. Store embedding temporarily in memory (not persisted to database)
- **Parallelization:** Embeddings generated sequentially (to avoid API rate limits)
- **Error Handling:** Skip job if embedding generation fails, log error, continue with next job

**Function:** Semantic Similarity Calculation
- **Description:** Calculate cosine similarity between resume embedding and job embedding
- **Input:** Two 768-dimensional vectors (resume_embedding, job_embedding)
- **Algorithm:** Cosine Similarity
  ```
  similarity = dot(A, B) / (norm(A) * norm(B))
  ```
- **Implementation:** NumPy library for vector operations
- **Output:** Float value between -1.0 (opposite) and 1.0 (identical)
- **Interpretation:**
  - 0.9-1.0: Extremely strong match
  - 0.8-0.9: Very strong match
  - 0.7-0.8: Strong match
  - 0.6-0.7: Good match
  - < 0.6: Weak match
- **Precision:** Rounded to 4 decimal places for display

**Function:** Job Ranking and Results Presentation
- **Description:** Sort jobs by similarity score and return ranked results to user
- **Input:** List of jobs with calculated similarity scores
- **Sorting:** Descending order (highest similarity first)
- **Response Format:**
  ```json
  {
    "query": "Software Engineer",
    "total_jobs_fetched": 25,
    "matches": [
      {
        "id": "job_123",
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "location": "Remote",
        "job_url": "https://...",
        "description": "We are seeking...",
        "salary_min": 100000,
        "salary_max": 150000,
        "similarity_score": 0.8543
      },
      ...
    ]
  }
  ```
- **Description Truncation:** Job descriptions truncated to 500 characters for display
- **UI Rendering:** Results displayed in table/card format with color-coded similarity scores

### 2.2.4 Weekly Job Digest Automation

**Function:** Scheduled Job Digest Generation
- **Description:** Automatically generate weekly job recommendations for all users with uploaded resumes
- **Trigger:** n8n cron schedule (Monday 9:00 AM UTC)
- **Endpoint:** `GET /jobs/weekly-digest`
- **Process:**
  1. Query all users with documents that have embeddings
  2. For each user:
     - Get most recent document
     - Extract job title from resume content
     - Search for 15 jobs using JobSpy
     - Generate embeddings for all jobs
     - Calculate similarity scores
     - Select top 5 matches
  3. Return digest data for all users
- **Output Format:**
  ```json
  {
    "total_users": 3,
    "digests": [
      {
        "user_id": "uuid",
        "email": "user@example.com",
        "document_name": "resume.pdf",
        "search_term": "Software Engineer",
        "top_matches": [array of 5 jobs]
      },
      ...
    ]
  }
  ```
- **Performance:** Processes users sequentially to avoid API rate limits

**Function:** Email Digest Formatting and Delivery
- **Description:** Format job matches into HTML email and send to users
- **Technology:** n8n workflow automation
- **Email Template:**
  - Subject: "Your Weekly Job Digest - [Number] New Matches"
  - HTML body with:
    - Personalized greeting
    - Summary of search query
    - Table of top 5 jobs with title, company, similarity score
    - "View Job" buttons linking to original postings
    - Footer with unsubscribe information
- **SMTP Configuration:**
  - Server: smtp.gmail.com
  - Port: 587 (TLS)
  - Authentication: App-specific password
- **From Address:** Configured email (e.g., noreply@cinebase.com)
- **To Address:** User's registered email
- **Delivery:** Sent via n8n Email node after HTTP request to backend completes

## 2.3 User Classes and Characteristics

### 2.3.1 Primary User Class: Job Seekers

**Demographics:**
- **Age Range:** 18-65 years old
- **Education Level:** High school diploma to advanced degrees
- **Geographic Location:** Primarily United States (due to job board country filtering)
- **Employment Status:** Unemployed, employed but seeking new opportunities, students

**Technical Proficiency:**
- **Computer Literacy:** Basic to intermediate (comfortable using web browsers, email)
- **File Management:** Ability to locate and upload PDF files from local storage
- **Internet Usage:** Regular internet users with access to email
- **Mobile vs Desktop:** Mixed usage (responsive design accommodates both)

**User Goals:**
- Find job opportunities matching their skills and experience
- Save time by avoiding manual searches across multiple job boards
- Stay informed about new job postings without daily checking
- Understand which jobs are most relevant to their qualifications
- Apply to positions with confidence that they match requirements

**Frequency of Use:**
- **Initial Setup:** One-time upload of resume
- **Active Job Search:** Daily/weekly checking of job matches
- **Passive Monitoring:** Monthly email digest review
- **Resume Updates:** Periodic (every few months or after major career changes)

**Primary Use Cases:**
1. Upload resume when starting job search
2. Click "Find Jobs" to get immediate ranked matches
3. Review similarity scores to prioritize applications
4. Click through to job boards to read full descriptions and apply
5. Receive and review weekly email digests
6. Update resume when skills or experience change

### 2.3.2 Secondary User Class: System Administrators

**Responsibilities:**
- Deploy and maintain backend infrastructure on Render
- Monitor application logs for errors and performance issues
- Manage environment variables and API keys
- Ensure database backups and data integrity (Supabase management)
- Configure n8n workflow for weekly digests
- Update dependencies and apply security patches

**Technical Skills:**
- **Backend:** Python, FastAPI, PostgreSQL knowledge
- **DevOps:** Cloud platform familiarity (Render, Vercel, Supabase)
- **Monitoring:** Log analysis, error tracking
- **Database:** SQL queries, pgvector extension understanding

**Access Level:**
- Full server access via Render dashboard
- Database admin access via Supabase console
- n8n workflow editor access
- Git repository access for code updates

## 2.4 Operating Environment

### 2.4.1 Client-Side Environment

**Supported Browsers:**
- Google Chrome 90+ (recommended)
- Mozilla Firefox 88+
- Apple Safari 14+
- Microsoft Edge 90+
- Opera 76+

**Operating Systems:**
- **Desktop:** Windows 10/11, macOS 10.14+, Linux (Ubuntu, Fedora, etc.)
- **Mobile:** iOS 14+, Android 9+

**Screen Resolutions:**
- **Minimum:** 360px width (mobile phones)
- **Recommended:** 1024px width or higher (desktop/tablet)
- **Maximum:** No upper limit (responsive design scales)

**Network Requirements:**
- **Minimum Bandwidth:** 1 Mbps (for basic usage)
- **Recommended:** 5 Mbps (for smooth experience with large file uploads)
- **Latency:** < 200ms for responsive UI interactions

**Browser Requirements:**
- JavaScript enabled (application will not function without it)
- LocalStorage enabled (for authentication state)
- Cookies enabled (for session management)
- TLS 1.2+ support (for secure HTTPS connections)

### 2.4.2 Server-Side Environment

**Backend Hosting Platform:**
- **Provider:** Render (cloud PaaS)
- **Region:** US East (configurable)
- **Container:** Docker-based Linux container
- **Runtime:** Python 3.11.7
- **Web Server:** Gunicorn with Uvicorn workers
- **Process Manager:** Gunicorn (production) / Uvicorn (development)

**Frontend Hosting Platform:**
- **Provider:** Vercel
- **Deployment:** Static site generation (SSG) with client-side routing
- **CDN:** Global Vercel CDN for asset delivery
- **Build Process:** Vite production build

**Database Environment:**
- **Provider:** Supabase (managed PostgreSQL)
- **PostgreSQL Version:** 15+
- **Extensions:** pgvector 0.2.4
- **Connection Pooling:** PgBouncer (port 6543)
- **Backup:** Automated daily backups (Supabase managed)

**Workflow Automation:**
- **Platform:** n8n (self-hosted for development, cloud-hosted for production)
- **Hosting:** Local development server or n8n cloud
- **Endpoint:** Accessible via HTTP for backend API calls

### 2.4.3 Third-Party Service Dependencies

**AI Service APIs:**
- **Hugging Face:**
  - Availability: 99.9% uptime SLA (cloud service)
  - Rate Limits: Free tier limits apply
  - Geographic Availability: Global

- **Groq:**
  - Availability: 99.9% uptime SLA
  - Rate Limits: Free tier limits apply
  - Geographic Availability: Global

**Job Board Platforms:**
- **Indeed, LinkedIn, Glassdoor:**
  - Availability: Dependent on public web scraping (no SLA)
  - Rate Limits: Subject to anti-scraping measures
  - Data Freshness: Real-time job postings

**Email Service:**
- **Gmail SMTP:**
  - Availability: 99.9% uptime
  - Sending Limits: 500 emails/day (free Gmail account)
  - Deliverability: Subject to spam filter policies

## 2.5 Design and Implementation Constraints

### 2.5.1 Regulatory Constraints

**Data Privacy:**
- **GDPR Compliance:** Not currently implemented (system stores user email and resume content without explicit consent mechanisms)
- **CCPA Compliance:** Not currently implemented (no data deletion request process)
- **Data Storage:** User data stored indefinitely without retention policies

**Web Scraping Legality:**
- JobSpy library scrapes publicly available job postings
- Compliance with job board Terms of Service not explicitly verified
- Risk of service disruption if job boards implement anti-scraping measures

### 2.5.2 Technical Constraints

**File Format Limitation:**
- Only PDF files supported for resume upload
- No support for DOCX, TXT, or other document formats
- PDF text extraction quality depends on PDF structure (image-based PDFs may fail)

**Embedding Model Fixed:**
- 768-dimensional embedding model (nomic-embed-text-v1.5)
- Cannot be changed without database schema migration
- Model selection dictated by free-tier cloud API availability

**Authentication Simplicity:**
- Email-only authentication (no password security)
- No multi-factor authentication (MFA)
- Vulnerable to email spoofing (no verification step)

**API Rate Limits:**
- Hugging Face free tier: Limited requests per hour
- Groq free tier: Limited tokens per day
- JobSpy scraping: Subject to IP-based rate limiting

**Platform-Specific Constraints:**
- **Render Free Tier:**
  - Service sleeps after 15 minutes of inactivity (cold start delays)
  - Ephemeral filesystem (uploaded files lost on container restart)
  - 512 MB RAM limit

- **Vercel Free Tier:**
  - 100 GB bandwidth per month
  - Function execution timeout: 10 seconds

- **Supabase Free Tier:**
  - 500 MB database storage
  - Paused after 7 days of inactivity

### 2.5.3 Interface Constraints

**Browser Compatibility:**
- No support for Internet Explorer (legacy browser)
- Requires modern JavaScript features (ES6+)
- Progressive Web App (PWA) features not implemented

**Mobile Limitations:**
- Responsive design but not optimized for mobile-first experience
- File upload via mobile browser may have limitations
- No native mobile app (iOS/Android)

### 2.5.4 Development Constraints

**Technology Stack Fixed:**
- Backend: Python with FastAPI (cannot switch to Node.js, Go, etc.)
- Frontend: React with Vite (cannot switch to Vue, Angular, etc.)
- Database: PostgreSQL with pgvector (cannot switch to MongoDB, MySQL, etc.)

**No Offline Functionality:**
- Requires active internet connection for all operations
- No local caching of job results
- No service worker for offline PWA capabilities

**Single Language Support:**
- English-only interface and content
- No internationalization (i18n) or localization (l10n)

## 2.6 Assumptions and Dependencies

### 2.6.1 Assumptions

**User Behavior Assumptions:**
1. Users have their resume/CV already prepared in PDF format
2. Users are comfortable with English-language interface
3. Users have valid email addresses for authentication and notifications
4. Users understand that job matching is based on semantic similarity, not exact keyword matching
5. Users will click through to job board sites to submit applications

**Technical Assumptions:**
1. Users have modern web browsers with JavaScript enabled
2. Internet connection is stable during file upload
3. PDF files contain extractable text (not just scanned images)
4. Job boards will continue to allow public access to job postings
5. Third-party AI APIs will maintain current pricing (free tier availability)

**Business Assumptions:**
1. Free tier services (Render, Vercel, Supabase, Hugging Face, Groq) will remain available
2. Job search is a recurring need (weekly digests will be utilized)
3. Users will find semantic matching more valuable than keyword-based search
4. No legal challenges from job boards regarding web scraping

### 2.6.2 Dependencies

**External Service Dependencies:**

| Service | Dependency Type | Impact if Unavailable |
|---------|----------------|----------------------|
| Hugging Face API | Critical | Embedding generation fails, job matching unavailable |
| Groq API | High | Job title extraction fails, falls back to "general" |
| JobSpy Library | Critical | Job search completely unavailable |
| Indeed/LinkedIn/Glassdoor | High | Reduced job results if individual boards are down |
| Gmail SMTP | Medium | Weekly digest emails not delivered |
| Render | Critical | Backend API completely unavailable |
| Vercel | Critical | Frontend application inaccessible |
| Supabase | Critical | Database unavailable, all data operations fail |
| n8n | Low | Weekly automation fails, manual triggers still work |

**Library Dependencies:**
- Python dependencies defined in `requirements.txt` (16 packages)
- Frontend dependencies defined in `package.json`
- Any library updates may introduce breaking changes

**Infrastructure Dependencies:**
- DNS resolution for all cloud services
- SSL/TLS certificates for HTTPS (managed by hosting providers)
- CDN availability for static asset delivery (Vercel)

**Data Dependencies:**
- Resume content quality affects job title extraction accuracy
- Job description quality affects similarity matching accuracy
- Email deliverability depends on SMTP reputation and spam filters

**Development Dependencies:**
- Git repository access (GitHub)
- Local development environment setup (Python venv, Node.js)
- API keys for Hugging Face and Groq (developer accounts)

### 2.6.3 Success Criteria

For Cinebase to be considered successfully implemented, the following criteria must be met:

**Functional Success:**
1. Users can upload PDF resumes and see them listed in dashboard
2. Vector embeddings are successfully generated for 95%+ of uploaded resumes
3. Job matching returns relevant results with similarity scores > 0.6 for top 5 matches
4. Weekly digest emails are delivered successfully to all active users
5. Application responds to user actions within 3 seconds (excluding job search which may take 30-60 seconds)

**Technical Success:**
1. Backend API achieves 99% uptime (excluding Render cold starts)
2. Database queries execute in < 1 second
3. File uploads complete successfully for files up to 10 MB
4. No data loss or corruption in database
5. API rate limits from third-party services are not exceeded

**User Experience Success:**
1. Login process completes in 2 clicks or fewer
2. Dashboard loads in < 2 seconds
3. Error messages are clear and actionable
4. Mobile interface is fully functional on devices 360px width and above
5. Job results are presented in a scannable, easy-to-read format

---

**End of Section 2: Detailed Scope**

---

# 3. Project Requirements

## 3.1 Functional Requirements

This section describes the specific behaviors and functions that Cinebase must provide to meet user needs and business objectives.

### FR-1: User Authentication

**Description:**
As a user, I should be able to log in using only my email address without creating a password, so that I can quickly access the platform without the friction of traditional authentication.

**Acceptance Criteria:**
1. Login form shall be accessible to unauthenticated users on the landing page
2. Email input field shall validate email format client-side before submission
3. Upon entering a valid email and clicking submit, the system shall check if the user exists in the database
4. If the user exists, the system shall return user data (ID, email, created_at) and establish a session
5. If the user does not exist, the system shall automatically create a new user record with the provided email
6. User session data shall be stored in browser LocalStorage for persistence across page refreshes
7. The system shall redirect authenticated users to the dashboard automatically

### FR-2: PDF Resume Upload

**Description:**
As a user, I should be able to upload my CV/resume in PDF format, so that the system can analyze my qualifications and match me with relevant jobs.

**Acceptance Criteria:**
1. Document upload functionality shall only be available to authenticated users
2. The upload interface shall support both file input selection and drag-and-drop interaction
3. The system shall validate that the uploaded file is in PDF format (MIME type: application/pdf)
4. The system shall reject files larger than 10 MB with an appropriate error message
5. Upon successful upload, the system shall save the PDF file to user-specific storage directory
6. The system shall extract text content from the PDF using pypdf library
7. The system shall create a document record in the database with metadata (filename, file size, upload date)
8. The system shall trigger a background task to generate vector embeddings without blocking the upload response
9. The user shall receive immediate confirmation of successful upload with document details displayed

###FR-3: Text Extraction from PDF

**Description:**
As the system, I should automatically extract readable text from uploaded PDF files, so that resume content can be analyzed by AI services.

**Acceptance Criteria:**
1. Text extraction shall occur immediately after file upload
2. The system shall extract text from all pages of the PDF document
3. Extracted text shall be stored in the documents table in the content column (TEXT type)
4. If text extraction fails, the system shall store an error message in the content field
5. The document status shall be set to "processed" after successful extraction
6. Extracted text shall be UTF-8 encoded

### FR-4: Vector Embedding Generation

**Description:**
As the system, I should generate semantic vector embeddings from resume text content, so that accurate job matching can be performed using similarity calculations.

**Acceptance Criteria:**
1. Embedding generation shall occur as a background task after document upload
2. The system shall truncate text content to first 8000 characters before sending to AI API
3. The system shall call Hugging Face Inference API with nomic-embed-text-v1.5 model
4. The API shall return a 768-dimensional floating-point vector
5. The system shall store the vector in the database using pgvector extension
6. The embedding column shall be updated via SQL: `UPDATE documents SET embedding = :embedding::vector WHERE id = :document_id`
7. Success or failure shall be logged with document ID for debugging purposes
8. The system shall not retry if embedding generation fails (single attempt per upload)

### FR-5: Document Listing and Management

**Description:**
As a user, I should be able to view all my uploaded resumes and manage them, so that I can organize my documents and delete outdated versions.

**Acceptance Criteria:**
1. The dashboard shall display all documents uploaded by the authenticated user
2. Documents shall be sorted by upload date in descending order (newest first)
3. Each document listing shall display: filename, upload date, file size, processing status
4. The listing shall indicate whether embedding generation is complete (ready for job matching)
5. Each document shall have a "Find Jobs" button (enabled only if embedding exists)
6. Each document shall have a "Delete" button
7. Clicking delete shall remove the document record from database and file from storage
8. The system shall verify user owns the document before allowing deletion (authorization check)
9. The system shall provide visual feedback for successful deletion

### FR-6: User Statistics Dashboard

**Description:**
As a user, I should see aggregate statistics about my uploaded documents, so that I can track my activity on the platform.

**Acceptance Criteria:**
1. The dashboard shall display total number of documents uploaded
2. The dashboard shall show documents grouped by processing status
3. The dashboard shall display count of documents uploaded in the last 7 days
4. Statistics shall update automatically after document upload or deletion
5. Statistics shall be calculated via SQL aggregate queries (COUNT, GROUP BY)

### FR-7: Job Title Extraction from Resume

**Description:**
As the system, I should automatically determine the most relevant job title from resume content using AI, so that job searches are accurately targeted to the user's qualifications.

**Acceptance Criteria:**
1. Job title extraction shall occur when user clicks "Find Jobs" button
2. The system shall send the first 3000 characters of resume content to Groq LLM API
3. The prompt shall instruct the LLM to return only a job title (2-4 words)
4. The system shall use low temperature (0.1) for deterministic output
5. The response shall be cleaned (remove quotes, prefixes like "Based on", "The")
6. The extracted job title shall be validated to be less than 50 characters
7. If extraction fails or response is invalid, the system shall use "general" as fallback
8. The extracted job title shall be logged for debugging purposes

### FR-8: Multi-Platform Job Search

**Description:**
As the system, I should search for jobs across Indeed, LinkedIn, and Glassdoor simultaneously, so that users receive comprehensive job recommendations from multiple sources.

**Acceptance Criteria:**
1. Job search shall be triggered when user clicks "Find Jobs" on a document
2. The system shall use the extracted job title as the search term
3. The system shall call python-jobspy library with parameters: search_term, location, results_wanted, is_remote
4. Default parameters shall be: location="Remote", results_wanted=10, is_remote=true
5. The JobSpy library shall scrape Indeed, LinkedIn, and Glassdoor in parallel
6. Results shall be returned as a list of job dictionaries containing: id, title, company, location, job_url, description, salary (if available)
7. The search shall execute in a background thread pool to avoid blocking async operations
8. If no jobs are found, the system shall return an empty results array with appropriate message

### FR-9: Job Description Embedding and Similarity Calculation

**Description:**
As the system, I should generate embeddings for each job description and calculate similarity scores against the user's resume, so that jobs can be ranked by relevance.

**Acceptance Criteria:**
1. For each job in search results, the system shall create combined text: "{title} at {company}. {description}"
2. The combined text shall be truncated to 8000 characters
3. The system shall send each job text to Hugging Face API to generate 768-dimensional embedding
4. The system shall calculate cosine similarity between resume embedding and job embedding
5. Cosine similarity formula: `similarity = dot(A, B) / (norm(A) * norm(B))`
6. Similarity score shall be a float between -1.0 and 1.0
7. The score shall be rounded to 4 decimal places
8. If embedding generation fails for a job, the system shall skip it and continue with next job
9. All errors shall be logged with job ID

### FR-10: Job Ranking and Results Presentation

**Description:**
As a user, I should receive a ranked list of job matches with similarity scores, so that I can prioritize which jobs to apply for based on how well they match my qualifications.

**Acceptance Criteria:**
1. Job results shall be sorted by similarity score in descending order (highest match first)
2. The response shall include: query (search term), total_jobs_fetched, matches array
3. Each match shall contain: id, title, company, location, job_url, description (truncated to 500 chars), salary_min, salary_max, similarity_score
4. The frontend shall display results in a table or card format
5. Similarity scores shall be displayed as percentages (0.8543 → 85.43%)
6. Each job shall have a link to the original posting on the job board
7. Job descriptions shall be truncated with "..." indicator if longer than 500 characters
8. The system shall display appropriate message if no jobs are found

### FR-11: Weekly Job Digest Automation

**Description:**
As a user, I should automatically receive a weekly email with top job matches based on my resume, so that I stay informed of new opportunities without manual checking.

**Acceptance Criteria:**
1. The system shall have an endpoint `/jobs/weekly-digest` callable by n8n workflow
2. The endpoint shall query all users who have documents with generated embeddings
3. For each user, the system shall retrieve their most recent document
4. The system shall extract job title from resume content using LLM
5. The system shall search for 15 jobs using JobSpy
6. The system shall generate embeddings and calculate similarity scores for all jobs
7. The system shall select the top 5 matches by similarity score
8. The response shall include: total_users, digests array with user_id, email, document_name, search_term, top_matches
9. n8n workflow shall trigger every Monday at 9:00 AM UTC
10. n8n shall format results into HTML email and send via Gmail SMTP

### FR-12: Email Digest Delivery

**Description:**
As a user, I should receive a well-formatted HTML email with my top job matches, so that I can quickly review opportunities directly from my inbox.

**Acceptance Criteria:**
1. Email subject shall be: "Your Weekly Job Digest - [Number] New Matches"
2. Email shall include personalized greeting with user's email
3. Email body shall display search query used for job matching
4. Email shall include a table of top 5 jobs with: title, company, similarity score
5. Each job shall have a "View Job" button linking to original posting
6. Email shall be sent from configured sender address via Gmail SMTP (port 587, TLS)
7. Email shall include footer with unsubscribe information
8. Email shall have HTML format with plain text fallback

## 3.2 Non-Functional Requirements

This section specifies quality attributes, performance benchmarks, security requirements, and constraints that Cinebase must satisfy.

### NFR-1: Performance Requirements

**Response Time:**
- Login request shall complete within 2 seconds
- Dashboard page load shall complete within 3 seconds
- Document upload shall provide feedback within 5 seconds (excluding background embedding task)
- Job search and matching shall complete within 60 seconds (dependent on external APIs and job board scraping)
- Database queries shall execute within 1 second

**Throughput:**
- System shall support 100 concurrent users without degradation
- Backend API shall handle 50 requests per second
- Database shall support 100 queries per second

**Scalability:**
- System architecture shall support horizontal scaling of backend containers on Render
- Database shall accommodate 10,000 users and 50,000 documents without performance degradation
- Vector similarity search shall remain performant with 100,000+ embedding vectors

### NFR-2: Security Requirements

**Data Protection:**
- All client-server communication shall use HTTPS with TLS 1.2 or higher
- API keys for external services (Hugging Face, Groq) shall be stored as environment variables, never in code
- User session data in LocalStorage shall not contain sensitive information beyond user ID and email
- Database credentials shall be managed via platform environment variables (Supabase connection string)

**Access Control:**
- Users shall only access their own documents (enforced via user_id foreign key checks)
- Document deletion shall require ownership verification
- API endpoints shall validate user authentication before processing requests

**Limitations:**
- No password storage (email-only authentication means no password hashing required)
- No multi-factor authentication (MFA) in current version
- No email verification (users can authenticate with any email address)

### NFR-3: Reliability and Availability

**Uptime:**
- Backend API shall maintain 99% uptime (excluding Render free tier cold starts)
- Database (Supabase) shall maintain 99.9% uptime per provider SLA
- Frontend (Vercel) shall maintain 99.9% uptime per provider SLA

**Error Handling:**
- All API errors shall return appropriate HTTP status codes (404, 400, 500)
- Error messages shall be user-friendly and actionable
- Backend shall log all errors with timestamps and request context
- Failed embedding generation shall not prevent document upload completion

**Data Integrity:**
- Database transactions shall be ACID-compliant
- Foreign key constraints shall prevent orphaned records
- CASCADE delete shall ensure user deletion removes all associated documents

### NFR-4: Usability Requirements

**User Interface:**
- UI shall be responsive and functional on screen widths from 360px (mobile) to 2560px (desktop)
- All interactive elements shall have clear hover states and visual feedback
- Loading states shall be displayed for all asynchronous operations
- Error messages shall appear prominently and provide guidance for resolution

**Accessibility:**
- Form inputs shall have proper labels and ARIA attributes
- Color contrast shall meet WCAG 2.1 AA standards
- Keyboard navigation shall be supported for all interactive elements

**Learning Curve:**
- New users shall be able to upload their first resume and run job search within 5 minutes
- No user manual or training required for basic operations

### NFR-5: Compatibility Requirements

**Browser Compatibility:**
- Google Chrome 90+ (primary supported browser)
- Mozilla Firefox 88+
- Apple Safari 14+
- Microsoft Edge 90+
- No support for Internet Explorer

**Operating Systems:**
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu, Fedora, Debian)
- iOS 14+ (mobile Safari)
- Android 9+ (mobile Chrome)

**Screen Resolutions:**
- Minimum: 360px width (mobile devices)
- Optimal: 1024px width or higher (desktop/tablet)

### NFR-6: Maintainability Requirements

**Code Quality:**
- Backend code shall follow PEP 8 Python style guidelines
- Frontend code shall follow ESLint recommended rules
- Functions shall be modular and single-purpose
- Database schema changes shall be documented

**Documentation:**
- API endpoints shall be documented via FastAPI automatic Swagger UI
- Code comments shall explain complex algorithms (e.g., cosine similarity calculation)
- README files shall provide setup instructions for local development

**Version Control:**
- All code shall be versioned using Git
- Commits shall follow conventional commit message format
- Feature branches shall be merged via pull requests

### NFR-7: Portability Requirements

**Deployment Flexibility:**
- Backend shall be containerizable (Docker-compatible)
- Frontend shall be deployable on any static hosting platform
- Database migrations shall be platform-agnostic (PostgreSQL standard)

**Environment Parity:**
- Development, staging, and production environments shall use identical configurations
- Environment-specific settings shall be managed via `.env` files and platform environment variables

### NFR-8: Compliance and Legal Requirements

**Data Privacy:**
- System shall store only necessary user data (email, documents)
- No GDPR compliance mechanisms currently implemented (future enhancement)
- No explicit user consent collection for data processing

**Web Scraping:**
- Job scraping via JobSpy library uses publicly available data
- No authentication bypassing or rate limit circumvention
- Risk acknowledgment: Job boards may block scraping activity

### NFR-9: Dependency Management

**External Service Availability:**
- System shall gracefully handle Hugging Face API failures (log error, skip embedding generation)
- System shall provide fallback when Groq API fails (use "general" as job title)
- System shall handle individual job board failures without crashing entire search

**API Rate Limits:**
- System shall not exceed Hugging Face free tier rate limits
- System shall not exceed Groq free tier token limits
- System shall implement sequential embedding generation to avoid rate limit bursts

### NFR-10: Disaster Recovery

**Backup and Recovery:**
- Database backups shall be automated daily via Supabase
- Point-in-time recovery shall be available for database (7 days retention)
- Uploaded PDF files are ephemeral on Render (may be lost on container restart)
- Database is source of truth (PDF text extracted and stored in DB)

**Data Loss Prevention:**
- Database writes shall be committed immediately
- Background tasks shall not be retried (accept single attempt per operation)

---

**End of Section 3: Project Requirements**
