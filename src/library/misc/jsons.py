#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: FIXME: XXX: HACK: NOTE: INTENT: USAGE:

import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter




# NOTE: AREA for functions.

def print_json(json_component):
    json_data = json.loads(json_component)
    formatted_json_data = json.dumps(json_data, indent=4)
    print(highlight(formatted_json_data, JsonLexer(), TerminalFormatter()))