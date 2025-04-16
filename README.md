## Project Structure
``` bash
fund-management-api/
├── .env.dev                    # Development environment variables
├── requirements.txt            # Python dependencies
├── config.py                   # Application configuration
├── run.py                      # Application entry point
│
├── app/                        # Application package
│   ├── dao.py                  # Data Access Object
│   ├── dto.py                  # Data Transfer Objects
│   ├── model.py                # Database models
│   ├── routes.py               # API routes
│
├── db/                         # Database related files
│   ├── task4_ddl.sql            # Database schema definitions
│   └── scripts/                # Database migration scripts
│       └── output/             # Migration output directory
│
└── tests/                      # Test files
```

### Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate - linux //.\.venv\Scripts\Activate.ps1 - windows
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup
1. Initialize the database:
    ```bash
    flask db init
    ```
2. Migrate the database:
    ```bash
    flask db migrate -m "initial migration"
    ```
3. Apply the migrations:
    ```bash
    flask db upgrade
    ```

### Running the Application
1. Development server:
    ```bash
    flask run
    ```
2. Access the API documentation:
    ```bash
    http://localhost:5000/api/docs
    ```

### Running Tests
1. Execute the test suite:
    ```bash
    pytest
    ```

### Database Migration
The project supports migrating data from SQLite to PostgreSQL. The migration process is handled by two scripts:
1. Export data from SQLite:
    ```bash
    sqlite3 instance/funds.db < db/scripts/export_from_sqlite.sql
    ```
    This command exports the funds table data to CSV format.

2. Import data to PostgreSQL:
    ```bash
    psql -d <db-name> -f db/scripts/import_to_postgres.sql
    ```
    This command imports the data into PostgreSQL using batch processing for better performance.

## 📘 API Documentation

## Sample API Requests and Responses
- For detailed API documentation, please refer to the API documentation at `http://localhost:5000/api/docs`

### 🚀 Create a new fund

**Request**
```bash
curl --location 'http://127.0.0.1:5000/funds' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Growth Fund",
    "manager_name": "Jane Smith",
    "description": "A diversified portfolio of global equities focusing on long-term capital appreciation.",
    "nav": 123123123.12,
    "performance": 12.34,
    "creation_date": "2024-01-01"
}'
```

**Response**
```json
{
    "fund_id": "a8b19b94-b0e4-4e2d-a62c-5df3b40a8385",
    "name": "Growth Fund",
    "manager_name": "Jane Smith",
    "description": "A diversified portfolio of global equities focusing on long-term capital appreciation.",
    "nav": "123123123.12",
    "performance": "12.34",
    "creation_date": "2024-01-01"
}
```

---

### 📄 Get all funds (with optional filters and pagination)

**Request**
```bash
curl --location 'http://127.0.0.1:5000/funds/list' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Growth",
    "manager_name": "Jane",
    "page": 1,
    "per_page": 5
}'
```

**Response**
```json
[
    {
        "fund_id": "a8b19b94-b0e4-4e2d-a62c-5df3b40a8385",
        "name": "Growth Fund",
        "manager_name": "Jane Smith",
        "description": "A diversified portfolio of global equities focusing on long-term capital appreciation.",
        "nav": "123123123.12",
        "performance": "12.34",
        "creation_date": "2024-01-01"
    }
]
```

---

### 🔍 Get fund by ID

**Request**
```bash
curl --location 'http://127.0.0.1:5000/funds/a8b19b94-b0e4-4e2d-a62c-5df3b40a8385'
```

**Response**
```json
{
    "fund_id": "a8b19b94-b0e4-4e2d-a62c-5df3b40a8385",
    "name": "Growth Fund",
    "manager_name": "Jane Smith",
    "description": "A diversified portfolio of global equities focusing on long-term capital appreciation.",
    "nav": "123123123.12",
    "performance": "12.34",
    "creation_date": "2024-01-01"
}
```

---

### ✏️ Update fund performance

**Request**
```bash
curl --location --request PUT 'http://127.0.0.1:5000/funds/a8b19b94-b0e4-4e2d-a62c-5df3b40a8385' \
--header 'Content-Type: application/json' \
--data '{
    "performance": -3.21
}'
```

**Response**
```json
{
    "fund_id": "a8b19b94-b0e4-4e2d-a62c-5df3b40a8385",
    "name": "Growth Fund",
    "manager_name": "Jane Smith",
    "description": "A diversified portfolio of global equities focusing on long-term capital appreciation.",
    "nav": "123123123.12",
    "performance": "-3.21",
    "creation_date": "2024-01-01"
}
```

---

### 🗑️ Delete fund

**Request**
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/funds/a8b19b94-b0e4-4e2d-a62c-5df3b40a8385'
```

**Response**
```json
{
    "message": "Fund deleted successfully"
}
```

**task4**
can refer db\task4_ddl.sql
