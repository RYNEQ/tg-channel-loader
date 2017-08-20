# tg-channel-loader

A media downloader script in python which can download all medias from a
channel (or chat of course)


## Dependencies

* Python 2.7
* [telegram-cli](https://github.com/vysheng/tg)
  * to download from channels telegram-cli needs to be patched based on
    the [vysheng/tgl#115](https://github.com/vysheng/tgl/pull/115)
    provided
    [here](https://github.com/regalstreak/XManager/commit/3515fa800b93213fe4138c05fde77b81be266108#diff-2c46835da3cef9a21d0bc3541afea13b);
    otherwise files only can be downloaded from chats and not channels
* [termcolor](https://pypi.python.org/pypi/termcolor) module
  * `sudo -H pip2 install termcolor` on Debian/Ubuntu will install it

**Note: You need to join the channel before running the script**

## Usage

1. Run `telegram-cli` as deamon with `json` response on desired port:

   here I used 2391

        telegram-cli -W -k tg-server.pub -D -vvv -d -E -R -C -P 2391 --json

2. Run Script on desired channel

   e.g. this will same all images of `somechannel` in a templorary
   directory:

        ./loadImages.py 2391 @somechannel $(mktemp -d)

### Ascii Cast

[![asciicast](https://asciinema.org/a/3geApnuQvCveFn809jlXhBI0i.png)](https://asciinema.org/a/3geApnuQvCveFn809jlXhBI0i)

## ToDo:

* add support for medias other than photos
* add error management
