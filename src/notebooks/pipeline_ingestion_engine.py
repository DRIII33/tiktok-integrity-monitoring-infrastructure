"""
TikTok Global Operations - Trust & Safety Engineering
Component: Advanced Text Normalization & Anomaly Detection Pipeline (Phases 1 & 2)
Description: Parses raw ad payloads, extracts mixed character anomalies, and strips hidden evasion symbols.
"""

import re
import unicodedata
import pandas as pd
import numpy as np

class IntegrityIngestionEngine:
    def __init__(self):
        self.homoglyph_map = {
            '\u03b1': 'a', '\u0430': 'a', '@': 'a',
            '\u03c5': 'u', '0': 'o', '5': 's'
        }
        self.violation_pattern = re.compile(r'(whatsapp|pharmacy|drugs|crypto|telegram|line group)')

    def strip_invisible_characters(self, text: str) -> tuple:
        """Removes hidden characters like zero-width spaces and logs the anomaly count."""
        invisible_chars = ['\u200b', '\u200c', '\u200d', '\ufeff']
        anomaly_count = 0
        cleaned_text = text
        for char in invisible_chars:
            if char in cleaned_text:
                anomaly_count += cleaned_text.count(char)
                cleaned_text = cleaned_text.replace(char, '')
        return cleaned_text, anomaly_count

    def normalize_text(self, text: str) -> str:
        """Standardizes character substitutions and maps inputs back to base alphabets."""
        text = text.lower()
        for homoglyph, replacement in self.homoglyph_map.items():
            text = text.replace(homoglyph, replacement)
        text = "".join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
        return text

    def process_payload_stream(self, dataframe: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """Processes incoming data streams to apply text cleaning filters and log anomalies."""
        processed_records = []
        for idx, row in dataframe.iterrows():
            raw_text = str(row[text_column])
            clean_text, hidden_count = self.strip_invisible_characters(raw_text)
            normalized_text = self.normalize_text(clean_text)
            is_violation = 1 if self.violation_pattern.search(normalized_text) else 0
            
            processed_records.append({
                'account_id': row.get('account_id', f"ACC_{idx:05d}"),
                'cleaned_text': normalized_text,
                'unicode_anomalies_count': hidden_count,
                'pipeline_prediction': is_violation
            })
        return pd.DataFrame(processed_records)

if __name__ == "__main__":
    sample_data = pd.DataFrame({
        'account_id': ['ACT_101', 'ACT_102', 'ACT_103'],
        'payload': ['Wh\u200bat\u200sapp group link now!', 'Ph\u03b1rmacy delivery info', 'Clean marketing campaign approval']
    })
    engine = IntegrityIngestionEngine()
    output_df = engine.process_payload_stream(sample_data, 'payload')
    print("Ingestion Engine Pipeline Test Output:")
    print(output_df.to_string())
