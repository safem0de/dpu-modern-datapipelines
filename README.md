### dpu-modern-datapipelines

#### run extract-loading to JSONBin
```bash
python 2025_01_18/app.py
```

#### run air-flow on docker
create envi for air-flow
```bash
mkdir -p mnt/dags mnt/tests mnt/logs mnt/plugins weather
or
mkdir -p dags logs plugins config
```

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```