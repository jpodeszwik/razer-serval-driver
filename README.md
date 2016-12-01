# razer-serval-linux-driver
This driver maps razer serval keys to another configurable keys.

## Instalation:
Install requirements. You can use virtualenv, or just:

```sudo pip install -r requirements.txt```

## Usage:

* Connect and turn on your razer serval
* Disable default serval input. You can use command:
```bash
xinput --disable "$(xinput list --id-only 'Razer Razer Serval')"
```
* Run driver:

```sudo python serval.py```

## Configuration:
Edit config.py. Keycodes are available at https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
