import argparse
import json


def merge(codacys):
    mergedCodacy = {}

    totalFounds = 0
    totalHits = 0

    mergedCodacyFileReports = []
    for codacy in codacys:
        codacy = json.loads(codacy)

        hits = getCoveredLineCount(codacy)
        founds = int(100 * hits / codacy['total'])

        totalHits += hits
        totalFounds += founds

        mergedCodacyFileReports.extend(codacy['fileReports'])
    mergedCodacy['fileReports'] = mergedCodacyFileReports

    mergedCodacy['total'] = int(100 * totalHits / totalFounds)

    return json.dumps(mergedCodacy, indent=4)


def getCoveredLineCount(codacy):
    count = 0
    for fileReport in codacy['fileReports']:
        for hint in fileReport['coverage'].values():
            count += (1 if hint > 0 else 0)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Codacy report files')
    parser.add_argument('files', type=argparse.FileType('r'), nargs='*', help='The Codacy input file')
    args = parser.parse_args()

    print(merge([file.read() for file in args.files]))
