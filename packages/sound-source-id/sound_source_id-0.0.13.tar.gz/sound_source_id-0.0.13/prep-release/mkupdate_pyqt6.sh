#!/usr/bin/env bash

pylupdate6 --verbose --ts sound_source_id_en_GB.ts --ts sound_source_id_es.ts --ts sound_source_id_fr.ts --ts sound_source_id_it.ts ../sound_source_id/__main__.py ../sound_source_id/audio_manager.py ../sound_source_id/dialog_edit_phones.py ../sound_source_id/dialog_edit_preferences.py ../sound_source_id/global_parameters.py ../sound_source_id/sndlib.py



lrelease -verbose sound_source_id.pro

mv *.qm ../translations/

rcc -g python ../resources.qrc | sed '0,/PySide2/s//PyQt6/' > ../sound_source_id/qrc_resources.py
