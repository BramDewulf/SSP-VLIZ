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
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        "Do not number the references. Do not add any extra columns or information. Adhere strictly to the format and instructions provided."
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
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        return None

def main():
    while True:
        reference = input("Enter the reference to parse (or type 'stop' to exit):\n")
        
        if reference.strip().lower() == "stop":
            print("Exiting...")
            break
        
        if not reference.strip():
            print("Error: Reference input cannot be empty.")
            continue
        
        json_response = send_api_request(reference)
        if json_response is None:
            print("Error: No valid response received from the API.")
            continue
        
        if "response" in json_response:
            metadata_table = json_response["response"]
            lines = metadata_table.split('\n')
            for line in lines:
                if line.startswith('|'):
                    print(line)
        else:
            print("Error: No 'response' key in JSON response.")

if __name__ == "__main__":
    main()
