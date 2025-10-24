#!/bin/bash

# This script takes the selected text of any app and sends it to refiner API, replacing the input 'in place'
# To activate, open automator and choose 'quick action'. add a new 'run shell script' and select receive 'current text' in 'any application'. 
# choose 'Output replaces selected text'.
# The shell should be /bin/bash and the 'Pass input as arguments' should be checked.
# Save as 'Refiner_Replace'
# In your mac 'keyboard shortcuts', choose services -> text -> type a new shortcut to 'Refiner_Replace'

# Get the selected text passed as a parameter to the script
selected_text="$1"

# Encode the selected text for URL
encoded_text=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$selected_text'''))")

# Invoke the API
response=$(curl --max-time 4 -s "http://localhost:8005/generate_get?text=${encoded_text}")

# Remove leading and trailing quotes
cleaned_response=$(echo $response | sed 's/^"//; s/"$//')

# Replace \n with actual newlines
final_response=$(echo -e "$cleaned_response")

echo "$final_response"