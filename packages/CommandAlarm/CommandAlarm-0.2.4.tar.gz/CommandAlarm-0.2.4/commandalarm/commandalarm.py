#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# commandalarm.py
# Copyright (C) 2023 alofgren <drelofren@outlook.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
""" Set an alarm with a custom command. """

import signal
import sys
import time
import datetime
import argparse
import subprocess
from . import __version__

ALARM_FIRED = False  # pylint: disable=W0603


def alarm_handler(signum, frame):  # pylint: disable=W0613
    """
    Handle the alarm signal.

    Parameters:
    signum (int): The signal number.
    frame (frame object): The current stack frame.

    Returns:
    None
    """
    global ALARM_FIRED  # pylint: disable=W0603
    ALARM_FIRED = True


def set_alarm(time_str, day):
    """
    Sets an alarm for a specific time and day.

    Parameters:
    time_str (str): The time in the format HH:MM:SS.
    day (int): The day of the week as an integer from 1 to 7, where 1 represents Monday.

    Returns:
    None
    """
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    date_obj = datetime.date.today()
    days_ahead = day - date_obj.isoweekday()
    if days_ahead < 0 or (days_ahead == 0
                          and datetime.datetime.now().time() > time_obj):
        days_ahead += 7
    date_obj += datetime.timedelta(days=days_ahead)
    alarm_datetime = datetime.datetime.combine(date_obj, time_obj)
    seconds_until_alarm = int(
        round((alarm_datetime - datetime.datetime.now()).total_seconds()))
    if seconds_until_alarm <= 0:
        seconds_until_alarm = 1
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(seconds_until_alarm)
    print(f"Alarm set for {alarm_datetime}")


def validate_weekday(value):
    """
    Validates whether the given value is a valid weekday integer between 1 and 7.

    Parameters:
    value (str): The value to be validated.

    Returns:
    int: The weekday integer if it is valid.

    Raises:
    argparse.ArgumentTypeError: If the value is not a valid integer or not a valid weekday.
    """
    try:
        weekday = int(value)
        if weekday < 1 or weekday > 7:
            raise argparse.ArgumentTypeError(
                "%s is not a valid weekday (must be between 1 and 7)" % value)
        return weekday
    except ValueError as value_err:
        raise argparse.ArgumentTypeError("%s is not a valid integer" %
                                         value) from value_err


def valid_time_string(time_str):
    """
    Validates that the time string is in the correct format.

    Parameters:
    time_str (str): The time in the format HH:MM:SS.

    Returns:
    str: The time string if it is valid.

    Raises:
    argparse.ArgumentTypeError: If the time string is not in the correct format.
    """
    try:
        datetime.datetime.strptime(time_str, "%H:%M:%S")
        return time_str
    except ValueError as value_err:
        raise argparse.ArgumentTypeError(
            f"{time_str} is not a valid time in the format HH:MM:SS"
        ) from value_err


def main():
    """
    The main function that parses command-line arguments, sets the alarm and runs the command.
    """
    global ALARM_FIRED  # pylint: disable=W0603
    parser = argparse.ArgumentParser(
        description="Set an alarm with a custom command.")
    parser.add_argument(
        "time",
        type=valid_time_string,
        help="the time in the format HH:MM:SS",
    )
    parser.add_argument(
        "command",
        type=str,
        nargs="+",
        help="the command to run",
    )
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument(
        "-d",
        "--day",
        type=validate_weekday,
        default=datetime.date.today().isoweekday(),
        help=
        "the day of the week as an integer from 1 to 7, where 1 represents Monday",
        choices=range(1, 8),
    )
    parser.add_argument(
        "-r",
        "--repeat",
        action="store_true",
        help="repeat indefinitely",
    )
    parser.add_argument("-s",
                        "--shell",
                        action="store_true",
                        default=False,
                        help="run command with shell")
    parser.add_argument("-n",
                        "--no-check",
                        action="store_false",
                        default=True,
                        help="don't check the command return code",
                        dest="check")
    parser.add_argument("-t",
                        "--timeout",
                        default=None,
                        type=int,
                        help="timeout in seconds for the command to complete")
    args = parser.parse_args()
    try:
        set_alarm(args.time, args.day)
        while True:
            while not ALARM_FIRED:
                signal.pause()
            print("Time is up!")
            command_str = " ".join(args.command)
            print("Running command:", command_str)
            try:
                command = command_str if args.shell else args.command
                result = subprocess.run(command,
                                        capture_output=True,
                                        shell=args.shell,
                                        timeout=args.timeout,
                                        check=args.check,
                                        text=True)
                print(result.stdout)
            except FileNotFoundError:
                print("Command not found", file=sys.stderr)
            except subprocess.CalledProcessError as called_process_err:
                print(
                    f"Command returned non-zero exit status {called_process_err.returncode}",
                    file=sys.stderr)
                print(f"stderr: {called_process_err.stderr}", file=sys.stderr)
            except PermissionError as permission_err:
                print(f"Permission error: {permission_err}", file=sys.stderr)
            except subprocess.TimeoutExpired as timeout_expired:
                print(
                    f"Command timed out after {timeout_expired.timeout} seconds",
                    file=sys.stderr)
            if args.repeat:
                ALARM_FIRED = False
                time.sleep(1)
                set_alarm(args.time, args.day)
            else:
                break
    except KeyboardInterrupt:
        print("Alarm stopped manually.", file=sys.stderr)
        signal.alarm(0)
        sys.exit(1)


if __name__ == "__main__":
    main()
