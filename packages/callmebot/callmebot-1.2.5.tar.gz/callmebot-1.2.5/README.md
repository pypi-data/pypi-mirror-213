# CallMeBot Python Client

This module offers a simple client to the [CallMeBot](https://www.callmebot.com/) service to send Whatsapp, Telegram and Signal text messages.


## Installation

Install with `pip3 install callmebot`.


## Usage

1. You should first configure CallMeBot as explained at https://www.callmebot.com/

2. Set the environment variables for the services you wish to use:

    ```bash
    export CALLMEBOT_WHATSAPP_PHONE=555123123123
    export CALLMEBOT_WHATSAPP_APIKEY=999999
    ```

3. Call the desired function (`whatsapp`, `signal`, `telegram`|) with the message to be sent:

    ```python
    import callmebot

    callmebot.whatsapp('This is an important message!\nRegards.')
    ```

4. Or, use the `callmebot` command line:

    ```bash
    callmebot whatsapp 'This is an important message!\nRegards.'
    ```

    Get help with `--help`:

    ```bash
    callmebot --help
    ```

## Credits

- [Jordi Petit](https://github.com/jordi-petit)


## License

Apache License 2.0
