import re


def contains_letter(line):
    for c in line:
        if c.isalpha():
            return True
    return False


def find_token_end(lines, start):
    end = 0

    for i, line in enumerate(lines[start:]):
        if i == len(lines) - 1 - start:
            break

        if len(line) == 0 or line[0] == '\n' or (len(line) == 1 and line[0] == '\n') or line == '':
            continue

        if line[0] == ' ' and contains_letter(line):
            end = i

        if i != 0 and line[0].isalpha():
            break

    return start + end + 1


def find_token_body(lines, token):
    re_class = re.compile(r"class\s+" + re.escape(token) + r"\b(\((?:[\w\s,]+)?\))?.*?(?=class|\Z)", re.DOTALL)
    re_func = re.compile(f'.+def\s+({token})')
    re_var = re.compile(f'^%s[,\s]*=.+({token})')

    for i, line in enumerate(lines):
        if not (re_class.match(line) or re_func.match(line) or re_var.match(line)):
            continue

        end = find_token_end(lines, i)
        body = ''.join(lines[i:end]).strip()
        return body, i, end
    return '', -1, -1


def find_docstring_in_body(body):
    re_docstring = re.compile(r'("""(.+?)""")|(\'\'\'(.+?)\'\'\')', re.DOTALL)
    match_obj = re_docstring.search(body)
    if match_obj:
        docstring = match_obj.group(2) or match_obj.group(4)
        return docstring.strip()
    return ''


def remove_whitespaces(docstring):
    return '\n'.join([line.strip() for line in docstring.split('\n')])


def get_docstring(filepath, name):
    with open(filepath) as f:
        lines = f.readlines()

    tokens = name.split('.')

    while tokens:
        token = tokens.pop(0)
        body, start, end = find_token_body(lines, token)
        lines = body.split('\n')

    docstring = find_docstring_in_body(body)
    references = re.findall('(\[@(.+?)\])', docstring)
    if not references:
        return docstring

    for ref in references:
        if '#' in ref[1]:
            mod, name = ref[1].split('#')
            docstring = docstring.replace(ref[0], get_docstring(mod, name))
        else:
            if ref[1].startswith('.'):
                name = token + ref[1]
            else:
                name = ref[1]
            docstring = docstring.replace(ref[0], get_docstring(filepath, name))
    return docstring
