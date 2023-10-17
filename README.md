# Haringey visitor parking voucher helper

Buying visitor parking vouchers using Haringey's website is so painful and
tedious, that it was worth writing a Python script to help me do it.

## Details

Given a date, this script will use two (already-purchased) guest parking
vouchers for a given car between 2pm and 4pm.

These will be valid in the Bruce Grove West controlled parking zone (CPZ).

| Environment variable             | Notes                              |
| -------------------------------- | ---------------------------------- |
| `HARINGEY_USERNAME`                | To log on to https://haringey.tarantopermits.com/ |
| `HARINGEY_PASSWORD`                |                                    |
| `HARINGEY_CAR_REG`                 | A UK car reg, like AB12 CDE        |

## Usage

```shell
HARINGEY_CAR_REG='<my-car-reg>' HARINGEY_USERNAME='<my-email-address>' HARINGEY_PASSWORD='<my-password>' python parking.py 2023-10-19
```
