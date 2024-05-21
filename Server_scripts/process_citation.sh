#!/bin/bash

# Check if correct number of arguments provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

input_file="$1"
output_file="$2"

# Function to send citation to API and append response to output file
send_citation_to_api() {
    citation="$1"
    api_response=$(curl --location 'http://llama3.vliz.be:8070/api/processCitation' \
                        --header 'Content-Type: application/x-www-form-urlencoded' \
                        --data-urlencode "citations=$citation")
    echo "$api_response" >> "$output_file"
}

# Ensure output file is empty before starting
> "$output_file"

# Write root tags to output file
echo "<root>" >> "$output_file"

# Read each line from input file and send citation to API
while IFS= read -r citation; do
    send_citation_to_api "$citation"
done < "$input_file"

# Write closing root tag to output file
echo "</root>" >> "$output_file"

