# PortIQ

A role-based portfolio and trading intelligence platform built with Streamlit, Flask, and MySQL. Users log in as one of four personas and get a tailored dashboard with persona-specific features and data.

## Team

- Yash Maheshwari
- Sean Snaider
- Ernesto
- Shlok

## Personas

| Persona | Role | Key Features |
|---|---|---|
| Andrew Rock | Quant Trader | Portfolio performance, strategy benchmarking, risk analysis, trade logs (CRUD) |
| John Data | Data Analyst | Dashboard layouts, data cleaning pipelines, dataset management, visualizations |
| Katrina Williams | CIO | Identity & access management (IAM), audit logs, role and permission management |
| Jane Doe | Beginner Investor | Portfolio positions, portfolio dashboard, AI portfolio assistant (Gemini) |

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** Flask REST API
- **Database:** MySQL 9
- **Infrastructure:** Docker & Docker Compose

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
│   └── backend/            # Route blueprints organized by persona/resource
├── database-files/         # SQL schema + mock data (run alphabetically on first start)
└── docker-compose.yaml     # Docker service definitions
```

## Setup

### 1. Configure environment variables

```bash
cp api/.env.template api/.env
```

Open `api/.env` and fill in:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session encryption key (any random string) |
| `DB_USER` | MySQL username (`root`) |
| `DB_HOST` | MySQL hostname — use `db` inside Docker |
| `DB_PORT` | MySQL port (`3306`) |
| `DB_NAME` | Database name (`PortIQ`) |
| `MYSQL_ROOT_PASSWORD` | MySQL root password |
| `GEMINI_API_KEY` | Google Gemini API key (free tier) — required for the AI Portfolio Assistant |

### 2. Start the containers

```bash
docker compose up -d
```

### 3. Access the app

| Service | URL |
|---|---|
| Streamlit frontend | http://localhost:8501 |
| Flask API | http://localhost:4000 |
| MySQL | localhost:3200 |

## Docker Commands Reference

```bash
# Start all containers (first run builds images)
docker compose up -d

# Rebuild images after code changes
docker compose up --build -d

# Stop and remove containers
docker compose down

# Reinitialize the database (wipes all data and reruns SQL files)
docker compose down db
docker volume rm project-app-team-repo_mysql_data
docker compose up db -d

# View logs
docker compose logs api
docker compose logs app
docker compose logs db
```

## Development Notes

- **Hot reload:** Streamlit and Flask both reload automatically on file save. Click **Always Rerun** in the Streamlit browser tab.
- **Database init:** SQL files in `database-files/` run once in alphabetical order when the container is first created. Restarting the container does NOT re-run them — you must wipe the volume.
- **Authentication:** Persona selection is mocked. There are no real passwords. This is a course project demonstrating role-based access patterns.
