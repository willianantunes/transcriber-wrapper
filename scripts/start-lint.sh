#!/usr/bin/env bash

TARGET_PROJECT=transcriber_wrapper
TARGET_TEST_PROJECT=tests
TARGET_FOLDERS="$TARGET_PROJECT $TARGET_TEST_PROJECT"

echo "######## ISORT..."
isort $TARGET_FOLDERS -c --diff
echo "######## BLACK..."
black --check --diff $TARGET_FOLDERS
echo "######## MYPY..."
# mypy will only target the project folder
mypy $TARGET_PROJECT
