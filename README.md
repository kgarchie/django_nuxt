# django_nuxt
## Getting Started
### Using Docker (Recommended)
This project is containerised using docker. Make sure you have Docker and Git installed then run the following commands.
```bash
git clone https://github.com/kgarchie/django_nuxt.git
cd django_nuxt
docker-compose up
```
Open your browser on http://localhost:3000 to use the web-app

### Shell commands
If you don't have docker, or you are facing problems, follow the instructions below to run it:
#### Install Python
1. Download and install Python3 and install it, make sure it's added to path.
1. Clone the repo, and start a shell session at therein.
1. Use the following commands to get started
    - First is the prerequisites; creating a python virtual environment and activating it
    Windows
    ```shell
    python -m venv venv && venv/Scripts/activate
    ```
1. Followed by installing dependancies
    ```bash
    pip install -r requirements.txt && cd ./frontend && corepack enable && pnpm install
    ```
1. Then running the web-app, you may need to run these commands on two separate shells/terminals
    ```bash
    python manage.py runserver
    ```
    ```bash
    cd ./frontend && pnpm run dev
    ```
1. Open your browser on http://localhost:3000 to use the web-app

### Running tests
Use the comman below to run tests. Tests are located in api/tests.py
```bash
python manage.py test
```
