# django_nuxt
## Getting Started
### Using Docker
This project is containerised using docker. Make sure you have Docker and Git installed then run the following commands.
```bash
git clone https://github.com/kgarchie/django_nuxt.git
cd django_nuxt
docker-compose up
```
Open your browser on http://localhost:3000 to use the web-app

### Shell commands (Recommended)
If you don't have docker, or you are facing problems, follow the instructions below to run it:

1. Download Python3 and install it, make sure it's added to path.
1. Download and install NodeJs ^18
1. Clone the repo, and start a shell session at therein.
```bash
git clone https://github.com/kgarchie/django_nuxt.git
cd django_nuxt
```
1. Use the following commands to get started
    ### Windows
    ```shell
    ./run.bat
    ```

    ### Linux
    ```bash
    chmod +x ./run.sh && ./run.sh
    ```

1. Open your browser on http://localhost:3000 to use the web-app

### Running tests
Use the command below to run tests. Tests are located in api/tests.py
```bash
python manage.py test
```
