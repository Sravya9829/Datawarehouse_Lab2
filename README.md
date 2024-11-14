# Scheduling a dbt Project with Airflow in Docker with Superset Visualization
## Project: Airflow-DBT-Superset Integration

This project demonstrates how to automate the scheduling of dbt (data build tool) jobs using Apache Airflow running in Docker, along with Superset for data visualization. The project focuses on integrating Airflow with a dbt project on Snowflake and visualizing the processed data through Apache Superset, enabling a robust end-to-end data pipeline and analytics solution.

## Introduction

The goal of this project is to automate the execution of dbt jobs using Airflow and visualize the resulting data transformations in Superset. By leveraging Airflow’s scheduling capabilities, dbt's transformation capabilities, and Superset's visualization tools, we create a comprehensive data pipeline that loads, transforms, and visualizes data in Snowflake.

## Technologies Used
- **Python**: Core scripting language for DAGs and data processing.
- **Apache Airflow**: Workflow automation tool to manage and schedule dbt jobs.
- **dbt**: Data build tool for data transformation within the Snowflake environment.
- **Snowflake**: Cloud data platform for storage and data transformation.
- **Docker**: Containerization platform for consistent and isolated environments.
- **Apache Superset**: Data visualization platform to create dashboards and explore data interactively.

## Setup and Installation

### Prerequisites
- Docker installed on your local machine.
- A Snowflake account for data storage and transformations.
- A dbt project set up and tested locally with Snowflake.
- Superset installed and configured to connect with Snowflake.

### Project Setup
1. **Clone or Copy dbt Project into Airflow Directory**:
   - Move your existing dbt project folder (named `dbt`) into the Airflow project folder, so it can be accessed by the Airflow Docker container.
   - Ensure that `profiles.yml` is correctly configured within the `dbt` folder to connect to Snowflake.

2. **Set Up Airflow and dbt in Docker**:
   - Modify the `docker-compose.yml` file to mount the `dbt` folder and install necessary packages:
     ```yaml
     services:
       airflow:
         volumes:
           - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
           - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
           - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
           - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
           - ${AIRFLOW_PROJ_DIR:-.}/dbt:/opt/airflow/dbt
         environment:
           _PIP_ADDITIONAL_REQUIREMENTS: "dbt-snowflake apache-airflow-providers-snowflake snowflake-connector-python"
     ```

3. **Install dbt-snowflake Package in Airflow**:
   - Make sure `dbt-snowflake` is added to `_PIP_ADDITIONAL_REQUIREMENTS` in `docker-compose.yml`.
   - Restart the Airflow container to apply changes:
     ```bash
     docker compose -f docker-compose.yml down
     docker compose -f docker-compose.yml up
     ```

### Superset Setup for Data Visualization

1. **Configure Snowflake Connection in Superset**:
   - In the Superset UI, go to **Data** > **Databases** > **+ Database**.
   - Select **Snowflake** as the database type.
   - Enter the necessary connection information, such as account, warehouse, database, and schema. A typical connection string looks like this:
     ```
     snowflake://<user>:<password>@<account>.snowflakecomputing.com/<database>/<schema>?warehouse=<warehouse>&role=<role>
     ```
   - Test the connection and save it.

2. **Import Tables into Superset**:
   - After successfully connecting to Snowflake, import the transformed tables created by dbt.
   - Navigate to **Data** > **Datasets** and click on **+ Dataset**.
   - Choose the Snowflake database, select the schema (e.g., `RAW_DATA`), and select the tables you want to visualize (e.g., `NPS` for raw data or `FORECAST_RESULTS` for predictions).

3. **Create Dashboards and Visualizations**:
   - Use the datasets imported from Snowflake to create charts and dashboards in Superset.
   - Visualizations can include line charts for stock predictions, tables for raw data, or other relevant analyses based on your dbt transformations.

## Configuration

### Configuring Airflow for dbt
1. **Add dbt Environment Variables**:
   - In the Airflow Web UI, navigate to **Admin > Variables**.
   - Set the necessary variables for the dbt configuration if needed (e.g., credentials or environment configurations).

2. **Snowflake Connection**:
   - Go to **Admin > Connections** in Airflow.
   - Add a new Snowflake connection with all relevant details, as shown in the earlier section.

## How to Run the Project

### Airflow DAG Execution
- **dbt Transformation DAG (`dbt_dag.py`)**: The main DAG that runs dbt commands for data transformation in Snowflake. This DAG will execute specific dbt jobs such as `dbt run`, `dbt test`, and `dbt snapshot`.

#### Example Commands in the DAG
- `dbt run`: Executes all transformations in the dbt project.
- `dbt test`: Runs tests to validate data quality in Snowflake.
- `dbt snapshot`: Takes a snapshot of tables for historical tracking.

### Steps to Run the DAG
1. Start your Airflow environment in Docker:
   ```bash
   docker compose -f docker-compose.yml up
   ```
2. Open the Airflow Web UI (usually at `http://localhost:8080`).
3. Trigger the `dbt_dag` manually or let it run on schedule as defined in the DAG file.

### Viewing Results in Superset
- Open Superset (usually at `http://localhost:8088`).
- Access the dashboards and charts created from your dbt-transformed data.
- Use these visualizations to analyze stock predictions, track metrics, or explore data transformations.

## Repository Overview
- **dbt_dag.py**: The Airflow DAG file that defines and schedules the dbt jobs.
- **docker-compose.yml**: Docker Compose file to set up and configure the Airflow environment with dbt.
- **dbt/**: The dbt project folder containing models, configurations, and `profiles.yml` for Snowflake.
- **superset_dashboards/**: (Optional) Folder to store JSON exports of Superset dashboards for version control.

## Troubleshooting

- **Common Errors**:
  - *ModuleNotFoundError*: Ensure `dbt-snowflake` is installed and listed in `_PIP_ADDITIONAL_REQUIREMENTS`.
  - *Connection Issues*: Double-check the Snowflake connection settings in `profiles.yml`, Airflow, and Superset.
  - *Permissions*: Ensure Docker has access to the `dbt` and `profiles.yml` files.

## Future Enhancements
Potential improvements include:
- Automating data refreshes in Superset to reflect real-time updates from dbt.
- Expanding the pipeline to include data ingestion from other sources.
- Using `DbtCloudRunJobOperator` to manage dbt jobs through dbt Cloud for simplified configuration.

## Contact Information
For further assistance, please contact:
- [satya@example.com](mailto:satya@example.com)
- [prerana@example.com](mailto:prerana@example.com)
- [chandana@example.com](mailto:chandana@example.com)
