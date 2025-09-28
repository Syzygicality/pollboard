# Pollboard
Pollboard is a Django REST API for creating and managing polls. Users can create and save drafts, put up polls, and vote and like others' polls. This application was designed for educational purposes.

## Features

- User registration and authentication
- Create, like, and delete polls
- Create and save poll drafts
- Vote on polls
- View voted and liked polls
- Searching, sorting, and filtering

## Tech Stack

- Python 3.13.7
- Django 5.2.6
- Django REST Framework
- PostgreSQL

## Setup

1. Clone the repository
```bash
git clone https://github.com/Syzygicality/pollboard.git
cd pollboard
```
2. initialize the virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run migrations (make sure that the database has been set up)
```bash
cd pollboard
python3 manage.py migrate
```
5. Start server
```bash
python manage.py runserver
```