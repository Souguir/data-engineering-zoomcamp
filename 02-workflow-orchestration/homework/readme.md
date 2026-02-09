### Module 2 Homework — Workflow Orchestration (Kestra)

Homework link: [02-workflow-orchestration/homework.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/02-workflow-orchestration/homework.md)

This README contains:
- Evidence of backfilling 2021 data for **yellow** and **green** taxi datasets
- Answers to the **6 quiz questions**, with screenshots

#### Evidence screenshots (Backfill + BigQuery tables)

**Backfill Yellow (2021-01-01 → 2021-07-31)**  
![Backfill yellow 2021](screenshots/backfill-yellow-2021.png)

**Backfill Green (2021-01-01 → 2021-07-31)**  
![Backfill green 2021](screenshots/backfill-green-2021.png)

**BigQuery tables after loading 2021 data (Yellow + Green present)**  
![BQ tables yellow + green 2021](screenshots/bq-yellow_greendat-2021.png)

**BigQuery green_tripdata table (schema view)**  
![BQ green_tripdata 2021](screenshots/bq-green_tripdata-2021.png)

### Quiz Answers

#### Q1) Uncompressed file size for Yellow Taxi `2020-12` (`yellow_tripdata_2020-12.csv`)
**Answer:** `134.5 MiB`  
![Q1 evidence](screenshots/quiz1.png)

#### Q2) Rendered value of `file` for `taxi=green`, `year=2020`, `month=04`
**Answer:** `green_tripdata_2020-04.csv`  
![Q2 evidence](screenshots/quiz2.png)

#### Q3) Rows for Yellow Taxi data for all CSV files in year 2020
**Answer:** `24,648,499`  
![Q3 evidence](screenshots/quiz3.png)

#### Q4) Rows for Green Taxi data for all CSV files in year 2020
**Answer:** `1,734,051`  
![Q4 evidence](screenshots/quiz4.png)

#### Q5) Rows for Yellow Taxi data for March 2021
**Answer:** `1,925,152`  
![Q5 evidence](screenshots/quiz5.png)

#### Q6) Configure timezone to New York in a Schedule trigger
**Answer:** Add a `timezone` property set to `America/New_York`  
![Q6 evidence](screenshots/quiz6.png)

### Notes
- Backfill period used: `2021-01-01` to `2021-07-31` (as instructed).
- The flow was executed for both taxi types (`yellow` and `green`) using Kestra backfill.
