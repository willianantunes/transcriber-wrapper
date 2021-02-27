#!/usr/bin/env bash

TARGET_PROJECT=transcriber_wrapper
TARGET_TEST_PROJECT=tests
TARGET_FOLDERS="$TARGET_PROJECT $TARGET_TEST_PROJECT"

isort -rc $TARGET_FOLDERS -c --diff
black --check --diff $TARGET_FOLDERS
# mypy will only target the project folder
mypy $TARGET_PROJECT
