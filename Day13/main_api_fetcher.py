{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "943a5a00-0997-4ce3-a7ef-6cbda77dcc4d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " Exchange Rate Report (Base: USD)\n",
      "----------------------------------------\n",
      "USD: 1.0\n",
      "GBP: 0.744\n",
      "EUR: 0.857\n",
      "PKR: 284.68\n",
      "\n",
      "Report saved to exchange_rate_report.txt\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import json\n",
    "\n",
    "def fetch_exchange_data(url='https://api.exchangerate-api.com/v4/latest/USD'):\n",
    "    try:\n",
    "        response = requests.get(url)\n",
    "        response.raise_for_status()\n",
    "        return response.json()\n",
    "    except requests.exceptions.RequestException as e:\n",
    "        print(\"API request failed:\", e)\n",
    "        return None\n",
    "\n",
    "def extract_prices(data):\n",
    "    try:\n",
    "        rates = data['rates']\n",
    "        return {\n",
    "            'USD': 1.0,  # Base is USD, so always 1.0\n",
    "            'GBP': rates['GBP'],\n",
    "            'EUR': rates['EUR'],\n",
    "            'PKR': rates.get('PKR', 'N/A')  # Optional\n",
    "        }\n",
    "    except KeyError:\n",
    "        print(\"Invalid JSON structure.\")\n",
    "        return None\n",
    "\n",
    "def format_report(prices):\n",
    "    report = \" Exchange Rate Report (Base: USD)\\n\"\n",
    "    report += \"-\" * 40 + \"\\n\"\n",
    "    for currency, value in prices.items():\n",
    "        report += f\"{currency}: {value}\\n\"\n",
    "    return report\n",
    "\n",
    "def save_report(report, filename='exchange_rate_report.txt'):\n",
    "    with open(filename, 'w') as f:\n",
    "        f.write(report)\n",
    "    print(f\"Report saved to {filename}\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    url = 'https://api.exchangerate-api.com/v4/latest/USD'\n",
    "    data = fetch_exchange_data(url)\n",
    "    if data:\n",
    "        prices = extract_prices(data)\n",
    "        if prices:\n",
    "            report = format_report(prices)\n",
    "            print(report)\n",
    "            save_report(report)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "34cf20ea-b004-49a0-9651-9d335ce613fe",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
