#based on https://gist.github.com/ndunn219/62263ce1fb59fda08656be7369ce329b

import re, sys

class SRTParser(object):
    @staticmethod
    def extractTextFromSRT(fileSRT):
        file_name = fileSRT
        file_encoding = 'utf-8'

        #loop through the lines for parsing
        with open(file_name, encoding=file_encoding, errors='replace') as f:
            lines = f.readlines()
            new_lines = SRTParser.clean_up(lines)
            new_file_name = file_name[:-4] + '.txt'

        #write parsed txt file
        with open(new_file_name, 'w') as f:
            for line in new_lines:
                f.write(line)

    @staticmethod
    def clean_up(lines):
        regexSubtitleIndexNumber = re.compile("[0-9]+")

        new_lines = []
        for line in lines[1:]:
            #if line empty or
            #if line contains --> or
            #if line matches the subtitle index regex
            #then skip line
            if (not line or not line.strip()) or ("-->" in line) or regexSubtitleIndexNumber.match(line):
                continue
            else:
                #append line
                new_lines.append(line)
        return new_lines
