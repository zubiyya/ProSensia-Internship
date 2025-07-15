# 🌐 Exchange Rate API Data Fetcher

## 📌 Overview
This Python script fetches **real-time currency exchange rates** using the [ExchangeRate-API](https://www.exchangerate-api.com/).  
It extracts rates for selected currencies and saves the output to a formatted text report.

> 🔄 Default base currency: **USD**

---

## 🛠 Tools & Concepts Used
- `requests` → for HTTP communication with public APIs  
- `json` → for parsing the API response  
- Reusable functions and modular design  
- Error handling for invalid URLs or data issues

---

## 🔗 Public API Used
- **Name:** Exchange Rate API  
- **URL:** `https://api.exchangerate-api.com/v4/latest/USD`  
- **Auth:** No authentication required (Free tier)

---

## 🧾 Sample Output

📊 Exchange Rate Report (Base: USD)  
----------------------------------------  
USD: 1.0  
GBP: 0.78  
EUR: 0.91  
PKR: 278.5  

> *(Values may vary depending on the live data returned)*

---

## 📁 Project Structure
Day 13/
├── api_fetcher.py # Main script
├── exchange_rate_report.txt # Output report (auto-generated)
└── README.md # This file


---

## ▶️ How to Run the Script

### 1. Install Python Dependencies
If `requests` isn’t installed:
```bash
pip install requests
