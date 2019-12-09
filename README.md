# DMR ID lookup
A simple script to automatically populate DMR records of amateur radio operators using the RadioID.net API. Useful when using DSDPlus to monitor a DMR-MARC repeater.

Usage:
1. Copy `dmr_id_lookup.py` to the directory where DSDPlus is located
2. Run `python dmr_id_lookup.py`

Every time the script is run, it will create a copy of the current DSDPlus.radios file with the date and time prefixed so you can restore it if something goes horribly wrong. A log file (updated_records.log) is also created to make it easier to keep track of updated records.