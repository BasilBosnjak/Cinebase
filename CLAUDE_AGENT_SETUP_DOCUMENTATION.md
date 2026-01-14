# Claude Code Agent Configuration Documentation

**Agent Name:** Claude Code CLI Agent
**Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
**Platform:** Linux 6.8.0-90-generic
**Working Directory:** /home/basil/repos/Cinebase
**Last Updated:** 2026-01-13

---

## Executive Summary

This document details the custom configuration of a Claude Code CLI agent specialized for full-stack development with Python (FastAPI), React, and PostgreSQL. The agent is configured with specialized MCP servers, custom tools, and sub-agent architectures for autonomous task execution.

### Integration Summary Table

| Category | Component | Purpose | Status |
|----------|-----------|---------|--------|
| **MCP Server** | IDE Integration | VS Code diagnostics & Jupyter execution | Active |
| **Sub-Agent** | Explore Agent | Fast codebase exploration and search | Active |
| **Sub-Agent** | Plan Agent | Software architecture and implementation planning | Active |
| **Sub-Agent** | General-Purpose Agent | Complex multi-step autonomous tasks | Active |
| **Sub-Agent** | Bash Agent | Command execution specialist | Active |
| **External Integration** | JobSpy MCP Server (deprecated) | Job board scraping (Indeed, LinkedIn, Glassdoor) | Replaced with Python library |
| **External Service** | n8n Workflow Automation | Embedding generation and email automation | Self-hosted (localhost:5678) |
| **AI Service** | Hugging Face Inference API | Text embeddings (nomic-embed-text-v1.5, 768-dim) | Cloud-based |
| **AI Service** | Groq LLM API | Text generation (llama-3.1-8b-instant) | Cloud-based |

---

## 1. MCP Servers

### 1.1 IDE MCP Server
**Status:** Active
**Source:** Built-in Claude Code integration

**Available Tools:**
- `mcp__ide__getDiagnostics` - Retrieves language diagnostics from VS Code
  - **Parameters:** Optional URI to filter diagnostics by file
  - **Returns:** Error/warning messages, line numbers, severity levels
  - **Use Cases:** Code validation, identifying type errors, linting issues

- `mcp__ide__executeCode` - Executes Python code in Jupyter kernel
  - **Parameters:** Python code string
  - **Returns:** Execution results, outputs, errors
  - **Use Cases:** Interactive data analysis, testing code snippets, exploratory programming
  - **State Management:** Persistent kernel state across calls

**Integration Notes:**
- Automatically available in notebook contexts
- Kernel state persists until restart
- Supports IPython magic commands

---

## 2. Custom Skills

**Location:** No custom skills directory detected
**Status:** Using default Claude Code skill set

**Note:** Skills are invoked via the Skill tool when users reference slash commands (e.g., `/commit`, `/review-pr`). No project-specific custom skills are currently configured.

---

## 3. Available Tools Catalog

### 3.1 Core Development Tools

#### Task (Agent Orchestration)
**Category:** Agent Management
**Purpose:** Launch specialized sub-agents for complex tasks

**Available Sub-Agent Types:**

| Sub-Agent | Tools Available | Use Case |
|-----------|----------------|----------|
| **Bash** | Bash | Terminal operations, git commands |
| **general-purpose** | All tools | Multi-step research and complex tasks |
| **Explore** | All tools | Fast codebase exploration and keyword search |
| **Plan** | All tools | Implementation planning and architecture design |
| **statusline-setup** | Read, Edit | Configure Claude Code status line |
| **claude-code-guide** | Glob, Grep, Read, WebFetch, WebSearch | Documentation and help queries |

**Key Features:**
- Background execution with `run_in_background=true`
- Agent resumption via `resume` parameter
- Context preservation across invocations
- Parallel execution support

#### File Operations Suite

**Read Tool**
- Supports images (PNG, JPG), PDFs, Jupyter notebooks (.ipynb)
- Line-based offset and limit for large files
- Automatic line numbering (cat -n format)

**Write Tool**
- Creates new files with validation
- Requires prior Read for existing files
- Path validation (absolute paths only)

**Edit Tool**
- Exact string replacement with `old_string` / `new_string`
- `replace_all` parameter for bulk renaming
- Preserves exact indentation

**NotebookEdit Tool**
- Cell-level editing for Jupyter notebooks
- Supports insert/delete/replace modes
- Cell type specification (code/markdown)

### 3.2 Search and Navigation Tools

**Glob**
- Fast file pattern matching (any codebase size)
- Supports `**/*.js`, `src/**/*.ts` patterns
- Results sorted by modification time

**Grep**
- Built on ripgrep (rg) with full regex support
- Output modes: `content`, `files_with_matches`, `count`
- Context lines: `-A`, `-B`, `-C` parameters
- Multiline mode with `multiline: true`
- File filtering: `glob` (patterns) or `type` (js, py, rust, etc.)

