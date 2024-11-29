# Telegram Exporter

A Python application to export messages from Telegram and save them to a SQLite database with HTML formatting and URL extraction.

## Description

This application uses the [Telethon](https://github.com/LonamiWebs/Telethon) library to interact with the Telegram API. It allows you to:

- **Export messages** from "Saved Messages" or any other chat, group, or channel.
- **Format messages in HTML** while preserving styles.
- **Extract URLs** from messages, including those contained in message entities (e.g., formatted links).
- **Store messages and URLs** in a SQLite database for further use.
- **Automatically generate `html.csv` and `html.json` files** containing the exported messages and URLs for easy analysis or external use.

---

## Installation

### Prerequisites

- **Python** version **3.7** to **3.12** (Python 3.13 is not supported due to deprecated modules like `imghdr`).
- **Git**

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

### File Generation

During the export process, the application automatically generates two files:

1. **`html.csv`**:
   - Contains the exported messages and their URLs in a CSV format.
   - Useful for analysis in spreadsheet software or data processing scripts.

2. **`html.json`**:
   - Contains the exported messages and their URLs in a JSON format.
   - Ideal for integration with other systems or further programmatic processing.

These files are updated every time the application runs and reflect the latest data.

---

### URL Extraction

The application automatically extracts URLs from messages and saves them in the `urls` column in the database. This includes:

- Direct links in the message text.
- Links contained in message entities (e.g., formatted links where display text differs from the URL).

---

## Testing

Run the tests:

```bash
python -m unittest discover tests
```

Ensure you are using Python versions from 3.7 to 3.12.

---

## Docker Usage

You can also run the application using Docker:

1. **Build the Docker image**:

   ```bash
   docker build -t telegram_exporter .
   ```

2. **Run the Docker container**:

   ```bash
   docker run -it --env-file .env telegram_exporter --chat username_or_link
   ```

Ensure your `.env` file is correctly configured.

---

## Contributing

If you'd like to contribute, please follow the [Contribution Guide](CONTRIBUTING.md).

---

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.
