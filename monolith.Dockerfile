# This file is only meant for deployment as a monolithic service
FROM nikolaik/python-nodejs:python3.12-nodejs20
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev \
    # removing unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

WORKDIR /code/frontend

RUN corepack enable

RUN pnpm install \
    && pnpm prune

ENV API_BASE=http://localhost:8000

VOLUME [ "/code/frontend/node_modules", "./frontend:code/frontend" ]

WORKDIR /code

EXPOSE 3000 8000

CMD ["npx", "concurrently", "cd ./frontend && pnpm run dev", "python manage.py runserver", "-y"]

# docker run -p 3000:3000 -p 8000:8000 <image name>
