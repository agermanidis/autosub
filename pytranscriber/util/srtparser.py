'''
   (C) 2019 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

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
