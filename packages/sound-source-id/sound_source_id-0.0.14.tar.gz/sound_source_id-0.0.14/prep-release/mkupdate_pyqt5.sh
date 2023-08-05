#!/bin/sh

pyrcc5 -o ../sound_source_id/qrc_resources.py ../resources.qrc
pylupdate5 -verbose sound_source_id.pro
lrelease -verbose sound_source_id.pro

mv *.qm ../translations/
