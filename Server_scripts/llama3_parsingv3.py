import json
import requests

def send_api_request(references):
    url = "http://localhost:11434/api/generate"
    prompt_text = (
        "Parse the following references into a metadata table with the specified columns:\n"
        "1. Authors: Each author is listed in separate columns.\n"
        "2. Year: Represents the year of publication.\n"
        "3. Title: The title of the article.\n"
        "4. Journal/Book Name: Provides full names of the journals or book.\n"
        "5. Volume/Issue: These details are listed without abbreviations.\n"
        "6. Page Range: Specifies the range of pages the article covers.\n"
        "7. Location: Add a location if applicable.\n\n"
        "References:\n"
        f"{references}\n\n"
        "Combine all references into a single markdown table with the following header and format:\n"
        "| Authors | Year | Title | Journal/Book Name | Volume/Issue | Page Range | Location |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        "Do not number the references. Do not add any extra columns or information. Adhere strictly to the format and instructions provided."
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

    for i in range(0, total_references, batch_size):
        batch_references = "\n".join(reference_list[i:i + batch_size])
        try:
            json_response = send_api_request(batch_references)
            if "response" in json_response:
                all_metadata_tables.append(json_response["response"])
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
        lines = metadata_table.split('\n')
        for i, line in enumerate(lines):
            if i == 0 or (line and not line.startswith('| --- ') and not line.startswith('| Authors |')):
                file.write(line + '\n')

if __name__ == "__main__":
    main()
