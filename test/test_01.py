import unittest

import template


class TestTemplate(unittest.TestCase):
    def test_simplest(self):
        tmp = 'This test is ${great}'
        repl = {
            'great': 'brilliant'
        }
        res = template.replace_template_variables(tmp, repl)
        self.assertEqual(res, 'This test is brilliant', 'Variable should have been replaced')
