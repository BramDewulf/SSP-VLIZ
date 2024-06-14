# Conversion script used to convert GROBID XML output to CSV format to test quality of GROBID in Excel (version 2)

import os
import csv
import xml.etree.ElementTree as ET

### from GROBID PDF ouput, 1 xml file)
def extract_data_from_xml(xml_file):
    try:
        # Parse XML
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define namespace map
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        # Extract bibliographic information
        bibliographic_data = []

        for biblStruct in root.findall('.//tei:biblStruct', ns):
            data = {}

            # Extract information from analytic element if present
            analytic = biblStruct.find('tei:analytic', ns)
            if analytic is not None:
                title_analytic = analytic.find('tei:title[@level="a"]', ns)
                if title_analytic is not None and title_analytic.text and title_analytic.text.strip():
                    data['title'] = title_analytic.text.strip()
                title_journal_analytic = analytic.find('tei:title[@level="j"]', ns)
                if title_journal_analytic is not None and title_journal_analytic.text and title_journal_analytic.text.strip():
                    data['journal'] = title_journal_analytic.text.strip()
                author_names_analytic = []
                for author in analytic.findall('tei:author/tei:persName', ns):
                    forename = author.find('tei:forename[@type="first"]', ns)
                    surname = author.find('tei:surname', ns)
                    if forename is not None and surname is not None:
                        author_names_analytic.append(f"{forename.text} {surname.text}")
                if author_names_analytic:
                    data['authors'] = ', '.join(author_names_analytic)

            # Extract information from monogr element
            monogr = biblStruct.find('tei:monogr', ns)
            if monogr is not None:
                title_monogr = monogr.find('tei:title[@level="m"]', ns)
                if title_monogr is not None and title_monogr.text and title_monogr.text.strip():
                    data['title'] = title_monogr.text.strip()
                journal_title = monogr.find('tei:title[@level="j"]', ns)
                if journal_title is not None and journal_title.text and journal_title.text.strip():
                    data['journal'] = journal_title.text.strip()
                author_names_monogr = []
                for author in monogr.findall('tei:author/tei:persName', ns):
                    forename = author.find('tei:forename[@type="first"]', ns)
                    middle_name = author.find('tei:forename[@type="middle"]', ns)
                    surname = author.find('tei:surname', ns)
                    full_name = ' '.join([name.text for name in [forename, middle_name, surname] if name is not None])
                    if full_name:
                        author_names_monogr.append(full_name)
                if author_names_monogr:
                    data['authors'] = ', '.join(author_names_monogr)
                date = monogr.find('tei:imprint/tei:date[@type="published"]', ns)
                if date is not None:
                    data['year'] = date.attrib.get('when', '')
                biblScope_page = monogr.find('tei:imprint/tei:biblScope[@unit="page"]', ns)
                if biblScope_page is not None:
                    from_page = biblScope_page.attrib.get('from', '')
                    to_page = biblScope_page.attrib.get('to', '')
                    if from_page and to_page:
                        data['page'] = f"{from_page}-{to_page}"
                    elif from_page:
                        data['page'] = from_page
                biblScope_volume = monogr.find('tei:imprint/tei:biblScope[@unit="volume"]', ns)
                if biblScope_volume is not None and biblScope_volume.text:
                    data['volume'] = biblScope_volume.text.strip()
                note = biblStruct.find('tei:note', ns)
                if note is not None and note.text:
                    data['notes'] = note.text.strip()

            # Merge data from analytic and monogr, prioritizing monogr
            merged_data = {**data}

            if analytic is not None:
                merged_data.update({key: value for key, value in data.items() if key not in merged_data})

            bibliographic_data.append(merged_data)
    except ET.ParseError as e:
        print(f"Error parsing XML file '{xml_file}': {e}")

    return bibliographic_data

def write_data_to_csv(data, output_csv):
    # Write data to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'journal', 'page', 'volume', 'year', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

# Fill in target input and output:
input_xml_folder = r'C:\Project\hard_queries_output.xml'
output_csv = 'hard_queries_ouput.csv'

bibliographic_data = extract_data_from_xml(input_xml_folder)
write_data_to_csv(bibliographic_data, output_csv)
