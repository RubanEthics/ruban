#!/bin/bash

# Target URL
TARGET="http://node-admin.webnexs.org"

# Step 1: Find all JS files (especially bundle files)
echo "[*] Fetching index.html..."
wget -q -O index.html "$TARGET"

JS_FILES=$(grep -oP 'src="[^"]+\.js"' index.html | cut -d'"' -f2)

echo "[*] Found JS files:"
echo "$JS_FILES"
echo

# Step 2: Download and scan JS files for interesting paths
for JS in $JS_FILES; do
    FULL_URL="$TARGET$JS"
    echo "[*] Scanning $FULL_URL"
    
    curl -s "$FULL_URL" | \
        grep -oP '\/[a-zA-Z0-9\-_\/]{3,}' | \
        sort -u | \
        grep -vE '\.(js|css|png|jpg|ico)$'
        
    echo
done