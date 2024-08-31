#!/bin/bash

# This script takes the selected text of any app and sends it to refiner
# To activate, open automator and choose 'quick action'. add a new 'run shell script' and select 'receive current text' in 'any application'. Save as 'Refiner'
# In your mac 'keyboard shortcuts', choose services -> text -> type a new shortcut to 'Refiner'

# Get the selected text passed as a parameter to the script
selected_text="$1"

# Encode the selected text for URL
encoded_text=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$selected_text'''))")

# Open the URL in the default browser with the selected text as a parameter
open "http://localhost:8501/?auto_generate=true&text=${encoded_text}"
