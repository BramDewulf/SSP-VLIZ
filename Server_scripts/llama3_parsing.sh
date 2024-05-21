#!/bin/bash

# Define the API endpoint
url="http://localhost:11436/api/generate"

# Function to send API request for each reference
send_api_request() {
    reference="$1"
    prompt="Please parse the following reference into a metadata table according to the provided matrix format: $reference **Metadata Table:** | Field | Value | |---------------------|------------------------------------------| | Author>"
    # Send API request and extract the response content after "response":""
    response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"model\": \"llama3\", \"prompt\": \"$prompt\"}" "$url" | grep -oP '(?<="response":").*')
    echo "$response"
}

# File path containing references
file_path="$1"

# Read references from the file
read_references() {
    cat "$file_path"
}

# Iterate over each reference and send API request
references=$(read_references)
while IFS= read -r reference; do
    send_api_request "$(echo "$reference" | tr -d '\n')"
done <<< "$references"

