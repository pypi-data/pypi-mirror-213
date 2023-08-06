import os

from thoth_doc.parsers import code_reference_parser



class DocGenerator:
    parsers = []
    image_host = None
    _default_parsers = [code_reference_parser]

    def __init__(self, docs_folder, compiled_docs_folder):
        self.docs_folder = docs_folder
        self.compiled_docs_folder = compiled_docs_folder

    def _get_compiled_docs_path(self, path=None):
        cwd = os.getcwd()
        if path and path.startswith('/'):
            path = path[1:]
        return f'{cwd}/{self.compiled_docs_folder}/{path}' if path else f'{cwd}/{self.compiled_docs_folder}'

    def _compile_lines(self, markdown_lines):
        compiled_markdown = ''
        skip = False

        for line in markdown_lines:
            if line.startswith('[ignore]'):
                skip = True
                continue
            elif line.startswith('[endignore]'):
                skip = False
                continue
            elif skip:
                compiled_markdown += line
                continue

            parsed = line
            for parser in self.parsers + self._default_parsers:
                parsed = parser(self, parsed)

            compiled_markdown += parsed
        return compiled_markdown

    def _create_folder_structure(self, cwd):
        os.makedirs(cwd, exist_ok=True)

        for root, dirs, files in os.walk(self.docs_folder):
            for dir in dirs:
                path = f'{cwd}/{root.replace(self.docs_folder, "")}/{dir}'
                os.makedirs(path, exist_ok=True)

    def generate(self):
        self._create_folder_structure(self._get_compiled_docs_path())

        for root, dirs, files in os.walk(self.docs_folder):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith('.md'):
                    with open(path) as f:
                        lines = f.readlines()
                    path = path.replace(self.docs_folder, '')
                    path = self._get_compiled_docs_path(path)
                    with open(path, 'w') as f:
                        f.write(self._compile_lines(lines))
                else:
                    os.system(f'cp {path} {self._get_compiled_docs_path()}/{root.replace(self.docs_folder, "")}')


class MultiOutputDocGenerator(DocGenerator):
    def __init__(self, docs_folder, compiled_docs_folder, output_folders):
        super().__init__(docs_folder, compiled_docs_folder)
        self.output_folders = output_folders

    def _clean_lines(self, lines, output_folder):
        ''' Removes block [only <dir>] ... [endonly] if dir != output_folder '''

        clean_lines = []
        skip = False
        for line in lines:
            if line.startswith('[only'):
                if output_folder not in line:
                    skip = True
            elif line.startswith('[endonly]'):
                skip = False
            elif not skip:
                clean_lines.append(line)
        return clean_lines

    def generate(self):
        for output_folder in self.output_folders:
            compiled_docs_path = f'{self._get_compiled_docs_path()}/{output_folder}'
            self._create_folder_structure(compiled_docs_path)

            for root, dirs, files in os.walk(self.docs_folder):
                for file in files:
                    path = os.path.join(root, file)
                    if file.endswith('.md'):
                        with open(path) as f:
                            lines = f.readlines()

                        path = path.replace(self.docs_folder, '')
                        path = f'{output_folder}/{path}'
                        path = self._get_compiled_docs_path(path)
                        with open(path, 'w') as f:
                            clean_lines = self._clean_lines(lines, output_folder)
                            compiled_lines = self._compile_lines(clean_lines)
                            f.write(self._compile_lines(compiled_lines))
                    else:
                        os.system(f'cp {path} {compiled_docs_path}/{root.replace(self.docs_folder, "")}')


if __name__ == '__main__':
    generator = DocGenerator('docs', 'docs_compiled')
    generator.image_folder = 'images'
    generator.generate()
