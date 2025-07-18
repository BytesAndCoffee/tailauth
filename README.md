# tailauth

**tailauth** is a [ZNC](https://znc.in) global module that allows automatic login for IRC clients connecting from the [Tailscale](https://tailscale.com) network (100.64.0.0/10). It's designed to simplify authentication in zero-trust environments where network-level access is already protected.

## Features

- Automatically accepts login attempts from Tailscale-assigned IPs
- Logs all login attempts (accepted or rejected)
- No password required for Tailscale users
- Designed to be secure under the assumption of a trusted Tailscale network

## Requirements

- ZNC 1.10 or newer
- `modpython` compiled and enabled
- Python 3.x

## Installation

1. Make sure your ZNC is compiled with Python support (`--enable-python` or `-DWANT_PYTHON=ON`)
2. Copy `tailauth.py` into your ZNC global modules directory:
```
~/.znc/modules/    # For user-specific
/usr/local/share/znc/modules/   # Or system-wide
```
3. Load the module via webadmin or `/znc LoadMod tailauth`

## How It Works

The module intercepts each login attempt. If the client's IP falls within the Tailscale subnet (100.64.0.0/10), the user is authenticated automatically (as long as any non-empty password is provided) — assuming the ZNC user exists.

All events are logged to:
```
~/.znc/modules-data/global/tailauth/tailauth.log
```

## Security

This module assumes your Tailscale network is trusted and secure. Only users connected via Tailscale can bypass password auth. It's **not** recommended to use this module outside such a secure overlay network.

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

Contributions welcome! Open a PR or reach out in `#znc` on [Libera.Chat](https://libera.chat).
