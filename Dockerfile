FROM python:3.8
#ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 5000

WORKDIR /app
# Allows docker to cache installed dependencies between builds
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install -U pip && \
    pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy

COPY . .
EXPOSE 5000
RUN chmod +x bin/start_app.sh

ENTRYPOINT [ "bin/start_app.sh" ]
