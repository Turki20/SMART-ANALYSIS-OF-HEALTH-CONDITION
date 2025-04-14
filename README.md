# Smart Analysis Of Health Conditions
...

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
4.create database
```sql
CREATE DATABASE smart_analysis_of_health_condition;
```
* setting.py
5. Connect the project to the database through the setting.py file.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smart_analysis_of_health_condition',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
* terminal (windows)
6. Run migrations:
``` bash
python manage.py makemigrations
python manage.py migrate
```
7. run the project
```bash
python manage.py runserver
```

