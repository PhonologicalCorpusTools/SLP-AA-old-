import sys
import os
import PyQt5
from cx_Freeze import setup, Executable

def readme():
    with open('README.md') as f:
        return f.read()

base = None
incl_files = ['media']
if sys.platform == "win32":
    base = "Win32GUI"
    libegl = os.path.join(os.path.dirname(PyQt5.__file__),'libEGL.dll')
    incl_files.append((libegl,os.path.split(libegl)[1]))

group_name = 'Sign Language Phonetics'

exe_name = 'SLP-Annotator'

shortcut_table = [
    ("StartMenuShortcut",       # Shortcut
     "ProgramMenuFolder",       # Directory_
     "%s" % (exe_name,),        # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]slpa.exe",     # Target
     None,                      # Arguments
     None,                      # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     'TARGETDIR'                # WkDir
     )
    ]

build_exe_options = {"excludes": [
                        'matplotlib',
                        "tcl",
                        'ttk',
                        "tkinter",],
                    "include_files":incl_files,
                    "includes": [
                            "PyQt5",
##                            "PyQt5.QtWebKitWidgets",
##                            "PyQt5.QtWebKit",
##                            "PyQt5.QtPrintSupport",
                            "PyQt5.QtMultimedia",
                            "sys", "anytree"]
                            }

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
        #'upgrade_code':'{9f3fd2c0-db11-4d9b-8124-2e91e6cfd19d}',
        'add_to_path': False,
        'initial_target_dir': r'[ProgramFiles64Folder]\%s\%s' % (group_name, exe_name),
        'data':msi_data}

bdist_mac_options = {#'iconfile':'media/slpa_icon.ico',
                    'qt_menu_nib':'/opt/local/share/qt5/plugins/platforms',
                    'bundle_name':'Sign Language Phonetic Annotator',
                    #'include_frameworks':["/Library/Frameworks/Tcl.framework",
                    #                    "/Library/Frameworks/Tk.framework"]
                                        }
bdist_dmg_options = {'applications_shortcut':True}

setup(name='Sign Language Phonetic Annotator',
      version='0.1',
      description='',
      long_description='',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='phonology corpus phonetics sign language',
      url='https://github.com/PhonologicalCorpusTools/SLP-Annotator',
      author='UBC Phonology Group',
      author_email='kathleen.hall@ubc.ca',
##      packages = ['slpa'],
      executables = [Executable('run_slpa.py',
                            base=base,
                            #shortcutDir=r'[StartMenuFolder]\%s' % group_name,
                            #shortcutName=exe_name,
                            #icon='docs/images/favicon.png'
                            )],
      options={
          'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options,
          'bdist_mac':bdist_mac_options,
          'bdist_dmg':bdist_dmg_options}
      )
