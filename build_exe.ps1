nuitka --standalone --onefile --follow-imports --windows-disable-console --enable-plugin=pyqt6 --enable-plugin=anti-bloat --show-anti-bloat-changes --noinclude-setuptools-mode=nofollow --noinclude-pytest-mode=nofollow --noinclude-unittest-mode=nofollow --noinclude-IPython-mode=nofollow --remove-output --include-data-dir=ui=ui --include-data-dir=logic=logic --include-data-dir=database=database --include-data-files=absolutePath.py=absolutePath.py --noinclude-data-files=*.ui --output-dir=build --windows-icon-from-ico=ui/resources/ControlMicTray.ico -o ControlMicTray.exe main.py