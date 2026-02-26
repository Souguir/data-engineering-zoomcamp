# Homework 04 – Analytics Engineering (dbt + BigQuery)


## 📦 Step 1 – Upload CSV.GZ files to Google Cloud Storage

### 1. Green Taxi (2019 & 2020)
```bash
BUCKET="gs://data_analytics_homework_bucket/nyc-green"
YEARS="2019 2020"
MONTHS="01 02 03 04 05 06 07 08 09 10 11 12"

for year in $YEARS; do
  for month in $MONTHS; do
    FILENAME="green_tripdata_${year}-${month}.csv.gz"
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/${FILENAME}"
    echo "Uploading $FILENAME ..."
    if curl -sSfL "$URL" | gsutil cp - "$BUCKET/$FILENAME"; then
      echo "✓ $FILENAME uploaded"
    else
      echo "✗ $FILENAME not available"
    fi
  done
done
```

### 2. Yellow Taxi (2019 & 2020)
```bash
BUCKET="gs://data_analytics_homework_bucket/nyc-yellow"
YEARS="2019 2020"
MONTHS="01 02 03 04 05 06 07 08 09 10 11 12"

for year in $YEARS; do
  for month in $MONTHS; do
    FILENAME="yellow_tripdata_${year}-${month}.csv.gz"
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/${FILENAME}"
    echo "Uploading $FILENAME ..."
    if curl -sSfL "$URL" | gsutil cp - "$BUCKET/$FILENAME"; then
      echo "✓ $FILENAME uploaded"
    else
      echo "✗ $FILENAME not available"
    fi
  done
done
```

### 3. FHV – 2019 only
```bash
BUCKET="gs://data_analytics_homework_bucket/nyc-fhv-2019"
YEAR="2019"
MONTHS="01 02 03 04 05 06 07 08 09 10 11 12"

for month in $MONTHS; do
  FILENAME="fhv_tripdata_${YEAR}-${month}.csv.gz"
  URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/${FILENAME}"
  echo "Uploading $FILENAME ..."
  if curl -sSfL "$URL" | gsutil cp - "$BUCKET/$FILENAME"; then
    echo "✓ $FILENAME uploaded"
  else
    echo "✗ $FILENAME not available"
  fi
done
```

### Verify uploads in GCS
```bash
gsutil ls gs://data_analytics_homework_bucket/nyc-green/
gsutil ls gs://data_analytics_homework_bucket/nyc-yellow/
gsutil ls gs://data_analytics_homework_bucket/nyc-fhv-2019/
```

---

## 🗄️ Step 2 – Create External Tables in BigQuery

External tables point to the raw CSV.GZ files stored in GCS without loading data into BigQuery storage.

```sql
-- Green External Table
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-sandbox-sg.zoomcamp.external_green_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data_analytics_homework_bucket/nyc-green/green_tripdata_*.csv.gz']
);

-- Yellow External Table
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-sandbox-sg.zoomcamp.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data_analytics_homework_bucket/nyc-yellow/yellow_tripdata_*.csv.gz']
);

-- FHV 2019 External Table
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-sandbox-sg.zoomcamp.external_fhv_2019_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://data_analytics_homework_bucket/nyc-fhv-2019/fhv_tripdata_2019-*.csv.gz']
);
```

---

## 🚀 Step 3 – Create Native Tables in BigQuery

Native tables materialize the data inside BigQuery storage for better query performance and full feature support (partitioning, clustering, time travel).

```sql
-- Green Native Table
CREATE OR REPLACE TABLE `zoomcamp-sandbox-sg.zoomcamp.green_tripdata_hw4` AS
SELECT * FROM `zoomcamp-sandbox-sg.zoomcamp.external_green_tripdata`;

-- Yellow Native Table
CREATE OR REPLACE TABLE `zoomcamp-sandbox-sg.zoomcamp.yellow_tripdata_hw4` AS
SELECT * FROM `zoomcamp-sandbox-sg.zoomcamp.external_yellow_tripdata`;

-- FHV 2019 Native Table
CREATE OR REPLACE TABLE `zoomcamp-sandbox-sg.zoomcamp.fhv_2019_tripdata` AS
SELECT * FROM `zoomcamp-sandbox-sg.zoomcamp.external_fhv_2019_tripdata`;
```

---

## ❓ Questions & Answers

### Question 1 – dbt Lineage and Execution

**Question:**  
Given the following dbt project structure:
```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```
If you run `dbt run --select int_trips_unioned`, what models will be built?

**Answer:** `int_trips_unioned` only ✅

**Explanation:**  
By default, `dbt run --select <model>` only builds the specified model.  
- To include upstream dependencies: `dbt run --select +int_trips_unioned`  
- To include downstream dependencies: `dbt run --select int_trips_unioned+`  
- Without the `+` operator, only the selected node is executed.

---

### Question 2 – dbt Tests

**Question:**  
An `accepted_values` test is configured for `payment_type` with values `[1, 2, 3, 4, 5]`.  
A new value `6` appears in the source data. What happens when you run `dbt test --select fct_trips`?

**Answer:** `dbt will fail the test, returning a non-zero exit code` ✅

**Explanation:**  
The `accepted_values` test runs a SQL query to find rows where the column value is not in the allowed list. When value `6` is found, the test returns failing rows → dbt marks the test as **FAIL** with a non-zero exit code (`1`), which stops any CI/CD pipeline to prevent bad data from flowing downstream.

---

### Question 3 – Row count in `fct_monthly_zone_revenue`

**SQL Query:**
```sql
SELECT COUNT(*) 
FROM `zoomcamp-sandbox-sg.dbt_asouguir.fct_monthly_zone_revenue`;
```

**Result:** `12184` ✅

---

### Question 4 – Top Green taxi zone by revenue in 2020

**SQL Query:**
```sql
SELECT 
    pickup_zone, 
    MAX(revenue_monthly_total_amount) AS max_revenue
FROM `zoomcamp-sandbox-sg.dbt_asouguir.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND revenue_month >= '2020-01-01'
  AND revenue_month <= '2020-12-31'
GROUP BY pickup_zone
ORDER BY MAX(revenue_monthly_total_amount) DESC
LIMIT 1;
```

**Result:** `East Harlem North` – `434592.76` ✅

---

### Question 5 – Total Green trips in October 2019

**SQL Query:**
```sql
SELECT SUM(total_monthly_trips)
FROM `zoomcamp-sandbox-sg.dbt_asouguir.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND revenue_month >= '2019-10-01'
  AND revenue_month <= '2019-10-31';
```

**Result:** `384624` ✅

---

### Question 6 – Row count in `stg_fhv_2019_tripdata`

**SQL Query:**
```sql
SELECT COUNT(*) 
FROM `zoomcamp-sandbox-sg.dbt_asouguir.stg_fhv_2019_tripdata`;
```

**Result:** `43244693` ✅


