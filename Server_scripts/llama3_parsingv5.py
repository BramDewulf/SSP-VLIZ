# Script used to automate Llama3 requests to API endpoint
import json
import requests
import sys

def send_api_request(references):
    url = "http://localhost:11434/api/generate"
    references_text = "\n".join(references)
    prompt_text = (
        "Parse the following references into a metadata table with the specified columns:\n"
        "1. Authors: Each author is listed in separate columns.\n"
        "2. Year: Represents the year of publication.\n"
        "3. Title: The title of the article.\n"
        "4. Journal/Book Name: Provides full names of the journals or book.\n"
        "5. Volume/Issue: These details are listed without abbreviations.\n"
        "6. Page Range: Specifies the range of pages the article covers.\n"
        "7. Location: Add a location if applicable.\n\n"
        f"References:\n{references_text}\n\n"
        "Combine all references into a single markdown table with the following header and format:\n"
        "| Authors | Year | Title | Journal/Book Name | Volume/Issue | Page Range | Location |\n"
        "| --- | --- | --- | --- | --- | --- | --- |"
    )

    prompt = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }

    try:
        response = requests.post(url, json=prompt)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

def process_references(references):
    batch_size = 5
    metadata_tables = []

    for i in range(0, len(references), batch_size):
        batch = references[i:i+batch_size]
        json_response = send_api_request(batch)
        if json_response and "response" in json_response:
            metadata_tables.append(json_response["response"])
        else:
            print(f"Error: Invalid response for batch starting with reference: {batch[0]}")
    
    return "\n".join(metadata_tables)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py references.txt")
        return

    references_file = sys.argv[1]
    try:
        with open(references_file, "r") as file:
            references = file.read().strip().split("\n")
    except FileNotFoundError:
        print(f"Error: '{references_file}' file not found.")
        return

    header = (
        "| Authors | Year | Title | Journal/Book Name | Volume/Issue | Page Range | Location |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
    )

    metadata_table = process_references(references)
    
    filtered_table = "\n".join([line for line in metadata_table.split("\n") if line.startswith("|")])
    
    full_table = header + filtered_table
    print("Metadata Table:")
    print(full_table)
    
    with open("output.txt", "w") as file:
        file.write(full_table)

if __name__ == "__main__":
    main()
