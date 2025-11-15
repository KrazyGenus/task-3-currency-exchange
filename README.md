
# 🌍 Task 3 — A simple Country Currency & Exchange Rate Data

A simple RESTful API built with **FastAPI** that fetches country and exchange rate data from external APIs, computes estimated GDP, and stores results in a **MySQL** database for cached access.

This project fulfills the **HNG Backend Stage 2 Task**: *Country Currency & Exchange API*.

---

## 📋 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [API Endpoints](#api-endpoints)
* [Setup Instructions](#setup-instructions)
* [Environment Variables](#environment-variables)
* [Running the App](#running-the-app)
* [Response Samples](#response-samples)
* [Error Handling](#error-handling)
* [License](#license)

---

## 🧩 Overview

The **TerraRate API** fetches country information and exchange rates, matches each country's currency to its rate, and calculates an **estimated GDP** using:

```
estimated_gdp = population × random(1000–2000) ÷ exchange_rate
```

The results are cached in a MySQL database and refreshed manually via the `/countries/refresh` endpoint.

---

## ⚙️ Features

* Fetch countries from [`restcountries.com`](https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies)
* Fetch exchange rates from [`open.er-api.com`](https://open.er-api.com/v6/latest/USD)
* Match each country's currency with its rate
* Compute estimated GDP
* Store and update country data in a MySQL database
* Generate a summary image showing:

  * Total number of countries
  * Top 5 countries by estimated GDP
  * Last refresh timestamp

---

## 🧰 Tech Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Package Manager:** [uv](https://github.com/astral-sh/uv)
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **HTTP Client:** `httpx`
* **Image Generation:** `Pillow`
* **Server:** Uvicorn

---

## 🚀 API Endpoints

| Method   | Endpoint             | Description                                        |
| -------- | -------------------- | -------------------------------------------------- |
| `POST`   | `/countries/refresh` | Fetch and refresh all countries and exchange rates |
| `GET`    | `/countries`         | Get all countries (supports filters and sorting)   |
| `GET`    | `/countries/{name}`  | Get a single country by name                       |
| `DELETE` | `/countries/{name}`  | Delete a country by name                           |
| `GET`    | `/status`            | Show total countries and last refresh timestamp    |
| `GET`    | `/countries/image`   | Serve generated summary image                      |

### 🧭 Query Filters

`GET /countries` supports filters and sorting:

```
/countries?region=Africa
/countries?currency=NGN
/countries?sort=gdp_desc
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
[git clone https://github.com/LunarKhord/task-3-currency-exchange.git]
cd task-3-currency-exchange
```

### 2️⃣ Install Dependencies (using uv)

```bash
uv sync
```

### 3️⃣ Create a `.env` File

In the project root, create a `.env` file:

```env
DATABASE_URL=mysql+mysqlconnector://<username>:<password>@<host>/<database_name>
PORT=7000
```

*(Ensure MySQL is running and the database exists.)*

### 4️⃣ Run Database Migrations (if using Alembic)

```bash
alembic upgrade head
```

*(Optional if you have migration scripts.)*

---

## ▶️ Running the App

### Run Development Server

```bash
uvicorn main:app --reload --port 7000
```

### Or via uv run

```bash
uv run uvicorn main:app --reload --port 7000
```

The API will be available at:
👉 **[http://127.0.0.1:7000](http://127.0.0.1:7000)**

---

## 🧾 Response Samples

### ✅ `GET /status`

```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}
```

### 🌍 `GET /countries?region=Africa`

```json
[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-22T18:00:00Z"
  }
]
```

---

## ❌ Error Handling

| Status Code | Example Response                                                                                          |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| **400**     | `{ "error": "Validation failed" }`                                                                        |
| **404**     | `{ "error": "Country not found" }`                                                                        |
| **500**     | `{ "error": "Internal server error" }`                                                                    |
| **503**     | `{ "error": "External data source unavailable", "details": "Could not fetch data from open.er-api.com" }` |

---



## 🧪 Testing(LocalHost)

You can use tools like **Postman** or **cURL** to test the endpoints.
Example:

```bash
curl -X POST http://127.0.0.1:7000/countries/refresh
curl http://127.0.0.1:7000/countries?region=Africa
```

---

## 📄 License

This project is released under the [MIT License](LICENSE).

---

## 🧠 Author

**Muhammad Hasim**
Backend Engineer | HNG 12 Intern
📧 Email: *[krazygenus@gmail.com](bugfix.exe@gmail.com)*
🐙 GitHub: [@KrazyGenus](https://github.com/KrazyGenus)
