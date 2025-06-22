import re
import logging
import pdfplumber

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(ch)


def extract_keywords_from_lines(lines, keywords):
    for line in lines:
        for key in keywords:
            if key in line and key not in ["F1", "F2", "F3", "T", "Inizio", "Fine"]:
                value = line.split(':')[-1].strip().split(' ')[0]
                keywords[key] = value
                logger.debug(f"Matched '{key}' with value '{value}'")
                break
    return keywords


def extract_consumption_data(text, keywords):
    pattern = r"Totale consumo fatturato di energia attiva.*?(\d+[,]?\d*) kWh (\d+[,]?\d*) kWh (\d+[,]?\d*) kWh (\d+[,]?\d*)"
    match = re.search(pattern, text)
    if match:
        keywords["F1"], keywords["F2"], keywords["F3"], keywords["T"] = match.groups()
        logger.debug(f"Extracted F1–F3, T values: {match.groups()}")
    else:
        logger.warning("Consumption values (F1, F2, F3, T) not found.")
    return keywords


def extract_billing_period(text, keywords):
    matches = re.findall(
        r"dal\s+(\d{2}\s(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s\d{4}).*?al\s+(\d{2}\s(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s\d{4})",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if matches:
        keywords["Inizio"], keywords["Fine"] = matches[0]
        logger.debug(f"Found billing period: {keywords['Inizio']} – {keywords['Fine']}")
    else:
        logger.warning("Billing period (dal...al) not found.")
    return keywords


def extract_data(text):
    logger.debug("Starting data extraction from text.")

    keywords = {
        "Spesa per la materia energia": None,
        "e la gestione del contatore": None,
        "Arrotondamento precedente": None,
        "Arrotondamento attuale": None,
        "Totale imposte e IVA": None,
        "TOTALE BOLLETTA": None,
        "F1": None,
        "F2": None,
        "F3": None,
        "T": None,
        "Inizio": None,
        "Fine": None
    }

    lines = text.split('\n')
    combined_text = " ".join(lines)

    keywords = extract_keywords_from_lines(lines, keywords)
    keywords = extract_consumption_data(combined_text, keywords)
    keywords = extract_billing_period(combined_text, keywords)

    return keywords


def extract_from_pdf_files(pdf_files):
    logger.info(f"Starting extraction from {len(pdf_files)} PDF file(s).")
    data_dict = {key: [] for key in extract_data('').keys()}

    for pdf_file in pdf_files:
        try:
            logger.info(f"Reading file: {pdf_file}")
            with pdfplumber.open(pdf_file) as pdf:
                full_text = ''
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + '\n'

                with open("resources/output/full_text.txt", "w", encoding="utf-8") as txt_file:
                    txt_file.write(full_text)

                extracted_data = extract_data(full_text)
                for key, value in extracted_data.items():
                    data_dict[key].append(value)

        except Exception as e:
            logger.error(f"Failed to process {pdf_file}: {e}")
            for key in data_dict:
                data_dict[key].append(None)

    return data_dict