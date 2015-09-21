from distutils.core import setup  
import py2exe  
import sys

includes = ["encodings", "encodings.*", "sip", "PyQt4"]
sys.argv.append("py2exe")  
options = {"py2exe":
               {
                   "bundle_files": 1,
                   "dll_excludes":["MSVCP90.dll"],
                   "compressed": 1,
                   "optimize": 2,
                   "includes": includes,
               }
}
setup(options = options,  
      zipfile=None,   
      windows = [
          {
              "script":'gui_main.py',
              "uac_info": "requireAdministrator"
          }
      ])