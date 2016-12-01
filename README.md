# razer-serval-linux-driver
This driver maps razer serval keys to another configurable keys.

## Instalation:
Install requirements. You can use virtualenv, or just:

```sudo pip install -r requirements.txt```

## Usage:

1. Connect and turn on your razer serval
2. Disable default serval input. You can use command:

```xinput --disable "$(xinput list --id-only 'Razer Razer Serval')"```
3. Run driver:

```sudo python serval.py```

## Configuration:
Edit config.py. Keycodes are available at https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
