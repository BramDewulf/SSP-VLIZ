# Conversion script used to convert GROBID XML output to CSV format to test quality of GROBID in Excel (version 3)

import os
import csv
import xml.etree.ElementTree as ET
def extract_data_from_xml(xml_file):
    bibliographic_data = []
    try:
        # Parse XML
        tree = ET.parse(xml_file)
        # Define namespace map
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        # Extract bibliographic information from each biblStruct element
        for biblStruct in tree.findall('.//biblStruct'):
            data = {}
            # Extract information from analytic element
            analytic = biblStruct.find('analytic')
            if analytic is not None:
                title_analytic_a = analytic.find('title[@level="a"]')
                if title_analytic_a is not None and title_analytic_a.text:
                    data['title'] = title_analytic_a.text.strip()
                else:
                    data['title'] = ''  # Set title to empty string if no title found
                author_names = []
                for author in analytic.findall('author/persName'):
                    forename = author.find('forename[@type="first"]')
                    surname = author.find('surname')
                    if forename is not None and surname is not None:
                        author_names.append(f"{forename.text} {surname.text}")
                if author_names:
                    data['authors'] = ', '.join(author_names)
                else:
                    data['authors'] = ''  # Set authors to empty string if no authors found
            else:
                data['title'] = ''
                data['authors'] = ''
            # Extract information from monogr element
            monogr = biblStruct.find('monogr')
            if monogr is not None:
                title_monogr_m = monogr.find('title[@level="m"]')
                if title_monogr_m is not None and title_monogr_m.text:
                    data['title'] = title_monogr_m.text.strip()
                else:
                    if 'title' not in data:
                        data['title'] = ''  # Set title to empty string if no title found
                title_monogr_j = monogr.find('title[@level="j"]')
                if title_monogr_j is not None and title_monogr_j.text:
                    data['journal'] = title_monogr_j.text.strip()
                else:
                    data['journal'] = ''  # Set journal to empty string if no journal title found
                author_names_monogr = []
                for author in monogr.findall('author/persName'):
                    forename = author.find('forename[@type="first"]')
                    surname = author.find('surname')
                    if forename is not None and surname is not None:
                        author_names_monogr.append(f"{forename.text} {surname.text}")
                if author_names_monogr:
                    if 'authors' in data:
                        data['authors'] += ', ' + ', '.join(author_names_monogr)
                    else:
                        data['authors'] = ', '.join(author_names_monogr)
                else:
                    if 'authors' not in data:
                        data['authors'] = ''  # Set authors to empty string if no authors found
                biblScope_volume = monogr.find('imprint/biblScope[@unit="volume"]')
                if biblScope_volume is not None and biblScope_volume.text:
                    data['volume'] = biblScope_volume.text.strip()
                else:
                    data['volume'] = ''  # Set volume to empty string if no volume found
                biblScope_page = monogr.find('imprint/biblScope[@unit="page"]')
                if biblScope_page is not None:
                    from_page = biblScope_page.get('from', '')
                    to_page = biblScope_page.get('to', '')
                    if from_page and to_page:
                        data['page'] = f"{from_page}-{to_page}"
                    elif from_page:
                        data['page'] = from_page
                else:
                    data['page'] = ''  # Set page to empty string if no page info found
                date = monogr.find('imprint/date[@type="published"]')
                if date is not None and 'when' in date.attrib:
                    data['year'] = date.attrib['when']
                else:
                    data['year'] = ''  # Set year to empty string if no year info found
            else:
                data['title'] = ''
                data['authors'] = ''
                data['journal'] = ''
                data['volume'] = ''
                data['page'] = ''
                data['year'] = ''

            # Append data to the list
            bibliographic_data.append(data)
    except ET.ParseError as e:
        print(f"Error parsing XML file '{xml_file}': {e}")
    return bibliographic_data
def write_data_to_csv(data, output_csv):
    # Write data to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'journal', 'volume', 'page', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
# Fill in target input and output:
input_xml_file = r'C:\Project\Project testing\grobid_output_150.xml'
output_csv = 'grobid_150_output.csv'
bibliographic_data = extract_data_from_xml(input_xml_file)
write_data_to_csv(bibliographic_data, output_csv)