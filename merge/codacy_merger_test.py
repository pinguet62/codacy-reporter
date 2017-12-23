import json
import unittest

import codacy_merger


class LcovTestCase(unittest.TestCase):
    def test_convert(self):
        with open('../jacoco/generator/target/site/jacoco/codacy.json') as file: jacoco = file.read()
        with open('../lcov/generator/coverage/codacy.json') as file: lcov = file.read()

        result = codacy_merger.merge([jacoco, lcov])
        result = json.loads(result)

        with open('expected.json') as file: expected = file.read()
        expected = json.loads(expected)

        self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(expected, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
