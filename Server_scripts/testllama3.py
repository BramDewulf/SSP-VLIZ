import requests

def send_api_request(references):
    url = "http://localhost:11436/api/generate"
    prompt = {"model": "llama3", "prompt": references, "stream": False}
    response = requests.post(url, json=prompt)
    print("API Response:")
    print(response.text)
    return response.json()

def main():
    with open("references.txt", "r") as file:
        references = file.read()
    try:
        response = send_api_request(references)
        metadata_table = response["text"]
        print("Metadata Table:")
        print(metadata_table)
        with open("output.txt", "w") as file:
            file.write(metadata_table)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
