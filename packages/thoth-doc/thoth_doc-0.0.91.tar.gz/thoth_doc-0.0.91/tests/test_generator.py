from unittest import TestCase

from thoth_doc.main import DocGenerator


class DocGeneratorTestCase(TestCase):
    def test_generate(self):
        generator = DocGenerator('src/thoth_doc/docs', 'src/thoth_doc/docs_compiled')
        generator.generate()
