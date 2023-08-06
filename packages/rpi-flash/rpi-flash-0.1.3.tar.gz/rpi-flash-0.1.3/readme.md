# rpi-flash

Script to flash and configure a disk image. Image may be local or via http, and may be gz compressed. To minimise flash writes, each block is read and compared first.

Made specifically for my Raspberry Pi flashing process, it may not be suitable for you. Currently supports macOS only.

## Configuraton

Configuration assumes a partition with `.configure_me` in its root. If not found this will be skipped.
The configuration is compatible with my custom [`rpi-base`](https://github.com/hillnz/rpi-image-base) image.

Run with `--write-env` to generate a .env file with variables and docs.
