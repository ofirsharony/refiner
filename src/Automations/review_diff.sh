#!/bin/bash

# This script takes the selected text of any app and opens it in the refiner app, to review the suggested changes.
# To activate, open automator and choose 'quick action'. add a new 'run shell script' and select 'receive current text' in 'any application'.
# Do not select 'output replaces selected text': this script prints nothing, so the selection would be deleted.
# The shell should be /bin/bash and the 'Pass input as arguments' should be checked.
# Save as 'Refiner_UI'
# In your mac 'keyboard shortcuts', choose services -> text -> type a new shortcut to 'Refiner_UI'

selected_text="$1"

# Give the text to Python as an argument, not inside the code, so quotes and backslashes are safe.
encoded_text=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$selected_text")

open "http://localhost:8504/?auto_generate=true&text=${encoded_text}"
