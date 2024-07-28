# Django Chat Application with WebSockets

This Django-based chat application allows users to chat in real-time using WebSockets. It leverages Django Channels to handle WebSocket connections and asynchronous communication.

## Features

- Real-time chat with multiple users
- WebSocket-based communication
- User authentication and authorization
- Message history
- Room-based chat (optional)

## Prerequisites

- Python 3.12
- Django
- Django Channels

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Soumen3/Namaste.git
   cd django-chat-app
   ```

2. Create a virtual environment and activate it:

   ```bash
  	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Django project:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/` in your web browser.

## Usage

1. Access the chat application at `http://127.0.0.1:8000/`.
2. Log in using your superuser credentials.
3. Search your friends.
4. Send them friend request.
5. Start chatting with them after the accept your request.
