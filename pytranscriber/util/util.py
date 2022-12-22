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

import platform
import os
import subprocess
import requests
import re
from pathlib import PureWindowsPath
from urllib.parse import urlparse



class MyUtil(object):
    @staticmethod
    def open_file(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    @staticmethod
    def is_internet_connected(proxies=None):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            res = requests.get('https://www.google.com', timeout=2,proxies=proxies)
            if res.status_code != 200:
                return False
            else:
                return True
        except OSError:
            pass
        return False

    @staticmethod
    def percentage(currentval, maxval):
        return 100 * currentval / float(maxval)

    @staticmethod
    def extract_tmp_root(path_code_file):
        
        # for Unixes
        if os.name != 'nt':
            regex = "\S+/onefile_[0-9_]*/"
            tmp_root_found = re.findall(regex, path_code_file)  
            #extract root tmp dir from code path  
            return tmp_root_found[0]
        # for Windows
        else:
            regex = "\S+/ONEFIL[~0-9_]*/"
            # converts the Windows Path to uri to use the same regular expression as in Unixes
            win_path = PureWindowsPath(path_code_file)
            uri_path = win_path.as_uri()
            
            tmp_root_found = re.findall(regex, uri_path)
            # after finding the regular expression on the uri converts back to python path
            py_path = urlparse(tmp_root_found[0]).path
            
            return os.path.normpath(py_path)