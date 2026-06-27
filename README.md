# Election Voting System (Streamlit)

A web-based election voting application built with [Streamlit](https://streamlit.io/) and PostgreSQL. It provides separate interfaces for voters to cast ballots and for administrators to manage nominees and view results.

## Features

### Voter portal
- Verify identity using NIC number against registered voter records
- View the nominee list
- Cast a single vote (duplicate votes are blocked)
- Logout after voting

### Admin dashboard
- Admin login with email and password
- Add new nominees
- View all nominees
- View top 3 nominees by vote count
- View vote count for an individual nominee

## Project structure

```
election_voting_system_streamlit/
├── app.py                     # Main Streamlit app (voter + admin)
├── connection.py              # Database connection (SQLAlchemy + PostgreSQL)
├── admin.py                   # Admin authentication and nominee management
├── admin_count_functions.py   # Vote counting and leaderboard queries
├── voter.py                   # Voter verification and vote submission
├── requirements.txt           # Python dependencies
├── .streamlit/secrets.toml    # Local secrets (not committed)
└── README.md
```

## Prerequisites

- Python 3.10+
- A PostgreSQL database (e.g. [Supabase](https://supabase.com/))
- pip

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd election_voting_system_streamlit
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.streamlit/secrets.toml` locally with your database URL:

```toml
DATABASE_URL = "postgresql://user:password@host:port/database"
```

Or set a `DATABASE_URL` environment variable:

```bash
# Windows PowerShell
$env:DATABASE_URL = "postgresql://user:password@host:port/database"

# macOS / Linux
export DATABASE_URL="postgresql://user:password@host:port/database"
```

> **Note:** Do not commit database credentials. Use environment variables or Streamlit secrets for production.

## Database setup

Run the following SQL in your PostgreSQL database (e.g. Supabase SQL Editor) before using the app:

```sql
CREATE TABLE admin (
    admin_id   SERIAL PRIMARY KEY,
    email      VARCHAR(255) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL
);

CREATE TABLE nominee (
    nominee_id    SERIAL PRIMARY KEY,
    name          VARCHAR(255) NOT NULL UNIQUE,
    nominee_party VARCHAR(255) NOT NULL
);

CREATE TABLE voter_details (
    nic_number          VARCHAR(20)  NOT NULL PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    electoral_district  VARCHAR(255) NOT NULL,
    electorates         VARCHAR(255) NOT NULL
);

CREATE TABLE voter (
    vote_id             SERIAL PRIMARY KEY,
    nic_no              VARCHAR(20)  NOT NULL UNIQUE,
    voter_name          VARCHAR(255) NOT NULL,
    electoral_district  VARCHAR(255) NOT NULL,
    electorates         VARCHAR(255) NOT NULL,
    nominee_id          INTEGER NOT NULL,
    voted_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_voter_nominee
        FOREIGN KEY (nominee_id) REFERENCES nominee(nominee_id)
);

-- Sample data
INSERT INTO admin (email, password) VALUES
('admin@election.lk', 'admin123');

INSERT INTO nominee (name, nominee_party) VALUES
('John Doe', 'Party A'),
('Jane Smith', 'Party B'),
('Alice Brown', 'Party C');

INSERT INTO voter_details (nic_number, name, electoral_district, electorates) VALUES
('123456789V', 'John Perera', 'Colombo', 'Colombo North'),
('987654321V', 'Kamal Silva', 'Gampaha', 'Gampaha East'),
('456789123V', 'Nimal Fernando', 'Kandy', 'Kandy Central');
```

### Tables

| Table           | Purpose                                              |
|-----------------|------------------------------------------------------|
| `admin`         | Admin login credentials                              |
| `nominee`       | Election candidates                                  |
| `voter_details` | Pre-registered voters (verified before voting)       |
| `voter`         | Cast votes (one row per voter; `nic_no` is unique)   |

## Running the app

Test the database connection:

```bash
python connection.py
```

Run the application:

```bash
streamlit run app.py
```

Use the sidebar to switch between **Voter Portal** and **Admin Dashboard**.

Streamlit will open the app in your browser (default: `http://localhost:8501`).

## Deploying to Streamlit Cloud

1. Push the repository to GitHub (do not commit `.streamlit/secrets.toml`).
2. Create a new app at [share.streamlit.io](https://share.streamlit.io).
3. Set **Main file path** to `app.py`.
4. In **App settings → Secrets**, add:

```toml
DATABASE_URL = "postgresql://user:password@host:port/database"
```

5. Use your Supabase **connection pooler** URL (port `6543`) for cloud deployments.

## Usage

### Voter flow
1. Enter your NIC number.
2. Enter your full name, electoral district, and electorate (must match `voter_details` exactly).
3. Click **Verify**.
4. Select a nominee and click **Submit Vote**.

### Admin flow
1. Log in with admin email and password.
2. Use the sidebar menu to add nominees, view lists, or check vote counts.

## Default credentials (sample data)

| Role  | Email               | Password  |
|-------|---------------------|-----------|
| Admin | admin@election.lk   | admin123  |

Change these credentials after first login in a production environment.

## Tech stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** PostgreSQL (Supabase)
- **ORM / DB driver:** SQLAlchemy, psycopg2-binary
- **Data handling:** pandas

## License

This project is provided as-is for educational and demonstration purposes.
