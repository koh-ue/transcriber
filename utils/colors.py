#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"
BOLD_BLUE = "\033[1;34m"
BOLD_PURPLE = "\033[1;35m"
BOLD_SKYBLUE = "\033[1;36m"
BOLD = "\033[1;0m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
SKYBLUE = "\033[36m"

END = "\033[0m"


def print_in_bold_red(words):
	print(BOLD_RED + words + END)

def print_in_bold_green(words):
	print(BOLD_GREEN + words + END)