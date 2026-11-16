#!/bin/bash

# This script takes the selected text of any app and sends it to refiner API, replacing the input 'in place'
# To activate, open automator and choose 'quick action'. add a new 'run shell script' and select receive 'current text' in 'any application'.
# choose 'Output replaces selected text'.
# The shell should be /bin/bash and the 'Pass input as arguments' should be checked.
# Save as 'Refiner_Replace'
# In your mac 'keyboard shortcuts', choose services -> text -> type a new shortcut to 'Refiner_Replace'

selected_text="$1"

# curl URL-encodes the text itself, so quotes and other special characters are safe.
response=$(curl --max-time 8 -sf -G "http://localhost:8005/generate_get" --data-urlencode "text=${selected_text}")

# The API returns a JSON string. Decode it, so escapes like \" and \n become real characters.
refined=$(printf '%s' "$response" | python3 -c 'import json, sys; print(json.load(sys.stdin), end="")' 2>/dev/null)

# If the API is down, times out, or returns nothing, keep the original text. Automator replaces the selection with our output.
if [ -n "$refined" ]; then
  printf '%s' "$refined"
else
  printf '%s' "$selected_text"
fi
