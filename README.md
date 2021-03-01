# Transcriber Wrapper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=willianantunes_transcriber-wrapper&metric=coverage)](https://sonarcloud.io/dashboard?id=willianantunes_transcriber-wrapper)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=willianantunes_transcriber-wrapper&metric=ncloc)](https://sonarcloud.io/dashboard?id=willianantunes_transcriber-wrapper)

Inspired by [Phonemizer](https://github.com/bootphon/phonemizer), this a simpler version focused in transcription applications that work with IPA (International Phonetic Alphabet). This works like a wrapper which is responsible to call a back-end application, let's say [espeak-ng](https://github.com/espeak-ng/espeak-ng). It adds some features on top of it like `with stress` option.

## Usage

For now, you need to install [espeak-ng](https://github.com/espeak-ng/espeak-ng) on your operational system. See [Dockerfile.dev](./Dockerfile.dev) as an example. After that, you can create a transcriber and then use it in your logic:

```python
from typing import List

import transcriber_wrapper

# The standard language is "en-us"
transcriber_en_us = transcriber_wrapper.build_transcriber()

def do_the_thing(words: List[str]) -> List[str]:
    return transcriber_en_us.transcribe(words)
```

## Development

### Updating pipenv dependencies

If you update Pipfile, you can issue the following command to refresh your lock file:

    docker-compose run remote-interpreter pipenv update
