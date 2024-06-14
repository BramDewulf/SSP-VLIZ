# Conversion script used to convert GROBID XML output to CSV format to test quality of GROBID in Excel (version 1)

import csv
import os
import xml.etree.ElementTree as ET

### Reads from folder with xml files
def extract_bibliographic_data(xml_string):
    root = ET.fromstring(xml_string)
    
    # Extract analytic title
    analytic_title_element = root.find("./analytic/title[@type='main']")
    analytic_title = analytic_title_element.text if analytic_title_element is not None else ""
    
    # Extract monogr title
    monogr_title_element = root.find("./monogr/title[@level='m']")
    monogr_title = monogr_title_element.text if monogr_title_element is not None else ""
    
    # Select longest as title
    if len(analytic_title) > len(monogr_title):
        title = analytic_title
    else:
        title = monogr_title
    
    # Extract authors/editors
    author_elements = root.findall("./analytic/author/persName") + root.findall("./monogr/author/persName") + root.findall("./monogr/editor/persName")
    authors = []
    for author_element in author_elements:
        full_name = " ".join([name.text for name in author_element.findall("./*")])
        authors.append(full_name)
    
    # Extract journal title
    journal_title_element = root.find(".//monogr/title[@level='j']")
    journal_title = journal_title_element.text if journal_title_element is not None else ""

    # Extract other metadata
    volume = root.find("./monogr/imprint/biblScope[@unit='volume']").text if root.find("./monogr/imprint/biblScope[@unit='volume']") is not None else ""
    issue = root.find("./monogr/imprint/biblScope[@unit='issue']").text if root.find("./monogr/imprint/biblScope[@unit='issue']") is not None else ""
    page_from = root.find("./monogr/imprint/biblScope[@unit='page']").attrib.get('from') if root.find("./monogr/imprint/biblScope[@unit='page']") is not None else ""
    page_to = root.find("./monogr/imprint/biblScope[@unit='page']").attrib.get('to') if root.find("./monogr/imprint/biblScope[@unit='page']") is not None else ""
    publication_year = root.find("./monogr/imprint/date[@type='published']").attrib.get('when') if root.find("./monogr/imprint/date[@type='published']") is not None else ""
    
    # Combine data
    data = [title, ", ".join(authors), journal_title, volume, issue, page_from, page_to, publication_year]
    
    return data

    # append to existing csv, create csv file if none found
def append_to_csv(data, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def process_xml_files(folder_path, output_filename):
    header_written = False
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                xml_string = file.read()
                data = extract_bibliographic_data(xml_string)
                if not header_written:
                    header = ['Title', 'Authors', 'Journal Title','Volume','Issue Number', 'Page From', 'Page To', 'Publication Year']
                    append_to_csv(header, output_filename)
                    header_written = True
                append_to_csv(data, output_filename)

# Folder containing the XML files
input_folder = r'C:\Project\Project testing\xml_files'


# CSV file output
output_csv_file = 'converted_grobid.csv'

# Process XML files and write to CSV
process_xml_files(input_folder, output_csv_file)




