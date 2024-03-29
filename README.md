## Audio Files

The application is designed to manage upload/download of .wav formatted audio files with a subsequent conversion to .mp3. 
It's written using the FastAPI framework and requires a quick registration with a valid email address to upload audio files.

## Installation

Before getting the project, make sure you've [Docker](https://docs.docker.com/engine/install/) installed and configured.
To set up the application, create a project directory on your computer, navigate to it and run:

```bash
git clone https://gitlab.com/praktikant101/fastapi_music_files.git
```

Once the project is downloaded, in the root directory of the newly created folder,
you should see the following structure:


```bash
├── Dockerfile
├── README.md
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── database.py
├── docker-compose.yml
├── main.py
├── postgres_config.sh
├── requirements.txt
├── src
│   ├── audiofile
│   ├── auth
│   ├── config.py
│   └── slugging.py
├── static
└── venv
    ├── bin
    ├── include
    ├── lib
    └── pyvenv.cfg
```

For further reference we will refer to as a "rd", standing for root directory.
In rd, create a .env (not cloned) as per .env_example. You can copy the DB_HOST and DB_ENGINE parameters from the .env_example.
The remaining parameters you can set as you wish.

The application uses the SMTP protocol to send emails with activation code. Once you register an account, you'll receive a code with an 
activation code that you'll have to use to activate your account. To ensure this functionality, you'll have to configure the following parameters
with an application in the Google App Passwords as per [here](https://bshoo.medium.com/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e):

MAIL_USERNAME=\
MAIL_FROM=\
MAIL_PASSWORD=\
MAIL_PORT=\
MAIL_SERVER="smtp.gmail.com"\
MAIN_FROM_NAME=

For the #Authentication values, please refer to [here](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).

## Buildup

To launch the project, in rd, run:

```bash
docker-compose up --build
```

## Usage

After the project is built, you can access the application on http://0.0.0.0:8000/docs.




