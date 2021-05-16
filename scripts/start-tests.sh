#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

COVER_PROJECT_PATH=.
TESTS_PROJECT_PATH=tests
REPORTS_FOLDER_PATH=tests-reports

# PYTHONPATH is needed because of tests.support.inject_env_vars
# See pytest.ini
PYTHONPATH=. pytest $TESTS_PROJECT_PATH -vv --doctest-modules \
  --cov=$COVER_PROJECT_PATH \
  --junitxml=$REPORTS_FOLDER_PATH/junit.xml \
  --cov-report=xml:$REPORTS_FOLDER_PATH/coverage.xml \
  --cov-report=html:$REPORTS_FOLDER_PATH/html \
  --cov-report=term
