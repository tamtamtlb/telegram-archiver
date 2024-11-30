# Telegram Exporter

![Build Status](https://github.com/VladimirVereshchagin/telegram_exporter/workflows/Python%20CI/CD/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![Docker Image Size](https://img.shields.io/docker/image-size/vladimirvereschagin/telegram_exporter/latest)
![GitHub Release](https://img.shields.io/github/v/release/VladimirVereshchagin/telegram_exporter)

[Docker Hub repository for Telegram Exporter](https://hub.docker.com/r/vladimirvereschagin/telegram_exporter)  
[GitHub Packages for Telegram Exporter](https://github.com/VladimirVereshchagin/telegram_exporter/packages)

## Project Description

**Telegram Exporter** is a Python application designed to export and store messages from Telegram chats, groups, or channels into a SQLite database. The application supports formatting messages into HTML and automatically generates CSV and JSON files for easy data analysis and integration with other tools.

The application is particularly useful for:

- Archiving messages from personal or public Telegram groups.
- Analyzing chat data with external tools like Excel, Python scripts, or web services.
- Exporting messages for research, reporting, or integration into third-party systems.

## Key Features

- **Comprehensive Data Export**:
  - Exports messages along with metadata like date, URLs, and chat IDs.
  - Supports rich text formatting with styles like bold, italic, and underline.
- **Automatic File Generation**:
  - Automatically generates `html.csv` and `html.json` after every export to ensure your data is always up-to-date.
- **SQLite Database Storage**:
  - Efficiently stores messages with options for filtering and querying.
- **Dockerized Deployment**:
  - Deployable using a pre-built Docker image for easy scalability and cross-platform support.
- **CI/CD Integration**:
  - Automatically builds and pushes Docker images to Docker Hub upon successful tests.
- **Cross-version Compatibility**:
  - Supports Python 3.10, 3.11, and 3.12.

---

## Installation

### Prerequisites

- **Python** version **3.10** to **3.12** (Python 3.13 is not supported due to deprecated modules like `imghdr`).
- **Git**
- **Docker** (optional for containerized deployment)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/VladimirVereshchagin/telegram_exporter.git
   cd telegram_exporter
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   - Rename `.env.example` to `.env` and fill in your credentials:

     ```env
     API_ID=your_api_id
     API_HASH=your_api_hash
     PHONE=your_phone_number_with_country_code
     ```

---

## Usage

You can export messages from any chat, group, or channel you have access to.

### Export from "Saved Messages" (default)

Run the application without any arguments to export messages from your "Saved Messages":

```bash
python telegram_exporter/main.py
```

### Export from a specific chat, group, or channel

Use the `--chat` argument with the username, ID, or link to the chat:

```bash
python telegram_exporter/main.py --chat username_or_link
```

#### Examples

- By username:

  ```bash
  python telegram_exporter/main.py --chat example_user
  ```

- By channel link:

  ```bash
  python telegram_exporter/main.py --chat https://t.me/example_channel
  ```

- By chat ID:

  ```bash
  python telegram_exporter/main.py --chat -1001234567890
  ```

> **Note:** Ensure you have access to the specified chat, group, or channel.

---

## Quick Start via Docker Hub

For quick deployment, use the pre-built Docker image available on Docker Hub.

### Run the Container

  ```bash
  docker run -d \
  --name telegram_exporter \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  vladimirvereschagin/telegram_exporter:latest
  ```

### Explanation

- --env-file .env: Passes the .env file with API credentials to the container.
- -v $(pwd)/data:/app/data: Mounts the local data directory to persist the SQLite database and generated files outside the container.

### Access the Files

After running the application, the following files will be updated in the data directory:

- db.sqlite3 — SQLite database containing exported messages.
- html.csv — CSV file with messages and URLs.
- html.json — JSON file with messages and URLs.

---

## CI/CD

GitHub Actions is configured to automatically test, build, and push the application to Docker Hub. The workflow includes:

- Linting with flake8.
- Running unit tests.
- Building and pushing Docker images.

---

### URL Extraction

The application automatically extracts URLs from messages and saves them in the `urls` column in the database. This includes:

- Direct links in the message text.
- Links contained in message entities (e.g., formatted links where display text differs from the URL).

---

## Running Tests Locally

Run the following command to execute all tests:

```bash
python -m unittest discover tests
```

For linting:

```bash
flake8 telegram_exporter tests
```

---

## Feedback

If you have any questions or suggestions, please create an [issue](https://github.com/VladimirVereshchagin/telegram_exporter/issues) or [pull request](https://github.com/VladimirVereshchagin/telegram_exporter/pulls) in the project repository.

---

## Contributing

If you'd like to contribute, please follow the [Contribution Guide](CONTRIBUTING.md).

---

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.
