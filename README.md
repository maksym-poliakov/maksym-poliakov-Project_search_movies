
# Film Search Application

## Overview
This Python application provides a command-line interface for searching films in a MySQL database based on keywords, genres, and release years. It supports exact and partial word searches, genre and year filtering, and displays popular search queries. The application uses a modular design with separate components for database interaction, user interface, input validation, and SQL query management.

## Features
- **Search by Keyword**: Perform exact or partial word searches on film titles.
- **Search by Genre and Year**: Filter films by genre, release year, or both.
- **Popular Queries**: View the top 10 most frequent search queries by type.
- **Pagination**: Display search results in configurable chunks with offset and limit.
- **Input Validation**: Robust validation for user inputs to ensure correct data types and ranges.
- **Database Support**: Connects to MySQL databases for reading and writing search queries.
- **Indexing**: Includes SQL indexes to optimize search performance.

## Prerequisites
- **Python 3.8+**
- **MySQL Server**
- **Required Python packages**:
  - `mysql-connector-python`
  - `python-dotenv`

Install dependencies using:
```bash
pip install mysql-connector-python python-dotenv
```

## Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up environment variables**:
   Create a `.env` file in the project root with the following structure:
   ```plaintext
   host_read=<read_database_host>
   user_read=<read_database_user>
   password_read=<read_database_password>
   database_read=<read_database_name>
   host_write=<write_database_host>
   user_write=<write_database_user>
   password_write=<write_database_password>
   database_write=<write_database_name>
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Project Structure
- **`main.py`**: Entry point of the application, initializes the user interface.
- **`user_iinterface.py`**: Manages menu navigation and user interaction.
- **`db_connect.py`**: Handles database connections and query execution.
- **`databases_config.py`**: Stores database connection configurations.
- **`config_sql_requests.py`**: Contains SQL queries and indexes for search optimization.
- **`validation.py`**: Validates user input for correctness and range.
- **`menu.py`**: Defines the menu structure and user prompts.
- **`unknownexception.py`**: Custom exception for error handling.

## Usage
1. Run `main.py`.
2. Follow the menu prompts to select a search type:
   - Search by keyword (exact or partial match).
   - Search by genre and/or year.
   - View popular queries.
3. Enter data as prompted (e.g., words, years, genres).
4. View search results with pagination support.
5. To exit, press Enter in the main menu or select "N" when prompted to continue.

## Notes
- Ensure the MySQL server is configured and accessible.
- The database must include `film`, `film_category`, and `category` tables with appropriate fields.
- The `search_queries` table is automatically created to store query statistics.
- Apply the indexes defined in `config_sql_requests.py` for optimal search performance.

## License
This project is licensed under the MIT License (unless otherwise specified).

