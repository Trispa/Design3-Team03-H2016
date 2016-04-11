#!/bin/sh
v4l2-ctl -c gain=0
v4l2-ctl -c brightness=128
v4l2-ctl -c exposure_auto=1
v4l2-ctl -c white_balance_temperature_auto=0
v4l2-ctl -c exposure_absolute=110
v4l2-ctl -c white_balance_temperature=504
