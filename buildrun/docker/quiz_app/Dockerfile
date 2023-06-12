FROM python:3.10.2-buster as base-image


ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir pip-tools==6.6.0
WORKDIR /code


# -----

FROM base-image as production-image

# creates a system user (-r), with no password, no home directory set, and no shell
RUN groupadd -r default-group && useradd -r -s /bin/false -g default-group default-user

RUN chown -R default-user:default-group /code
COPY --chown=default-user:default-group ./src /code/
COPY --chown=default-user:default-group ./buildrun/docker/quiz_app/requirements/prod-requirements.txt /code/requirements.txt
RUN pip-sync requirements.txt --pip-args '--no-cache-dir --no-deps'
USER default-user


# -----

FROM base-image as base-test-image

# creates a system user (-r), with no password, no home directory set, and no shell
RUN groupadd -r default-group && useradd -r -s /bin/false -g default-group default-user

RUN chown -R default-user:default-group /code
COPY --chown=default-user:default-group ./buildrun/docker/quiz_app/requirements/test-requirements.txt /code/requirements.txt
RUN pip-sync requirements.txt --pip-args '--no-cache-dir --no-deps'

USER default-user


# -----

FROM base-image as dev-image

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
COPY ./buildrun/docker/quiz_app/requirements/dev-requirements.txt /code/requirements.txt
RUN pip-sync requirements.txt --pip-args '--no-cache-dir --no-deps'


# -----

FROM base-test-image as test-image

COPY --chown=default-user:default-group ./src /code/
ENV SECRET_KEY=not-secret
ENV SIMPLE_JWT_SIGNING_KEY=not-secret-either
ENV DATABASE_URL=postgresql://test_user:test_pwd@db:5432/test_db
ENV ENV_MODE=TEST
ENV DJANGO_SETTINGS_MODULE=configurations.test-settings


CMD ["sh","-c","python manage.py collectstatic --noinput && python manage.py makemigrations --check && python manage.py migrate && pytest"]
# -----
