### dpu-modern-datapipelines
---
#### create enviroment for folder
```bash
python -m venv 2025_01_18
```
#### then change directory
```bash
cd 2025_01_18/
```
#### activate environment folder
```bash
source bin/activate
```
#### create .env file
```bash
JSONBIN_API_KEY=**************
JSONBIN_COLLECTION_ID=****************
```
#### run extract-loading to JSONBin
```bash
python app.py
```
#### install all lib
```bash
pip install -r requirements.txt
```
#### update lib list
```bash
pip freeze > requirements.txt
```
---
#### run air-flow on docker
create envi for air-flow
```bash
mkdir -p mnt/dags mnt/tests mnt/logs mnt/plugins weather
```
```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
user/pass default
```bash
user : airflow
pass : airflow
```