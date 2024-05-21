import requests
import json

# Function to read references from a text file
def read_references_from_file(file_path):
    with open(file_path, 'r') as file:
        references = file.readlines()
    return references

# Function to send a single API request with all references combined
def send_api_request(references):
    url = 'http://localhost:11436/api/generate'
    
    # Construct the prompt with all references
    prompt = "Please parse the following references into a single metadata table according to the provided matrix format:\n\n**Raw References:**\n"
    for reference in references:
        prompt += f"{reference.strip()}\n"
    prompt += "\n**Metadata Table:**\n| Field               | Value                                    |\n|---------------------|------------------------------------------|"

    payload = {
        "model": "llama3",
        "prompt": prompt
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Main function
def main():
    file_path = 'references.txt'  # Replace with your file path
    references = read_references_from_file(file_path)
    
    # Send API request and get the response
    response = send_api_request(references)
    
    # Save the response to an output file
    with open('output.txt', 'w') as output_file:
        output_file.write(response.get('response', 'No response'))

    print("Processing complete. Metadata table saved to output.txt.")

if __name__ == "__main__":
    main()
