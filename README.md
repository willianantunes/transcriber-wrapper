# Transcriber Wrapper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Inspired by [Phonemizer](https://github.com/bootphon/phonemizer), this a simpler version focused in transcription applications that work with IPA (International Phonetic Alphabet). This works like a wrapper which is responsible to call a back-end application, let's say [espeak-ng](https://github.com/espeak-ng/espeak-ng). It adds some features on top of it like `with stress` option.

## Updating pipenv dependencies

If you update Pipfile, you can issue the following command to refresh your lock file:

    docker-compose run remote-interpreter pipenv update

## Using it in your project

For now, you need to install [espeak-ng](https://github.com/espeak-ng/espeak-ng) on your operational system. See [Dockerfile.dev](./Dockerfile.dev) as an example.
