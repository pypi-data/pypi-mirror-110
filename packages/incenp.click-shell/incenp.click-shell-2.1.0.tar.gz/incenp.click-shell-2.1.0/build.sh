#!/bin/bash

set -e

mkdir -p reports

# Code linting
echo "Running pycodestyle..."
pycodestyle incenp

echo "Running pylint..."
pylint incenp --reports=n --exit-zero --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt

# Type checking
echo "Running mypy..."
mypy incenp

# Unit tests
pytest -vv --cov=incenp --cov-report=xml