### 3.3 Execution and Deployment Tools

**Bash**
- Persistent shell session with timeout control (default: 2min, max: 10min)
- Background execution via `run_in_background`
- Directory verification before file operations
- Git workflow automation (commit, PR creation via `gh` CLI)

**TaskOutput**
- Retrieves output from background tasks
- Blocking (`block=true`) and non-blocking modes
- Timeout configuration (default: 30s, max: 600s)

**KillShell**
- Terminates background bash shells by ID
- Used for cleaning up long-running processes

### 3.4 Web Integration Tools

**WebFetch**
- Fetches and processes web content with AI model
- HTML to markdown conversion
- 15-minute self-cleaning cache
- Automatic HTTPS upgrade
- Redirect detection and notification

**WebSearch**
- Live web search with result extraction
- Domain filtering (allow/block lists)
- Mandatory source citation requirement
- Geographic restriction: US-only

### 3.5 Planning and Interaction Tools

**EnterPlanMode**
- Transitions agent into planning mode
- Used for non-trivial implementation tasks
- Requires user approval to proceed

**ExitPlanMode**
- Signals plan completion and requests approval
- Only used after plan is written to file

**AskUserQuestion**
- Interactive question prompts (1-4 questions)
- Multiple choice with auto-generated "Other" option
- Multi-select capability
- Header labels (max 12 chars)

**TodoWrite**
- Task tracking with status management (pending, in_progress, completed)
- Dual-form task descriptions (imperative + present continuous)
- Real-time progress updates
- Used for complex multi-step tasks (3+ steps)

**Skill**
- Executes named skills (slash commands)
- Examples: `/commit`, `/review-pr`, `/pdf`
- Optional argument passing

---

## 4. Sub-Agent Configurations

### 4.1 Explore Agent
**Type:** Fast codebase exploration specialist
**Tools:** All tools (Read, Glob, Grep, etc.)
**Invocation:**
```
Task(subagent_type="Explore", prompt="Where are errors from the client handled?")
```

**Thoroughness Levels:**
- `quick` - Basic searches
- `medium` - Moderate exploration
- `very thorough` - Comprehensive multi-location analysis

**Use Cases:**
- Finding files by patterns (`src/components/**/*.tsx`)
- Searching code for keywords ("API endpoints")
- Answering questions about codebase architecture

**Performance:**
- Optimized for speed over exhaustive analysis
- Prefers parallel tool calls
- Context-aware search strategies

### 4.2 Plan Agent
**Type:** Software architect for implementation planning
**Tools:** All tools
**Invocation:**
```
Task(subagent_type="Plan", prompt="Design implementation for user authentication")
```

**Outputs:**
- Step-by-step implementation plans
- Critical file identification
- Architectural trade-off analysis
- Technology selection recommendations

**Workflow:**
1. Codebase exploration (Glob, Grep, Read)
2. Pattern analysis
3. Architecture design
4. User approval via ExitPlanMode

### 4.3 General-Purpose Agent
**Type:** Multi-step task executor
**Tools:** All tools
**Invocation:**
```
Task(subagent_type="general-purpose", prompt="Research and implement feature X")
```

**Capabilities:**
- Complex question research
- Code search across multiple files
- Multi-step autonomous execution
- Used when initial search confidence is low

**Best Practices:**
- Use when task requires >3 search iterations
- Delegate file/keyword searches here to reduce context usage
- Returns single consolidated message upon completion

### 4.4 Bash Agent
**Type:** Command execution specialist
**Tools:** Bash only
**Invocation:**
```
Task(subagent_type="Bash", prompt="Run git operations and deployment")
```

**Specialized For:**
- Git operations (commit, push, pull, branch management)
- Package management (npm, pip, apt)
- Build and deployment scripts
- Docker operations

**Safety Features:**
- Never updates git config
- Never runs destructive commands (force push, hard reset) without explicit request
- Never skips hooks (--no-verify) unless requested
- Validates HEAD commit ownership before amend

### 4.5 Claude Code Guide Agent
**Type:** Documentation and help specialist
**Tools:** Glob, Grep, Read, WebFetch, WebSearch
**Invocation:**
```
Task(subagent_type="claude-code-guide", prompt="How do I configure MCP servers?")
```

**Knowledge Domains:**
- Claude Code CLI features, hooks, slash commands
- MCP server configuration and integration
- Claude Agent SDK for custom agents
- Claude API (Anthropic API) usage and tool integration

**Resumability:**
- Can be resumed via `resume` parameter with agent ID
- Preserves full conversation context

---

## 5. Project-Specific Integrations

### 5.1 JobSpy Integration (Deprecated)
**Previous Configuration:** MCP Server at `http://localhost:9423`
**Current Status:** Replaced with `python-jobspy` library (v1.1.75)

