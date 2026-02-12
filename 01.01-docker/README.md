# Module 1 Homework: Docker & SQL

## Question 1: Understanding Docker Images
**Command:**
```bash
docker run -it --rm --entrypoint=bash python:3.13
pip -V
```
**Answer:** `25.3`

---

## Question 2: Understanding Docker Networking and docker-compose
**Answer:** `postgre:5432`

---

## Question 3: Counting Short Trips
**Answer:** `8007`

**SQL Query:**
```sql
SELECT count(*) 
FROM public.green_trip_table gt
WHERE gt.lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
  AND gt.trip_distance <= 1
```

---

## Question 4: Longest Trip for Each Day
**Answer:** `2025-11-14`

**SQL Query:**
```sql
SELECT gt.lpep_pickup_datetime, MAX(gt.trip_distance) 
FROM public.green_trip_table gt
WHERE gt.trip_distance < 100 
GROUP BY gt.lpep_pickup_datetime
ORDER BY MAX(gt.trip_distance) DESC
LIMIT 1
```

---

## Question 5: Biggest Pickup Zone
**Answer:** `East Harlem North`

**SQL Query:**
```sql
SELECT tz."Zone", SUM(gt."total_amount") AS total_amount_by_zone
FROM taxi_zone_table tz
INNER JOIN green_trip_table gt ON tz."LocationID" = gt."PULocationID"
WHERE DATE(gt."lpep_pickup_datetime") = '2025-11-18'
GROUP BY tz."Zone"
ORDER BY total_amount_by_zone DESC
LIMIT 1
```

---

## Question 6: Largest Tip
**Answer:** `Yorkville West`

**SQL Query:**
```sql
SELECT tz_dropoff."Zone" AS dropoff_zone, MAX(gt."tip_amount") AS total_tip_amount
FROM taxi_zone_table tz_pickup
INNER JOIN green_trip_table gt ON tz_pickup."LocationID" = gt."PULocationID"
INNER JOIN taxi_zone_table AS tz_dropoff ON tz_dropoff."LocationID" = gt."DOLocationID"
WHERE TO_CHAR(gt."lpep_pickup_datetime", 'YYYY-MM') = '2025-11'
  AND tz_pickup."Zone" = 'East Harlem North'
GROUP BY tz_dropoff."Zone"
ORDER BY total_tip_amount DESC
LIMIT 1
```

---

## Question 7: Terraform Workflow
**Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`
