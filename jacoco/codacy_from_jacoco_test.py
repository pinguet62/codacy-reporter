import json
import unittest

import codacy_from_jacoco


class JacocoTestCase(unittest.TestCase):
    def test_convert(self):
        with open('generator/target/site/jacoco/jacoco.xml') as file: jacoco = file.read()
        prefix = 'src/main/java/'

        result = codacy_from_jacoco.convert(jacoco, prefix)
        result = json.loads(result)

        with open('generator/target/site/jacoco/codacy.json') as file: expected = file.read()
        expected = json.loads(expected)

        self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(expected, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
