# Smart Analysis Of Health Conditions

## Features
- 
-
-

## Requirements
Before installing the project, ensure that you have the following prerequisites installed:
- Python: 3.13.2
- pip: 25.01
- MySQL: mysql-8.4.4
- MySQL Workbench 8.0 CE

## Installation and Setup
* terminal (windows)
1. Clone the repository:
```bash
git clone https://github.com/Turki20/SMART-ANALYSIS-OF-HEALTH-CONDITION.git
cd Smart_Analysis_of_Health_Condition
```
2. Create and activate virtual environment:
```bash
python -m virtualenv env
```
```bash
cd env/Scripts
activate
cd ..
cd ..
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

* MySQL
```sql
CREATE DATABASE trip_to_jeddah;
```
* setting.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trip_to_jeddah',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
* terminal (windows)
``` bash
python manage.py makemigrations
python manage.py migrate
```
```bash
python manage.py runserver
```

