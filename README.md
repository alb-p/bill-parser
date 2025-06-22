# Bill Extractor

`bill-extractor` is a Python tool that automatically extracts structured data from electricity bill PDFs and converts it into CSV format for easy analysis.

## 🚀 Features

- Extracts:
  - Charges for energy, meter management, taxes, and total
  - Consumption by time bands (F1, F2, F3, Total)
  - Billing period (start/end dates)
- Supports multiple PDF files
- Exports data directly to CSV
- Saves full raw text output for debugging

## 🛠️ Requirements

- Python 3.7+
- [pdfplumber](https://github.com/jsvine/pdfplumber)

## 📦 Installation

```bash
git clone https://github.com/your-username/bill-extractor.git
cd bill-extractor
python -m venv env
source env/bin/activate  # or 'env\Scripts\activate' on Windows
pip install -r requirements.txt
```

## 📁 Project Structure

```
bill-extractor/
├── main.py
├── utils/
│   └── extractor.py
├── resources/
│   ├── input/
│   │   └── conf.json
│   ├── documents/
│   │   └── 2025_05.pdf
│   └── output/
│       ├── extracted_data.csv
│       └── full_text.txt
```

## ⚙️ Usage

Edit `resources/input/conf.json` to list the PDF files you want to analyze:

```json
{
  "files_to_analyze": [
    {
      "filename": "2025_05.pdf"
    }
  ]
}
```

Then run:

```bash
python main.py
```

## 🧪 Output

- Extracted CSV: `resources/output/extracted_data.csv`
- Raw full text: `resources/output/full_text.txt`

## 📄 License

MIT