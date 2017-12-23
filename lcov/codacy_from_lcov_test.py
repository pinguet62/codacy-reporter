import json
import unittest

import codacy_from_lcov


class LcovTestCase(unittest.TestCase):
    def test_convert(self):
        with open('generator/coverage/lcov.info') as file: lcov = file.read()
        basedir = 'generator'

        result = codacy_from_lcov.convert(lcov, basedir)
        result = json.loads(result)

        with open('generator/coverage/codacy.json') as file: expected = file.read()
        expected = json.loads(expected)

        self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(expected, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
