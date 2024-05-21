from grobid_client.grobid_client import GrobidClient

client = GrobidClient('https://kermitt2-grobid.hf.space/')
client.process("processReferences", r'C:\Project\Example_query10.pdf', n=20)