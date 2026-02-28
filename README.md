# MediTab — British Parliamentary Debate Tab System

MediTab is a full-featured tab system for British Parliamentary (BP) debate and public speaking tournaments, inspired by Tabbycat. It supports the complete BP debate format with power pairing, adjudicator allocation, clash detection, and a public tab.

## Features

- 🏆 **Tournament Management** — Create and manage multiple tournaments with custom settings
- 🗳️ **BP Power Pairing** — Automatic draw generation using power pairing with position balancing (OG / OO / CG / CO)
- ⚖️ **Judging System** — Adjudicator allocation with institutional and personal clash detection, panel scoring, and feedback
- 📊 **Public Tab** — Live standings viewable by contestants without login
- 👥 **Team & Speaker Dashboards** — Personalised views for each registered team and speaker
- 🔐 **Role-Based Access** — Admin, Tab Director, Adjudicator, and Participant roles
- 🐳 **Docker Deployment** — Production-ready Docker + PostgreSQL + Nginx setup

## Quick Start (Development)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the tournament listing, and `http://127.0.0.1:8000/admin/` for the Django admin.

## Docker Deployment (Production)

```bash
cp .env.example .env          # edit SECRET_KEY and database settings
docker-compose up --build -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

The app will be served on port 80 via Nginx.

## Project Structure

```
meditab/
├── apps/
│   ├── accounts/        # User authentication & roles
│   ├── tournaments/     # Tournament pages & admin dashboard
│   ├── participants/    # Teams, speakers, institutions
│   ├── adjudication/    # Judges, conflicts, feedback
│   ├── draws/           # Rounds, BP pairing algorithm
│   └── results/         # Ballots, scores, standings
├── templates/           # Bootstrap 5 HTML templates
├── static/              # CSS & JS assets
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

## BP Debate Rules Implemented

- 4 teams per debate: Opening Government (OG), Opening Opposition (OO), Closing Government (CG), Closing Opposition (CO)
- Teams ranked 1st–4th per debate; points: 1st = 3 pts, 2nd = 2 pts, 3rd = 1 pt, 4th = 0 pts
- Speaker scores on a 50–100 scale
- Power pairing from Round 2 onwards; position balancing across rounds
- Break rounds (Quarter-finals, Semi-finals, Grand Final) supported