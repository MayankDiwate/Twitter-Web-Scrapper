# 🐦 Twitter Web Scraper Tool

This is a Python Flask-based web scraper tool designed to extract data from Twitter using Selenium. It uses proxy support and environment variables for secure and configurable scraping.

## ✨ Features

- **🕵️‍♂️ Scraping**: Fetches Twitter data using Selenium.
- **🌐 Proxy Support**: Manages and validates proxies for secure web scraping.
- **💻 Web Interface**: Provides a simple web-based interface to interact with the scraper.
- **🔑 Environment Variables**: Configuration is managed via a `.env` file for flexibility and security.
- **💾 Database Support**: Stores scraped Twitter trends in MongoDB.

---

## 📂 Project Structure

```
proxies/
    check_proxies.py        # Validates proxies from a list
    proxy_list.txt          # Contains a list of proxies
    valid_proxy_list.txt    # Stores validated proxies

scrapper/
    selenium_scrapper.py    # Main scraper logic using Selenium

templates/
    index.html              # HTML template for the Flask web app

venv/                       # Virtual environment folder
.env                        # Environment variables file
.gitignore                  # Files and folders to ignore in version control
app.py                      # Flask application entry point
config.py                   # Configuration management
README.md                   # Documentation (this file)
requirements.txt            # Python dependencies
```

---

## 🔧 Requirements

- 🐍 Python 3.7 or higher
- 🌐 Google Chrome and ChromeDriver

### 📜 Python Libraries

All necessary libraries are listed in the `requirements.txt` file. Install them using:

```bash
pip install -r requirements.txt
```

---

## 🚀 Setup

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate    # For Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
TWITTER_EMAIL=<your_twitter_email>
TWITTER_PASSWORD=<your_twitter_password>
TWITTER_URL=https://x.com/i/flow/login
MONGODB_URI=<your_mongo_uri
DB_NAME=twitter_trends
COLLECTION_NAME=trends
```

### Step 5: Set Up ChromeDriver

Download the appropriate version of ChromeDriver for your system from [here](https://chromedriver.chromium.org/downloads) and add it to your system's PATH.

---

## 📖 Usage

### Step 1: Start the Flask App

Run the Flask application:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`.

### Step 2: Access the Web Interface

Open your browser and navigate to the provided URL to start scraping.

---

## 🌐 Proxy Management

1. Add your proxies to `proxies/proxy_list.txt`.
2. Run `check_proxies.py` to validate the proxies:

   ```bash
   python proxies/check_proxies.py
   ```

3. Valid proxies will be saved to `proxies/valid_proxy_list.txt`.

---

## 💾 Database Integration

The tool uses MongoDB to store Twitter trends data. Ensure the following variables are correctly set in your `.env` file:

- `MONGODB_URI`: Your MongoDB connection string.
- `DB_NAME`: The name of the database (default: `twitter_trends`).
- `COLLECTION_NAME`: The name of the collection (default: `trends`).

Scraped data will be stored in the specified MongoDB collection.

---

## 🤝 Contribution

Feel free to fork the repository and contribute by submitting pull requests.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🙏 Acknowledgments

- 🛠 Selenium for web scraping
- 🌐 Flask for the web interface
- 💾 MongoDB for data storage
