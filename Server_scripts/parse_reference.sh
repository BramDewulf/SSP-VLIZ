#!/bin/bash

# Prompt the user to input the reference
read -p "Enter the reference: " reference

# Construct the curl command
curl -X POST -d "{
    \"model\": \"llama3\",
    \"prompt\": \"Please parse the following reference into a metadata table:\\n\\n**Reference:**\\n$reference\\n\\n**Metadata Table:**\\n| Field               | Value                                    |\\n|---------------------|------------------------------------------|\\n| Authors             |                                          |\\n| Year                |                                          |\\n| Abbreviated Title   |                                          |\\n| Journal Abbrev.     |                                          |\\n| Full Journal Name   |                                          |\\n| Volume/Issue        |                                          |\\n| Page Range          |                                          |\\n| Location            |                                          |\\n| Taxonomic Names     |                                          |\"
}" http://localhost:11436/api/generate


