# Z-Tube Backend

Welcome to the backend repository of Z-Tube, a comprehensive social media, e-commerce, and business platform. Built with the robust Python Django framework, Z-Tube offers a seamless experience for users to engage in social interactions, such as posting, tweeting, commenting, and chatting, as well as facilitating e-commerce activities like purchasing items. This backend is designed to support the diverse functionalities required by a modern, multi-faceted platform like Z-Tube.

## Features

- **Social Media Interactions**: Users can create, edit, and delete posts and tweets. The platform supports interactive features like comments and chats, enabling users to connect and engage with each other in real-time.
- **E-commerce Functionality**: Z-Tube integrates e-commerce features, allowing users to browse, select, and purchase items within the app. This seamless blend of social media and e-commerce creates a unique user experience.
- **Robust Backend**: Built with Django, the backend ensures high performance, security, and scalability. It is designed to handle the complex functionalities of a combined social media and e-commerce platform efficiently.

## Technologies Used

- **Django**: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework**: A powerful and flexible toolkit for building Web APIs, used to facilitate communication between the backend and frontend.
- **PostgreSQL**: Used as the primary database for development and production environments, respectively, to store user data, posts, comments, and product information.

## Getting Started

To set up the Z-Tube backend on your local machine, follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/rahulcodepython/Z-Tube-Backend.git
    cd Z-Tube-Backend
    ```

Create virtual environment:

```sh
python -m virtualenv venv
```

Activate environment:

for windows
- ```sh venv\Scripts\activate```
  
for linux
- ```sh source venv/bin/activate```

Install the required dependencies:

```sh
pip install -r requirements.txt
```


Run the Django migrations to prepare your database:

```sh
python manage.py migrate
```

Finally, start the development server:

```sh
python manage.py runserver
```

## Usage

1. Write an environment file named ```.env``` file:

```
DEBUG='True'
EMAIL_PORT=587
EMAIL_HOST_USER=<Email sending host user email>
EMAIL_HOST_PASSWORD=<Email sending host user password>
BASE_APP_URL='http://localhost:3000'
BASE_API_URL='http://127.0.0.1:8000'
FRONTEND_SITE_NAME='Z-Tube App'
DB_ENGINE='django.db.backends.postgresql'
DB_USER='rahul'
DB_NAME='postgres'
DB_PASSWORD='admin'
DB_HOST='localhost'
DB_PORT='5432'
GITHUB_OAUTH2_CLIENT_ID=<github auth client id>
GITHUB_OAUTH2_CLIENT_SECRET=<github auth secret key>
GITHUB_REDIRECT_URI='http://localhost:3000/github/callback'
GOOGLE_OAUTH2_CLIENT_ID=<google auth client id>
GOOGLE_OAUTH2_CLIENT_SECRET=<google auth secret key>
GOOGLE_REDIRECT_URI='http://localhost:3000/google/callback'
```

Now, the backend server should be running locally, and you can start developing or testing the API endpoints.

## Contributing

Contributions to the Z-Tube backend are welcome! Whether it's adding new features, fixing bugs, or improving documentation, your help is appreciated. Please refer to the CONTRIBUTING.md file for more details on how to contribute.
