update_venv:
    #!/bin/zsh
    echo "Updating venv"
    echo "Selecting python 3.9"
    poetry env use 3.9
    echo "Installing dependencies"
    poetry lock --no-update; poetry install
    echo "venv updated"

run: (update_venv)
    #!/bin/zsh
    echo "Running"
    poetry run streamlit run app.py
    echo "Running"

build:
    #!/bin/zsh
    echo "Building"
    docker-compose build
    echo "Built"

run_docker: (build)
    #!/bin/zsh
    echo "Running"
    docker-compose up
