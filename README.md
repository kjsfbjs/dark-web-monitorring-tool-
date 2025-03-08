# Dark Web Monitoring Tool

## 📌 Overview

Sahil's **Dark Web Monitoring Tool** is a Python-based command-line application that helps users check if their email has been breached and search for specific keywords on the dark web. It leverages the **Have I Been Pwned (HIBP) API** for breach detection and uses the **Tor network** for secure and anonymous dark web searches.

## 🚀 Features

- **Email Breach Check**: Uses the HIBP API to verify if an email has been leaked in data breaches.
- **Dark Web Keyword Search**: Connects through the Tor network to scan hidden `.onion` websites.
- **Search History Logging**: Stores past searches in an SQLite database.
- **Redis Caching**: Speeds up API calls and prevents redundant checks.
- **Interactive CLI**: User-friendly interface with progress bars and color-coded messages.
- **Tor Anonymity**: Utilizes Tor proxies for safe browsing.
- **Random User-Agent Spoofing**: Prevents tracking by dark web sites.

## 🛠️ Installation

### **Prerequisites**

- Python 3.8+
- Tor (must be installed and running)
- Redis (for caching API responses)

### **Setup**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourrepo/dark-web-monitor.git
   cd dark-web-monitor
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   ```bash
   export HIBP_API_KEY="your_hibp_api_key"
   export TOR_PASSWORD="your_tor_control_password"
   ```
4. **Start Tor (if not running)**:
   ```bash
   tor
   ```
5. **Run the tool**:
   ```bash
   python main.py
   ```

## 🎮 Usage

When you launch the tool, you will see an interactive CLI menu:

```
========================================
      🌐 Sahil's Dark Web Monitor 🌐
========================================

🔍 1. Check if an email has been breached
🕵️ 2. Search for a keyword on the dark web
📜 3. View search history
❌ 4. Exit
➡️ Enter your choice (1/2/3/4):
```

### **1️⃣ Email Breach Check**

- Enter an email, and the tool will check if it appears in known breaches.
- Results are cached in Redis for 24 hours.
- Example Output:
  ```
  🚨 [!] example@email.com has been found in breaches:
  - Breach: "LinkedIn" | Date: 2016 | Compromised: Emails, Passwords
  - Breach: "Adobe" | Date: 2013 | Compromised: Emails, Passwords
  ```

### **2️⃣ Dark Web Keyword Search**

- Enter a keyword (e.g., "bitcoin", "credit card") to scan `.onion` sites.
- The tool rotates IP addresses using Tor for security.
- Example Output:
  ```
  🔍 Searching for 'bitcoin' on the dark web...
  ❌ [-] No results found for 'bitcoin'.
  ```

### **3️⃣ View Search History**

- Shows past email and keyword searches.
- Example Output:
  ```
  📜 Search History:
  - Checked email: example@email.com
  - Searched keyword: bitcoin
  ```

### **4️⃣ Exit**

- Exits the program safely.

## 🔐 Security Considerations

- The tool **does not store user credentials**.
- API keys should be set using **environment variables**.
- Dark web searches run **anonymously** via Tor.
- SQLite database is used only for logging search history.

## 📜 License

This project is licensed under the MIT License. Feel free to modify and improve it.

## 📞 Support

For issues or suggestions, open an issue on GitHub or contact Sahil. 

[sahil.musani379@gmial.com](mailto\:sahil.musani379@gmial.com)

---

Enjoy monitoring your digital footprint securely! 🚀

