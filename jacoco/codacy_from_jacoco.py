import argparse
import json
import xml.etree.ElementTree


# https://github.com/codacy/coverage-parser/blob/master/src/main/scala/com/codacy/parsers/implementation/JacocoParser.scala

def convert(jacoco, prefix):
    report = xml.etree.ElementTree.fromstring(jacoco)

    codacy = {}

    codacy['language'] = 'Java'

    lineCounterTotal = report.find('./counter[@type="LINE"]')
    coveredTotal = int(lineCounterTotal.get('covered'))
    missedTotal = int(lineCounterTotal.get('missed'))
    codacy['total'] = int((coveredTotal / (coveredTotal + missedTotal)) * 100)

    codacyFileReports = []
    for package in report.findall('./package'):
        for sourcefile in package.findall('sourcefile'):
            codacyFileReport = {}

            codacyFileReport['filename'] = prefix + package.get('name') + '/' + sourcefile.get('name')

            sourcefileCounter = sourcefile.find('./counter[@type="LINE"]')
            sourcefileCounterCovered = int(sourcefileCounter.get('covered'))
            sourcefileCounterMissed = int(sourcefileCounter.get('missed'))
            codacyFileReport['total'] = int((sourcefileCounterCovered / (sourcefileCounterCovered + sourcefileCounterMissed)) * 100)

            codacyCoverage = {}
            for line in sourcefile.findall('line'):
                lineMissedInstructions = int(line.get('mi'))
                lineCoveredInstructions = int(line.get('ci'))
                if lineMissedInstructions + lineCoveredInstructions > 0:
                    covered = 0 if lineCoveredInstructions == 0 else 1
                    if covered == 1:
                        codacyCoverage[line.get('nr')] = covered
            codacyFileReport['coverage'] = codacyCoverage

            codacyFileReports.append(codacyFileReport)
    codacy['fileReports'] = codacyFileReports

    return json.dumps(codacy, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert JaCoCo report file to Codacy model')
    parser.add_argument('--prefix', type=str, help='Prefix to add to classname (ex: "src/main/java/")')
    parser.add_argument('file', type=argparse.FileType('r'), help='The JaCoCo input file')
    args = parser.parse_args()

    print(convert(args.file.read(), args.prefix))