**Migration Notes:**
- MCP server was self-hosted at `/home/basil/repos/jobspy-mcp-server`
- Required `ENABLE_SSE=1 node src/index.js` to start
- Now uses direct Python library integration in FastAPI backend

**Supported Job Boards:**
- Indeed
- LinkedIn
- Glassdoor
- Google Jobs
- ZipRecruiter
- Bayt
- Naukri

### 5.2 n8n Workflow Automation
**Configuration:** Self-hosted at `http://localhost:5678`
**Purpose:** Background task automation

**Workflows:**
1. **Document Embedding Generation** (Deprecated)
   - Triggered by PDF upload webhook
   - Replaced with FastAPI background tasks

2. **Weekly Job Digest Email**
   - Cron trigger: Every Monday 9:00 AM
   - Calls `/jobs/weekly-digest` endpoint
   - Formats HTML email with top 5 job matches per user
   - Sends via SMTP (Gmail)

**Workflow File:** `/home/basil/repos/Cinebase/n8n-workflows/weekly-job-digest.json`

### 5.3 Cloud AI Services

**Hugging Face Inference API**
- **Endpoint:** `https://router.huggingface.co/pipeline/feature-extraction/nomic-ai/nomic-embed-text-v1.5`
- **Model:** nomic-embed-text-v1.5
- **Output:** 768-dimensional vectors
- **Use Case:** Document and job description embeddings
- **Environment Variable:** `HUGGINGFACE_API_KEY`

**Groq LLM API**
- **Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
- **Model:** llama-3.1-8b-instant
- **Use Cases:** Job title extraction from CVs, text generation
- **Parameters:** Configurable max_tokens (default: 100), temperature (default: 0.1)
- **Environment Variable:** `GROQ_API_KEY`

---

## 6. Deployment Architecture

### 6.1 Production Environment

**Frontend:**
- Platform: Vercel
- URL: `https://cinebase-sepia.vercel.app`
- Build: Vite + React
- Environment Variables:
  - `VITE_API_URL=https://cinebase-backend.onrender.com`

**Backend:**
- Platform: Render
- URL: `https://cinebase-backend.onrender.com`
- Runtime: Python 3.11.7 + Gunicorn
- Environment Variables:
  - `DATABASE_URL` (Supabase connection pooler)
  - `CORS_ORIGINS=https://cinebase-sepia.vercel.app,http://localhost:5173`
  - `HUGGINGFACE_API_KEY`
  - `GROQ_API_KEY`

**Database:**
- Platform: Supabase (Managed PostgreSQL)
- Extensions: pgvector
- Connection: IPv4 pooler (port 6543) for Render compatibility

### 6.2 Development Environment

**Local Services:**
- Backend: `http://localhost:8000` (uvicorn)
- Frontend: `http://localhost:5173` (Vite dev server)
- n8n: `http://localhost:5678`
- PostgreSQL: `localhost:5432`

**Required Local Dependencies:**
- PostgreSQL with pgvector extension
- Python 3.11+ with virtual environment
- Node.js for frontend
- n8n (npm global install or Docker)

---

## 7. Agent Behavior Configuration

### 7.1 Communication Style
- **Emojis:** Disabled by default (only when explicitly requested)
- **Output Format:** GitHub-flavored Markdown (CommonMark)
- **Conciseness:** Short, technical responses
- **Tool Calls:** Never use bash/echo for user communication
- **Professional Tone:** Objective, fact-focused, no superlatives

### 7.2 Task Management Patterns

**TodoWrite Usage Triggers:**
- Complex multi-step tasks (3+ steps)
- Non-trivial complex tasks
- User explicitly requests todo list
- Multiple tasks provided (numbered/comma-separated)
- After receiving new instructions

**TodoWrite Exclusions:**
- Single straightforward tasks
- Trivial tasks (<3 steps)
- Purely conversational requests

