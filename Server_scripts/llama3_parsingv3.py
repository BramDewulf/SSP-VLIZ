import json
import requests

def send_api_request(references):
    url = "http://localhost:11436/api/generate"
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
        "Combine all references into a single markdown table without repeating the headers."
    )
    prompt = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }
    response = requests.post(url, json=prompt)
    return response.json()

def process_references_in_batches(references, batch_size=10):
    reference_list = references.split("\n\n")
    total_references = len(reference_list)
    metadata_table = ""
    
    for i in range(0, total_references, batch_size):
        batch_references = "\n\n".join(reference_list[i:i + batch_size])
        try:
            json_response = send_api_request(batch_references)
            if "response" in json_response:
                metadata_table += json_response["response"] + "\n"
            else:
                print(f"Error: No 'response' key in JSON response for batch {i // batch_size + 1}")
        except Exception as e:
            print(f"Error processing batch {i // batch_size + 1}:", e)
    
    return metadata_table

def main():
    with open("references.txt", "r") as file:
        references = file.read().strip()
    
    metadata_table = process_references_in_batches(references)
    
    print("Metadata Table:")
    print(metadata_table)
    
    with open("output.txt", "w") as file:
        file.write(metadata_table)

if __name__ == "__main__":
    main()
