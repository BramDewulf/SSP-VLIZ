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
            "4. Journal Name: Provides full names of the journals.\n"
            "5. Volume/Issue: These details are listed without abbreviations.\n"
            "6. Page Range: Specifies the range of pages the article covers.\n\n"
            "References:\n"
            f"{references}\n\n"
            "Combine all references into a single markdown table without repeating the headers. Do not number the references."
        )
    else:
        prompt_text = (
            "Continue parsing these next references into the existing metadata table with the specified columns (Author, Year, Title, Journal name, Volume/Issue, Page range), using the same matrix format please and keep the same layout using | to split columns. Do not number the references in the table and dont add any columns:\n\n"
            f"{references}\n\n"
        )
    prompt = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }
    response = requests.post(url, json=prompt)
    return response.json()

def process_references_in_batches(references, batch_size=5):
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
    
    return all_metadata_tables

def extract_metadata_tables(metadata_tables):
    extracted_tables = []
    for table in metadata_tables:
        matches = re.findall(r'\|.*?\|', table, re.DOTALL)
        if matches:
            extracted_tables.append("".join(matches))
    return extracted_tables

def write_metadata_tables_to_file(metadata_tables, output_file):
    with open(output_file, "w") as file:
        for table in metadata_tables:
            file.write(table + "\n\n")

def main():
    with open("references.txt", "r") as file:
        references = file.read().strip()
    
    metadata_tables = process_references_in_batches(references, batch_size=5)
    extracted_tables = extract_metadata_tables(metadata_tables)
    
    if extracted_tables:
        write_metadata_tables_to_file(extracted_tables, "output.txt")
        print("Output written to 'output.txt'")
    else:
        print("No metadata tables found to write.")

if __name__ == "__main__":
    main()