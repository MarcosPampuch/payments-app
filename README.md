# Payments & Receivables Platform

## Introduction

This project is a simple, modular platform for managing payments and receivables. It demonstrates a modern event-driven architecture using Python microservices, Kafka for event streaming, and PostgreSQL for persistent storage. The platform allows you to ingest payment data (via CSV or synthetic generation), process and validate transactions, and visualize results through a dashboard interface.

---

## System Architecture

![System Architecture Diagram](./architecture.png)

Below is a brief description of each container in the system:

### Containers Overview

- **Postgres**  
  The main relational database for storing users, currencies, and transactions records.

- **Broker**  
  Kafka broker is used as the event streaming platform for ingesting and distributing payment events. It is composed by the topics `payments-events` and `import-payments-events`.

- **Metabase**  
  An open-source business intelligence tool for visualizing and exploring the data stored in Postgres.

- **Payments Ingestion Service**  
  A Python service that consumes messages from Kafka topics `payments-events` and `import-payments-events`, validates them, and upserts them into the Postgres table `transactions`. This service is also responsible for creating the Postgres tables, indexes, constraints, and triggers, as well as populating the users and currencies tables—all managed through migrations using the Alembic framework.

- **Data Generator**  
  A Python service that generates synthetic payment events every 2 seconds and publishes them to Kafka for demonstration purposes.

- **CSV Importer UI**  
  A Flask web application that allows users to upload CSV files containing payment data. The app parses, validates, and streams the data to Kafka, highlighting duplicated and suspicious records (e.g., high-value transactions).

- **Minio**  
  The Minio container is responsable for holding all CSV files uploaded by the Importer UI.
  
---

## Data Validation Flow

Data validationw before inserting data in the database are performed in two stages:

- **CSV Importer UI:**
  - Only checks if the uploaded file is a valid, non-corrupted CSV and remove duplicates. It does not validate the content or schema of individual records.

- **Payments Ingestion Service:**
  - Performs all record-level validation. Each record consumed from Kafka is checked against the expected schema.
  - Any record that fails schema validation is **not inserted** into the database, and a log entry is created for every invalid record, making it easy to audit and debug ingestion issues.

---

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MarcosPampuch/payments-app.git
   ```

2. **Start the system using Docker Compose:**
   ```bash
   docker-compose up --build -d
   ```
   This will build and start all containers defined in the `docker-compose.yml` file.

3. **(Recommended) Insert first load of data through CSV file:**
   
    i. Access the [csv importer interface](http://localhost:5050).
    
    ii. Load file `csvs/huge_load_transactions`.

4. **(Optional) View logs for a specific service:**
   ```bash
   docker-compose logs -f <service-name>
   ```


---

## Accessing the CSV Importer

Once all containers are running, you can access the CSV Importer UI to upload payment data:

- **URL:**  
  [http://localhost:5050](http://localhost:5050)

- **How to use:**  
  1. Open the URL in your browser.
  2. Upload a CSV file with payment records.
  3. The UI will display and drop any duplicate for you and also output suspicious records before sending them to Kafka for processing.

- **Check uploaded files:**  
  1. All files uploaded can be seen in Minio's UI interface: [http://localhost:9001/browser/files-imported](http://localhost:9001/browser/files-imported)
  2. Credentials to access the UI are:
      - **User:** admin
      - **Password:** password1234

---

## Accessing Metabase Dashboards

Metabase provides a user-friendly interface to explore and visualize your payment data:

- **URL:**  
  [http://localhost:3000](http://localhost:3000)

- **Credentials:**
  - **User:** marcospampuch@gmail.com
  - **Password:** #1_Circle

- **How to use:**  
  1. Open the URL in your browser.
  2. Log in with the credentials above.
  3. Navigate to the **Home** page.
  4. Access the **Overview Dashboard** to see the metrics and visualizations for your payment data.
 
---

## Pre-generated CSV Files for Import

A set of pre-generated CSV files is provided in the repository for testing and demonstration.

These files are located in the `csvs/` directory.

### CSV File Descriptions

- **huge_load_transactions.csv**  
  A large dataset of transactions, intended primarily for initial database population and bulk testing.

- **suspicious_duplicated_transactions.csv**  
  Contains example transactions that include both duplicated records and records with amounts above the suspicious threshold (amount > 8000).

- **suspicious_transactions.csv**  
  Contains only transactions with amounts above the suspicious threshold (amount > 8000).

- **regular_transactions.csv**  
  Contains only valid, unique transactions (no duplicates, no suspicious amounts).

---

## Environment

This project was developed and tested with the following versions:

- **Docker:** 28.1.1, build 4eba377
- **Docker Compose:** v2.35.1-desktop.1

---

## Future Improvements

Here are some ideas for future enhancements to this platform:

- **Integrate all UIs:**
  - Unify the Minio, CSV Importer and Metabase interface by a root page that redirects the user.

- **CSV Schema Validation:**
  - Implement stricter validation of CSV columns in the UI Importer to ensure only valid files are processed.

- **Data Warehouse Replication:**
  - Develop a batch or streaming process (using Kafka Connect, Debezium, or custom code) to replicate data from Postgres to a data warehouse, enabling advanced analytics and dashboarding.

---

## Observations

### Transaction Updates

Updates of records are only possible through the `transaction_id` field. Both the data generator and UI importer are primarily designed for inserting new records (as they never generate repeated transaction IDs). However, updates are possible if a transaction with an existing `transaction_id` is inserted into the `payments-events` topic.

When an upsert operation completes successfully, the `modified_at` column will be updated to the current timestamp.

### Testing Transaction Updates

To test the update functionality, follow these steps:

1. **Access the Kafka broker container:**
   ```bash
   docker exec -it broker bash
   ```

2. **Insert a record using the Kafka console producer:**
   ```bash
   /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic payments-events
   ```

3. **Important Note:** The `transaction_id` of the event must currently exist in the transactions table for the update to work properly.


---

