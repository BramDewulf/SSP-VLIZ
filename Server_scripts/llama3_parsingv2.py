import json
import requests

def send_api_request(references):
    url = "http://localhost:11436/api/generate"
    # Define the metadata format instruction within the prompt
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

def main():
    with open("references.txt", "r") as file:
        references = file.read().strip()
    try:
        json_response = send_api_request(references)
        print("API Response:")
        print(json_response)  # Print the raw API response for debugging
        if "response" in json_response:
            metadata_table = json_response["response"]
            print("Metadata Table:")
            print(metadata_table)
            with open("output.txt", "w") as file:
                file.write(metadata_table)
        else:
            print("Error: No 'response' key in JSON response")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
