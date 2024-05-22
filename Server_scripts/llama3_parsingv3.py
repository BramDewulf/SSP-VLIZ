import json
import requests

def send_api_request(references, first_batch=False):
    url = "http://localhost:11436/api/generate"
    if first_batch:
        prompt_text = (
            "Parse the following references into a single metadata table with the specified columns:\n"
            "1. Authors: Each author is listed in separate columns.\n"
            "2. Year: Represents the year of publication.\n"
            "3. Title: The title of the article.\n"
            "4. Journal/Book Name: Provides full names of the journals or book.\n"
            "5. Volume/Issue: These details are listed without abbreviations.\n"
            "6. Page Range: Specifies the range of pages the article covers.\n\n"
            "References:\n"
            f"{references}\n\n"
            "Combine all references into a single markdown table without repeating the headers. Do not number the references."
        )
    else:
        prompt_text = (
            "Continue parsing these next references into the existing metadata table (use the standard headers: Authors, Year, Title, Journal/Book Name, Volume/Issue, Page range), using the same matrix format with metadata fields split by vertical lines. Do not number the references in the table and dont add any columns and most importantly do not abbreviate any metadata! (If no data is found just leave the field empty):\n\n"
            f"{references}\n\n"
        )
    prompt = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }
    response = requests.post(url, json=prompt)
    return response.json()

def process_references_one_by_one(references):
    reference_list = references.split("\n")
    all_metadata_tables = []

    for reference in reference_list:
        try:
            json_response = send_api_request(reference, first_batch=True)
            if "response" in json_response:
                all_metadata_tables.append(json_response["response"])
            else:
                print("Error: No 'response' key in JSON response for reference:", reference)
        except Exception as e:
            print("Error processing reference:", reference, "-", e)
    
    # Combine all the metadata tables
    combined_metadata_table = "\n".join(all_metadata_tables)
    return combined_metadata_table

def main():
    with open("references.txt", "r") as file:
        references = file.read().strip()
    
    metadata_table = process_references_one_by_one(references)
    
    print("Metadata Table:")
    print(metadata_table)
    
    with open("output.txt", "w") as file:
        for line in metadata_table.split('\n'):
            if line.startswith('|'):
                file.write(line + '\n')

if __name__ == "__main__":
    main()