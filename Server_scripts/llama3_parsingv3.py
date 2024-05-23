import json
import requests

def send_api_request(reference):
    url = "http://localhost:11434/api/generate"
    prompt_text = (
        "Parse the following reference into a metadata table with the specified columns:\n"
        "1. Authors: Each author is listed in separate columns.\n"
        "2. Year: Represents the year of publication.\n"
        "3. Title: The title of the article.\n"
        "4. Journal/Book Name: Provides full names of the journals or book.\n"
        "5. Volume/Issue: These details are listed without abbreviations.\n"
        "6. Page Range: Specifies the range of pages the article covers.\n"
        "7. Location: Add a location if applicable.\n\n"
        "Reference:\n"
        f"{reference}\n\n"
        "Combine all references into a single markdown table with the following header and format:\n"
        "| Authors | Year | Title | Journal/Book Name | Volume/Issue | Page Range | Location |\n"
        "| --- | --- | --- | --- | --- | --- | --- |"
    )

    prompt = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }
    response = requests.post(url, json=prompt)
    return response.json()

def process_references(references):
    reference_list = references.split("\n")
    metadata_tables = []

    for reference in reference_list:
        try:
            json_response = send_api_request(reference)
            if "response" in json_response:
                metadata_tables.append(json_response["response"])
            else:
                print(f"Error: No 'response' key in JSON response for reference: {reference}")
        except Exception as e:
            print(f"Error processing reference: {reference}", e)
    
    return "\n".join(metadata_tables)

def main():
    with open("references.txt", "r") as file:
        references = file.read().strip()
    
    header = (
        "| Authors | Year | Title | Journal/Book Name | Volume/Issue | Page Range | Location |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
    )

    metadata_table = process_references(references)
    
    print("Metadata Table:")
    print(header + metadata_table)
    
    with open("output.txt", "w") as file:
        file.write(header + metadata_table)

if __name__ == "__main__":
    main()
