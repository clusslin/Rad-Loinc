"""
Excel file processor for radiology LOINC mapping
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import datetime


class ExcelProcessor:
    """Process Excel files for radiology LOINC mapping"""

    def __init__(self):
        self.required_columns = [
            'value_code',
            'modality',
            'Study Description'
        ]
        self.optional_columns = [
            'Chinese Study Description',
            'Contrast',
            'Combine Modality'
        ]

    def read_excel(self, file_path: str) -> pd.DataFrame:
        """
        Read Excel or CSV file with radiology study data

        Args:
            file_path: Path to Excel or CSV file

        Returns:
            DataFrame with study data
        """
        try:
            # Check file extension
            file_path_lower = file_path.lower()
            if file_path_lower.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Check for required columns
            missing_cols = []
            for col in self.required_columns:
                if col not in df.columns:
                    missing_cols.append(col)

            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")

            # Fill optional columns if missing
            for col in self.optional_columns:
                if col not in df.columns:
                    df[col] = ""

            # Convert to string and handle NaN
            df = df.fillna("")
            for col in df.columns:
                df[col] = df[col].astype(str)

            return df

        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")

    def prepare_studies(self, df: pd.DataFrame) -> List[Dict]:
        """
        Convert DataFrame to list of study dictionaries

        Args:
            df: DataFrame with study data

        Returns:
            List of study dictionaries
        """
        studies = []
        for idx, row in df.iterrows():
            study = {
                'value_code': str(row.get('value_code', '')),
                'modality': str(row.get('modality', '')),
                'Study Description': str(row.get('Study Description', '')),
                'Chinese Study Description': str(row.get('Chinese Study Description', '')),
                'Contrast': str(row.get('Contrast', '')),
                'Combine Modality': str(row.get('Combine Modality', ''))
            }
            studies.append(study)
        return studies

    def create_output_dataframe(self, mapping_results: List[Dict]) -> pd.DataFrame:
        """
        Create output DataFrame from mapping results

        Args:
            mapping_results: List of mapping result dictionaries

        Returns:
            DataFrame with results
        """
        output_data = []

        for result in mapping_results:
            row = {
                'value_code': result['value_code'],
                'modality': result['modality'],
                'Study Description': result['study_description'],
                'Chinese Study Description': result['chinese_description'],
                'Contrast': result['contrast'],
                'Combine Modality': result['combine_modality'],
                'Primary Modality': result['primary_modality'],
                'Expanded Description': result['expanded_description'],
                'Body Parts': ', '.join(result['body_parts']),
                'Laterality': result['laterality'] if result['laterality'] else '',
                'LOINC Code': result['loinc_code'] if result['loinc_code'] else '',
                'LOINC Name': result['loinc_long_name'] if result['loinc_long_name'] else '',
                'LOINC Component': result['loinc_component'] if result['loinc_component'] else '',
                'LOINC Method': result['loinc_method'] if result['loinc_method'] else '',
                'Mapping Confidence': result['mapping_confidence'],
                'Has Issues': 'Yes' if result['has_issues'] else 'No',
                'Issues': '; '.join(result['issues']) if result['issues'] else ''
            }
            output_data.append(row)

        df = pd.DataFrame(output_data)
        return df

    def write_excel(
        self,
        df: pd.DataFrame,
        output_path: str,
        sheet_name: str = 'LOINC Mapping'
    ):
        """
        Write DataFrame to Excel file

        Args:
            df: DataFrame to write
            output_path: Output file path
            sheet_name: Sheet name
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Write to Excel with formatting
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Get worksheet
                worksheet = writer.sheets[sheet_name]

                # Auto-adjust column widths
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    # Cap at 50 characters
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[chr(65 + idx)].width = adjusted_width

            print(f"Output written to: {output_path}")

        except Exception as e:
            raise Exception(f"Error writing Excel file: {str(e)}")

    def generate_summary(self, mapping_results: List[Dict]) -> Dict:
        """
        Generate summary statistics from mapping results

        Args:
            mapping_results: List of mapping results

        Returns:
            Dictionary with summary statistics
        """
        total = len(mapping_results)
        with_loinc = sum(1 for r in mapping_results if r['loinc_code'])
        with_issues = sum(1 for r in mapping_results if r['has_issues'])
        high_confidence = sum(1 for r in mapping_results if r['mapping_confidence'] == 'High')
        low_confidence = sum(1 for r in mapping_results if r['mapping_confidence'] == 'Low')
        no_mapping = sum(1 for r in mapping_results if r['mapping_confidence'] == 'None')

        # Count by modality
        modality_counts = {}
        for r in mapping_results:
            mod = r['primary_modality']
            modality_counts[mod] = modality_counts.get(mod, 0) + 1

        summary = {
            'total_studies': total,
            'mapped_to_loinc': with_loinc,
            'with_issues': with_issues,
            'high_confidence': high_confidence,
            'low_confidence': low_confidence,
            'no_mapping': no_mapping,
            'mapping_rate': f"{(with_loinc/total*100):.1f}%" if total > 0 else "0%",
            'modality_distribution': modality_counts
        }

        return summary

    def print_summary(self, summary: Dict):
        """Print summary statistics"""
        print("\n" + "="*60)
        print("LOINC Mapping Summary")
        print("="*60)
        print(f"Total Studies: {summary['total_studies']}")
        print(f"Mapped to LOINC: {summary['mapped_to_loinc']} ({summary['mapping_rate']})")
        print(f"With Issues: {summary['with_issues']}")
        print(f"\nConfidence Levels:")
        print(f"  High: {summary['high_confidence']}")
        print(f"  Low: {summary['low_confidence']}")
        print(f"  None: {summary['no_mapping']}")
        print(f"\nModality Distribution:")
        for modality, count in sorted(summary['modality_distribution'].items()):
            print(f"  {modality}: {count}")
        print("="*60 + "\n")
