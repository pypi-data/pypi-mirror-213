#!/usr/bin/env bash

pylupdate6 --verbose --ts emid_en_GB.ts --ts emid_es.ts --ts emid_fr.ts --ts emid_it.ts ../emid/__main__.py ../emid/audio_manager.py ../emid/dialog_edit_phones.py ../emid/dialog_edit_preferences.py ../emid/global_parameters.py ../emid/sndlib.py



lrelease -verbose emid.pro

mv *.qm ../translations/

rcc -g python ../resources.qrc | sed '0,/PySide2/s//PyQt6/' > ../emid/qrc_resources.py