**Status Transition Rules:**
- Exactly ONE task must be `in_progress` at any time
- Complete tasks IMMEDIATELY after finishing (no batching)
- Remove irrelevant tasks entirely (don't leave as pending)

### 7.3 File Operation Preferences

**Priority Order:**
1. Specialized tools (Read, Edit, Write, Glob, Grep)
2. Bash only for actual terminal operations
3. Never use bash for: find, grep, cat, echo, sed, awk

**Edit vs. Write:**
- ALWAYS prefer editing existing files
- NEVER write new files unless absolutely necessary
- NEVER proactively create documentation files (*.md, README)

### 7.4 Git Workflow Rules

**Commit Creation:**
- Only when explicitly requested by user
- Must read `git status`, `git diff`, `git log` in parallel first
- Analyze ALL staged changes before drafting message
- Include Co-Author tag: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
- Use HEREDOC for commit messages

**Safety Constraints:**
- Never amend unless: (1) user requested OR hook auto-modified files, (2) commit created in current conversation, (3) not yet pushed
- Never force push to main/master without warning
- Never skip hooks (--no-verify) unless requested

**Pull Request Creation:**
- Check `git status`, `git diff`, `git log`, branch tracking in parallel
- Analyze ALL commits from base branch divergence
- Create PR with summary bullets + test plan checklist
- Use `gh pr create` with HEREDOC body

---

## 8. Context and Performance Optimizations

### 8.1 Summarization
- Unlimited context via automatic summarization
- Conversation compacted when token limit approaches
- Full transcript available at: `~/.claude/projects/-home-basil-repos-Cinebase/<session-id>.jsonl`

### 8.2 Parallel Execution Patterns

**When to Parallelize:**
- Independent file reads (Read multiple files)
- Multiple glob/grep searches
- Parallel bash commands when independent
- Multiple sub-agent launches when user requests "in parallel"

**Sequential Execution Required:**
- Dependent tool calls (output of one feeds into next)
- File operations before git commits
- Database migrations before deployments

### 8.3 Agent vs. Direct Tool Usage

**Use Task (Sub-Agent) When:**
- Open-ended codebase exploration
- Need multiple rounds of search/grep/glob
- Complex research across many files
- Initial search confidence is low

**Use Direct Tools When:**
- Specific file path known
- Specific class/function search (use Glob)
- Search within 2-3 known files (use Read)
- Needle-in-haystack queries

---

## 9. Security and Best Practices

### 9.1 Security Protocols
- **Authorized Contexts:** Security testing, CTF challenges, defensive security, educational contexts
- **Prohibited:** Destructive techniques, DoS attacks, mass targeting, supply chain compromise
- **Dual-Use Tools:** Require clear authorization (pentesting, CTF, security research)

### 9.2 Code Quality Standards
- Avoid over-engineering (minimum complexity for current task)
- No premature abstractions
- No backwards-compatibility hacks for unused code
- Only validate at system boundaries (user input, external APIs)
- No error handling for impossible scenarios
- Delete unused code completely (no `_vars`, `// removed` comments)

### 9.3 Environment Variable Management
- Never commit `.env` files (use `.gitignore`)
- Set secrets via platform environment variables (Render, Vercel)
- Use `pydantic-settings` for configuration management
- Prefix frontend vars with `VITE_` for Vite accessibility

---

## 10. Troubleshooting and Diagnostics

### 10.1 Common Debug Workflows

**Backend Deployment Issues:**
1. Check Render logs for import errors
2. Verify environment variables set correctly
3. Test endpoints via `/docs` (Swagger UI)
4. Check database connectivity via `/health`

**CORS Errors:**
1. Verify `CORS_ORIGINS` includes frontend URL (no spaces)
2. Ensure backend redeployed after env var change
3. Hard refresh frontend (Ctrl+Shift+R)

**Background Task Failures:**
1. Check Render logs for `[Embedding]` or task-specific tags
2. Verify API keys present in environment
3. Test API endpoints directly (curl/Postman)
4. Check for async/await issues in background functions

### 10.2 Log Locations

**Local Development:**
- Backend: Terminal running `uvicorn app.main:app --reload`
- Frontend: Browser console (F12)
- n8n: Web UI at `http://localhost:5678` → Executions

**Production:**
- Backend: Render Dashboard → Logs tab
- Frontend: Vercel Dashboard → Deployments → Function Logs
- Database: Supabase Dashboard → SQL Editor

---

## Appendix A: Key File Locations

**Configuration Files:**
- Agent settings: `~/.claude/settings.json`
- Project config: `~/.claude/projects/-home-basil-repos-Cinebase/`
- Session environments: `~/.claude/session-env/<session-id>/`

**Project Structure:**
- Backend: `/home/basil/repos/Cinebase/backend/`
- Frontend: `/home/basil/repos/Cinebase/frontend/`
- n8n workflows: `/home/basil/repos/Cinebase/n8n-workflows/`
- Project docs: `/home/basil/repos/Cinebase/CLAUDE.md`

**External Services:**
- JobSpy MCP Server (deprecated): `/home/basil/repos/jobspy-mcp-server/`

---

## Appendix B: Dependencies and Versions

**Backend Python (3.11.7):**
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- pydantic[email]==2.5.0
- pgvector==0.2.4
- python-jobspy==1.1.75
- httpx==0.25.2 (for cloud API calls)

**Frontend:**
- React + Vite
- Tailwind CSS
- React Router DOM

**External APIs:**
- Hugging Face Inference API (embeddings)
- Groq LLM API (text generation)

---

**Document Version:** 1.0
**Effective Date:** 2026-01-13
**Maintained By:** Claude Code Agent (automated documentation)
