# Pollboard

Pollboard is a robust Django REST API designed for creating, managing, and interacting with polls. It provides a backend infrastructure for users to publish polls, vote on active topics, and track engagement through likes and reports. The system also includes demographic tracking by capturing extensible user characteristics (age, gender, country) at the moment of voting for statistical analysis.

This project is designed for educational purposes and demonstrates a scalable architecture using Django REST Framework, PostgreSQL, and Redis.

## Features

* **User Authentication**: Secure registration and login handling using JWT (JSON Web Tokens) via Djoser.
* **Poll Management**:
    * Create, retrieve, update, and delete polls.
    * Set voting periods with automatic closing dates.
    * Categorize polls for easy filtering.


* **Engagement System**:
* **Voting**: Users can vote on polls within the active period. The system ensures one vote per user per poll.
* **Likes**: Users can like polls to show appreciation.
* **Reporting**: Community moderation tools allowing users to report polls with specific reasons.


* **Demographics & Statistics**:
    * User profiles track characteristics such as Country, Gender, and Age.
* **Snapshotting**: When a vote is cast, a snapshot of the user's characteristics is saved with the vote, allowing for historical demographic analysis even if the user's profile changes later.


* **Search & Filtering**: Filter polls by category, sort by creation date, or search by title and description.
* **Throttling**: Built-in rate limiting for anonymous and authenticated users to prevent abuse.

## 🚀 Upcoming Features (Roadmap)

The following features are currently in development and will be released soon:

* **Automoderation**: Integration with the **OpenAI Text Moderation API** to automatically flag or reject inappropriate poll content upon creation.
* **Vote Aggregation**: Advanced statistical endpoints to aggregate vote data based on user demographics (e.g., "How did users from Canada vote vs. users from the US?").

## Tech Stack

* **Language**: Python 3.13.7
* **Framework**: Django 5.2.6 & Django REST Framework
* **Database**: PostgreSQL
* **Caching & Throttling**: Redis
* **Authentication**: Djoser & SimpleJWT

## Installation & Setup

### Prerequisites

* Python 3.13+
* PostgreSQL
* Redis

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/Syzygicality/pollboard.git
cd pollboard

```


2. **Initialize the virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

```


3. **Install dependencies**
```bash
pip install -r app/requirements.txt

```


4. **Environment Configuration**
Create a `.env` file in the `app/` directory. You can use the `app/template.env` as a reference. Fill in your database and Redis credentials:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pollboard
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=localhost
DB_PORT=5432
# Add REDIS configuration if necessary per settings.py

```


5. **Database Setup**
Ensure your PostgreSQL server is running and the database (e.g., `pollboard`) is created.
```bash
cd app
python manage.py migrate

```


6. **Run the Server**
```bash
python manage.py runserver

```



## Major API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/auth/` | POST | User registration and token management (Djoser) |
| `/polls` | GET | List all polls (supports filtering and search) |
| `/polls/create` | POST | Create a new poll |
| `/polls/<id>` | GET | Retrieve a single poll |
| `/vote/<poll_id>/<option_id>` | POST | Cast a vote on a specific option |
| `/polls/<id>/like` | POST | Like a poll |
| `/polls/<id>/report` | POST | Report a poll |
| `/users/characteristics` | GET/PUT | Manage user demographics |

## License

Distributed under the MIT License. See `LICENSE` for more information.