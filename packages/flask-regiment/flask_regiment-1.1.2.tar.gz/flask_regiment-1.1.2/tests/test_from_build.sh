#!/bin/bash
./venv/bin/pip uninstall flask_regiment
./venv/bin/pip install ../dist/flask_regiment*.whl
FLASK_APP=test_flask_regiment FLASK_RUN_PORT=12345 ./venv/bin/flask run
