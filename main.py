import json

import json
import csv
from utils.extractor import extract_from_pdf_files

def main():
    input_path = 'resources/input/conf.json'
    output_csv = 'resources/output/extracted_data.csv'

    with open(input_path, 'r') as file:
        config = json.load(file)

    pdf_files = [f"resources/documents/{file['filename']}" for file in config['files_to_analyze']]
    data_dict = extract_from_pdf_files(pdf_files)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([''] + pdf_files)
        for key, values in data_dict.items():
            writer.writerow([key] + values)

    print(f"Data extracted and written to '{output_csv}'")

if __name__ == '__main__':
    main()
