# OpenClassrooms Projet P9

## Objectif
The young startup LITReview aims to market a product that allows a community of users to access or request book reviews on demand. The project's goal is to develop this web application using Django.

## Architecture and directories
```bash
│  .gitignore
│  admin.py
│  apps.py
│  encrypt.py
│  models.py
│  tests.py
│  __init__.py
│
│
├─static
│  ├─css
│  ├─images
│  │      favicon.ico
│  │
│  ├─js
│  └─plugins
│      └─bootstrap-5.1.3-dist
│          ├─css
│          │      bootstrap.min.css
│          └─js
│
├─templates
│  │  create_ticket.html
│  │  critique.html
│  │  feed.html
│  │  followers.html
│  │  inscription.html
│  │  layout.html
│  │  login.html
│  │  loyout_login_signup.html
│  │  modifier_critique.html
│  │  modifier_ticket.html
│  │  posts.html
│  │  reply_ticket.html
│  │  review_flux_snippet.html
│  │  review_snippet.html
│  │  tickets_flux_snippet.html
│  └─  ticket_snippet.html
│ 
│ 
├─utils
│  └─  forms.py
│  
│
├─views
    │  feed.py
    │  follower.py
    │  inscription.py
    │  login.py
    │  posts.py
    │  review.py
    │  signout.py
    └─  ticket.py
```

## Local Configuration
## Installation

### Getting the project on your local machine.
1. Clone the repository to your local machine.
```bash
git clone https://github.com/xrobotzyh/openclassroomsprojet9.git
```
2.Navigate to the cloned directory.
```bash
cd openclassroomsprojet9
```

### Create a virtual environment
1.Create a virtual environment named "env".
```bash
python3 -m venv env
```

### Activate and install your virtual environment
Activate the newly created virtual environment "env".
```bash
source env/bin/activate
```
Install the packages listed in requirements.txt.
```bash
pip install -r requirements.txt
```

### Initialize the database
Navigate to the working directory.
```bash
cd LiteReview
```
Perform a search for migrations.
```bash
python manage.py makemigrations
```
Apply the migrations.
```bash
python manage.py migrate
```

## Usage
### Start the serveur
```bash
python manage.py runserver
```
### Navigation
Access the site on your browser using the URL http://127.0.0.1:8000/

## Test
Use the following information to test
```bash
| User name             | password   
|-----------------------|---------------|
| test-didi             | 123456789     | 
| test2-lulu            | 123456789     | 
```

## Thanks!
