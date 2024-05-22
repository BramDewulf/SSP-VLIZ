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

def process_references_in_batches(references, batch_size=1):
    reference_list = references.split("\n")
    total_references = len(reference_list)
    all_metadata_tables = []
    first_batch = True

    for i in range(0, total_references, batch_size):
        batch_references = "\n".join(reference_list[i:i + batch_size])
        try:
            json_response = send_api_request(batch_references, first_batch)
            if "response" in json_response:
                all_metadata_tables.append(json_response["response"])
                first_batch = False
            else:
                print(f"Error: No 'response' key in JSON response for batch {i // batch_size + 1}")
        except Exception as e:
            print(f"Error processing batch {i // batch_size + 1}:", e)
    
    # Combine all the metadata tables, ensuring the header is only included once
    if all_metadata_tables:
        combined_metadata_table = all_metadata_tables[0]
        for table in all_metadata_tables[1:]:
            combined_metadata_table += "\n" + "\n".join(table.split("\n")[1:])
        return combined_metadata_table
    else:
        return ""

def main():
    with open("references.txt", "r") as file:
        references = file.read().strip()
    
    metadata_table = process_references_in_batches(references, batch_size=5)
    
    print("Metadata Table:")
    print(metadata_table)
    
    with open("output.txt", "w") as file:
        for line in metadata_table.split('\n'):
            if line.startswith('|'):
                file.write(line + '\n')

if __name__ == "__main__":
    main()