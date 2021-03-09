#!/usr/bin/env bash

COVER_PROJECT_PATH=.
TESTS_PROJECT_PATH=tests
REPORTS_FOLDER_PATH=tests-reports

pytest $TESTS_PROJECT_PATH -vv --doctest-modules \
  --cov=$COVER_PROJECT_PATH \
  --junitxml=$REPORTS_FOLDER_PATH/junit.xml \
  --cov-report=xml:$REPORTS_FOLDER_PATH/coverage.xml \
  --cov-report=html:$REPORTS_FOLDER_PATH/html \
  --cov-report=term
