from distutils.core import setup  
import py2exe  
import sys

includes = ["encodings", "encodings.*", "sip", "Tkinter"]
sys.argv.append("py2exe")  
options = {"py2exe":
               {
                   "bundle_files": 3,
                   "dll_excludes":["MSVCP90.dll"],
                   "compressed": 1,
                   "optimize": 2,
               }
}
setup(options = options,  
      zipfile=None,   
      windows = [
          {
              "script":'main.py',
              "uac_info": "requireAdministrator"
          }
      ])