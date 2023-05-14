FROM python:3.9

COPY pyproject.toml pyproject.toml
RUN sed -i '/packages/d' pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install poetry
# Added because of a bug in poetry 1.4.1
RUN poetry config installer.modern-installation false
RUN poetry config installer.max-workers 10
RUN poetry install
RUN poetry run python -c "import solcx; solcx.install_solc('0.8.19')"

COPY naturalchain naturalchain
COPY app.py app.py
COPY .streamlit/docker_config.toml .streamlit/config.toml
COPY assets assets

RUN apt update
RUN apt install nodejs npm -y
WORKDIR /naturalchain
RUN npm cache clean --force
RUN npm i @openzeppelin/contracts@4.8.3
WORKDIR /


ENTRYPOINT ["poetry", "run", "python", "-m", "streamlit", "run", "app.py"]
