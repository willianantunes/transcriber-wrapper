# Transcriber Wrapper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=willianantunes_transcriber-wrapper&metric=coverage)](https://sonarcloud.io/dashboard?id=willianantunes_transcriber-wrapper)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=willianantunes_transcriber-wrapper&metric=ncloc)](https://sonarcloud.io/dashboard?id=willianantunes_transcriber-wrapper)

Inspired by [Phonemizer](https://github.com/bootphon/phonemizer), this a simpler version focused in transcription applications that work with IPA (International Phonetic Alphabet). This works like a wrapper which is responsible to call a back-end application, let's say [espeak-ng](https://github.com/espeak-ng/espeak-ng). It adds some features on top of it like `with stress` option.

## Supported back-ends

- [eSpeakNG](https://en.wikipedia.org/wiki/ESpeak)
- [Festival Speech Synthesis System](https://en.wikipedia.org/wiki/Festival_Speech_Synthesis_System)

## Usage

You need to install espeak-ng and festival on your operational system. See [Dockerfile.dev](./Dockerfile.dev) as an example. After that, you can create a transcriber and then use it in your logic:

```python
from typing import List

import transcriber_wrapper

# The standard language is "en-us"
# The standard back-end is "espeak"
transcriber_en_us = transcriber_wrapper.build_transcriber()

def do_the_thing(words: List[str]) -> List[str]:
    return transcriber_en_us.transcribe(words)
```

Don't forget to see [test_builder.py](./tests/int/test_builder.py) to get insights how to use this project!

## Development

### Executing commands directly on the binaries

After building the remote interpreter service, just enter in it:

    docker-compose run remote-interpreter sh

You must be at `/usr/bin/`. Then try one of these below.

#### eSpeakNG

Check out these links:

- [Supported Languages](https://github.com/espeak-ng/espeak-ng/blob/53915bf0a7cd48f90c4a38ac52fff697723d9f4d/docs/languages.md)
- [Command Line User Guide](https://github.com/espeak-ng/espeak-ng/blob/53915bf0a7cd48f90c4a38ac52fff697723d9f4d/src/espeak-ng.1.ronn)

Some sample commands:

```shell
espeak-ng "Hello my friend, stay awhile and listen!" -ven-us -x --ipa -q --sep=_
espeak-ng "Curiosity" -ven-us -x --ipa -q --sep=" "
espeak-ng "If you will not bow before a sultan, then you will cower before a sorcerer!" -ven-us -x --ipa -q
espeak-ng --voices
```

#### Festival

You can execute `festival --help` to get a list of what you can do through what the festival developers call "Shell API" (see more details [here](http://www.festvox.org/docs/manual-2.4.0/festival_28.html#Shell-API)).

You can use the script [festival.lisp](./scripts/festival.lisp) to get the computation from a given word, some samples:

```shell
WORD=something festival -b /app/scripts/festival.lisp
WORD=theoretically festival -b /app/scripts/festival.lisp
```

What you can do is just type `festival` and then start its command line prompt. From there you can do the following for example:

```shell
# It will list voices available
festival> (voice.list)
# Default voice
festival> voice_default
# This won't work with our Docker image, but if you are on your ubuntu/debian machine, it may will
(SayText "Can someone refactor festival to be writen in Python with a friendly API?") 
```

### Updating pipenv dependencies

If you update Pipfile, you can issue the following command to refresh your lock file:

    docker-compose run remote-interpreter pipenv update

If you'd like to add a new package, let's say a production one:

    docker-compose run remote-interpreter pipenv install pyparsing

Don't forget to update your service!

    docker-compose build remote-interpreter
