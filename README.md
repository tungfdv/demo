# Waste MGMT Django BE

## Quickstart

> **NOTE**: Install **Python >= 3.8** as most of project dependencies are not compatible below that version.

### 1. Clone Repository

```bash
$ git clone <project-git-url>
```

### 2. Setup and activate VirtualEnv

Inside your cloned repository directory, run following commands:

```bash
$ python3 -m venv venv
```

```bash
$ source venv/bin/activate
```

```bash
$ pip install -r requirements.txt
```

### 3. Start the server

Once all dependencies are installed, you can start your server via terminal using `manage.py` script.

```bash
# migrate db
$ python manage.py makemigrations
$ python manage.py migrate
# runserver
$ python manage.py runserver
```

and kill the server using `ctrl+c`.

> **Note:** Make sure you create a `.env` file and change environment variables as per your requiremnts.
