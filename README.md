# 🔁 Scalable API Data Ingestion & Conditional Workflow Automation with Azure Data Factory

📺 **Demo Video Included**

## 📘 Project Summary

This project presents a production-ready architecture built with **Azure Data Factory (ADF)** that handles both scheduled data ingestion and conditional pipeline execution. It integrates data from multiple REST API sources and uses logic-based workflows to simulate real-world enterprise ETL systems.

---

## 🌐 Key Capabilities

* 🌍 **Multinational API Ingestion** — Fetch metadata from five countries (India, US, UK, China, Russia) using the [RESTCountries API](https://restcountries.com).
* 🧠 **Threshold-Based Pipeline Control** — Dynamically route execution based on incoming record volumes.
* ☁️ **Data Lake Integration** — Store JSON results into **Azure Data Lake Storage Gen2 (ADLS)**.
* 🕓 **Automated Scheduling** — Pipelines are scheduled to run **twice daily**, ensuring timely data availability.

---

## 🧱 Architecture Highlights

### ✅ 1. **Country Metadata Pipeline**

Ingests and stores country-specific data using:

* **Linked Services**: One per country (Total: 5)
* **Datasets**: Individual dataset for each REST endpoint
* **Activities**:

  * `ForEach` activity iterates over country names
  * `Switch` activity handles logic per country
  * `Copy` activity stores data to: `/data-export/{country}.json`
* **Trigger Time**: Runs at **12:00 AM** and **12:00 PM IST**

---

### ✅ 2. **Conditional Customer & Product Pipeline**

A dynamic pipeline that adjusts based on incoming data volume:

* Retrieves customer data via the `randomuser.me` API
* If **customer count > 500**:

  * Data is saved to ADLS
  * Triggers **child product pipeline**
* In the child pipeline:

  * If **product count > 600**, additional processing is triggered
* Implements:

  * **Parent-child pipeline linking**
  * **If Conditions** and **Switch statements**
  * **Dynamic parameterization and expressions**

---

## 🛠️ Tools & Technologies Used

| Component                | Purpose                                  |
| ------------------------ | ---------------------------------------- |
| Azure Data Factory (ADF) | Orchestration & ETL processing           |
| Azure Data Lake Gen2     | Data storage (JSON format)               |
| REST APIs                | Data sources (RESTCountries, RandomUser) |
| JSON / Expressions       | Logic & transformation rules             |
| ADF Triggers             | Time-based automation                    |
| Control Activities       | ForEach, Switch, If-Else, Web, Copy      |

---

## ⚙️ Pipeline Flow Summary

### 🌍 **Country Data Pipeline**

* Iterates over 5 countries: `["india", "us", "uk", "china", "russia"]`
* For each:

  * Calls REST API
  * Writes data to ADLS path `/data-export/{country}.json`

### 👤 **Conditional Workflow Pipeline**

* Pulls **1000 random users**
* If record count > 500:

  * Dumps to ADLS
  * Triggers child pipeline
* In child pipeline:

  * If record count > 600:

    * Executes a placeholder for product processing

---

## 📅 Scheduling Details

* ⏰ **Country Metadata Pipeline**: Triggered at **12:00 AM & 12:00 PM IST**
* 🕹️ **Conditional Pipeline**: Triggered manually or scheduled based on use case

---

## 📊 Real-World Applications

* Automated ingestion for real-time dashboards
* API-to-lake ETL framework for enterprise-scale analytics
* Condition-based orchestration using ADF’s built-in control flow
* Educational demonstrations for advanced ADF features

---

## ✅ Final Outcome

This solution demonstrates how to build:

* 🔁 Reusable and modular pipelines
* ⏱️ Time-driven automation for API ingestion
* 🤖 Intelligent ETL orchestration using ADF expressions, parameters, and triggers

