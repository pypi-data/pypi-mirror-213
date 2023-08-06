import os
import re

from thoth_doc.utils import get_docstring, remove_whitespaces


def code_reference_parser(_, line):
    ''' Parses [@code/main.py#Class.method] syntax. Extacts docstring. '''

    matches = re.findall(r'(\[@(.+?)\])', line)
    if matches:
        for match in matches:
            mod, name = match[1].split('#')
            docstring = get_docstring(mod, name)
            docstring = remove_whitespaces(docstring)
            docstring = docstring.replace('\n', '\n\n')
            line = line.replace(match[0], docstring)
        return line
    return line


def env_var_parser(_, line):
    ''' Parses [$env.ENV_VAR_NAME] syntax '''

    matches = re.findall(r'(\[\$env\.(\w+)\])', line)
    if matches:
        for match, var_name in matches:
            value = os.environ.get(var_name)
            line = line.replace(match, str(value))
        return line
    return line


def django_settings_parser(_, line):
    ''' Parses [$settings.SETTINGS_VAR_NAME] syntax '''

    matches = re.findall(r'(\[\$settings\.(\w+)\])', line)
    if matches:
        try:
            from django.conf import settings
        except ImportError:
            raise ImportError('Django is not installed')
        for match, setting_name in matches:
            value = getattr(settings, setting_name)
            line = line.replace(match, str(value))
        return line
    return line
