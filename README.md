# PortIQ

A role-based portfolio and trading intelligence platform built with Streamlit, Flask, and MySQL. Users log in as one of four personas and get a tailored dashboard with persona-specific features and data.

## Personas

| Persona | Role | Key Features |
|---|---|---|
| Andrew Rock | Quant Trader | Portfolio performance, strategy benchmarking, risk analysis, trade logs (CRUD) |
| John Data | Data Analyst | NGO directory management, ML regression/classification predictions, API testing |
| Katrina Williams | CIO | Identity & access management (IAM), audit logs, role/permission management |
| Jane Doe | Beginner User | Educational content about markets and trading |

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** Flask REST API
- **Database:** MySQL 9
- **Infrastructure:** Docker & Docker Compose
- **Runtime:** Python 3.11

## Project Structure

```
PortIQ/
├── app/                    # Streamlit frontend
│   └── src/
│       ├── Home.py         # Login / persona selection page
│       ├── modules/nav.py  # Role-based sidebar navigation
│       └── pages/          # All role-specific pages
├── api/                    # Flask REST API
│   ├── backend_app.py      # API entry point
│   └── backend/            # Route blueprints (users, roles, portiq, actions)
├── database-files/         # SQL init scripts (run alphabetically on first start)
├── datasets/               # ML datasets
├── ml-src/                 # ML model development (Jupyter notebooks, scripts)
├── docker-compose.yaml     # Team/production containers
└── sandbox.yaml            # Personal testing containers
```

## Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- VSCode (recommended)

## Setup

### 1. Create Python environment

```bash
conda create -n db-proj python=3.11
conda activate db-proj
```

### 2. Install dependencies locally (for IDE support)

```bash
cd api
pip install -r requirements.txt
cd ../app/src
pip install -r requirements.txt
cd ../..
```

### 3. Configure environment variables

```bash
cp .env.template api/.env
```

Open `api/.env` and fill in the placeholders:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session encryption key (any random string) |
| `DB_USER` | MySQL username (e.g. `root`) |
| `DB_HOST` | MySQL hostname — use `db` inside Docker |
| `DB_PORT` | MySQL port (e.g. `3306`) |
| `DB_NAME` | Database name (e.g. `PortIQ`) |
| `MYSQL_ROOT_PASSWORD` | MySQL root password |
| `ENCRYPTION_KEY` | AES key for encrypting sensitive user fields |

### 4. Start the containers

**Team / shared development:**
```bash
docker compose up -d
```

**Personal sandbox (isolated ports, won't conflict with teammates):**
```bash
docker compose -f sandbox.yaml up -d
```

### 5. Access the app

| Service | Team URL | Sandbox URL |
|---|---|---|
| Streamlit frontend | http://localhost:8501 | http://localhost:8502 |
| Flask API | http://localhost:4000 | http://localhost:4001 |
| MySQL | localhost:3200 | localhost:3201 |

## Development Tips

- **Hot reload:** Both Streamlit and Flask reload automatically when files are saved. In the browser, click **Always Rerun** to keep Streamlit in sync.
- **MySQL init:** SQL files in `database-files/` run once, in alphabetical order, when the container is first created.
- **Reinitialize the database** (after editing SQL files):
  ```bash
  docker compose down db -v && docker compose up db -d
  ```
- **View MySQL logs** for SQL errors: open Docker Desktop → MySQL container → Logs tab → search for `Error`.

## Role-Based Access Control (RBAC)

Persona selection on the home page sets `st.session_state['role']` and `st.session_state['authenticated']`. The `SideBarLinks()` function in `modules/nav.py` reads these values and renders the appropriate sidebar links for that role. Page numbering reflects the role:

| Prefix | Persona |
|---|---|
| `0x` | Quant Trader |
| `1x` | Data Analyst |
| `2x` | CIO |
| `3x` | Shared / About |
| `4x` | Beginner User |

> Authentication is mocked — there are no real passwords. This is a course project demonstrating RBAC patterns, not a production auth system.

## Docker Commands Reference

```bash
# Start all containers
docker compose up -d

# Stop and remove containers (keeps volumes)
docker compose down

# Stop containers without removing them
docker compose stop

# Restart all containers
docker compose restart

# Start only a specific service
docker compose up db -d       # database only
docker compose up app -d      # frontend only
docker compose up api -d      # backend only

# Reinitialize the database (destructive — deletes all data)
docker compose down db -v && docker compose up db -d
```
