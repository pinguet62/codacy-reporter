import argparse
import json
import os


# https://github.com/codacy/node-codacy-coverage/blob/master/lib/impl/lcov.js

def convert(lcov, basedir):
    lines = lcov.splitlines()

    codacy = {}

    # codacy['language'] = 'JavaScript'

    totalFounds = 0
    totalHits = 0

    codacyFileReports = []
    codacyFileReport = None
    for line in lines:
        if line.startswith('TN:'):
            codacyFileReport = {'coverage': {}}
        if line.startswith('SF:'):
            filename = line[3:]
            codacyFileReport['filename'] = os.path.relpath(filename, basedir).replace('\\', '/')
        if line.startswith('DA:'):
            (lineIndex, count) = line[3:].split(',')
            codacyFileReport['coverage'][int(lineIndex)] = int(count)
        if line.startswith('LF:'):
            lineFounds = int(line[3:])
            totalFounds += lineFounds
        if line.startswith('LH:'):
            lineHits = int(line[3:])
            totalHits += lineHits
        if line == 'end_of_record':
            codacyFileReport['total'] = int(100 * lineHits / lineFounds)
            codacyFileReports.append(codacyFileReport)
    codacy['fileReports'] = codacyFileReports

    codacy['total'] = int(100 * totalHits / totalFounds)

    return json.dumps(codacy, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert LCOV report file to Codacy model')
    parser.add_argument('--basedir', type=str, help='Path to source folder (ex: "sub/module")')
    parser.add_argument('file', type=argparse.FileType('r'), help='The LCOV input file')
    args = parser.parse_args()

    print(convert(args.file.read(), args.basedir))
