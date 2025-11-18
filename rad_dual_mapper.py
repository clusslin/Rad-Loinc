#!/usr/bin/env python3
"""
Radiology Dual Mapper - Map to both LOINC and ICD-10-PCS codes
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.loinc_mapper import LOINCMapper
from src.icd10pcs_mapper import ICD10PCSMapper
from src.excel_processor import ExcelProcessor
import pandas as pd


def create_dual_output_dataframe(loinc_results, icd10pcs_results):
    """
    Create output DataFrame with both LOINC and ICD-10-PCS codes

    Args:
        loinc_results: List of LOINC mapping results
        icd10pcs_results: List of ICD-10-PCS mapping results

    Returns:
        DataFrame with combined results
    """
    output_data = []

    for loinc_result, icd10pcs_result in zip(loinc_results, icd10pcs_results):
        # Combine issues from both mappings
        all_issues = set()
        if loinc_result['issues']:
            all_issues.update([f"LOINC: {issue}" for issue in loinc_result['issues']])
        if icd10pcs_result['issues']:
            all_issues.update([f"ICD-10-PCS: {issue}" for issue in icd10pcs_result['issues']])

        has_any_issues = loinc_result['has_issues'] or icd10pcs_result['has_issues']

        row = {
            'value_code': loinc_result['value_code'],
            'modality': loinc_result['modality'],
            'Study Description': loinc_result['study_description'],
            'Chinese Study Description': loinc_result['chinese_description'],
            'Contrast': loinc_result['contrast'],
            'Combine Modality': loinc_result['combine_modality'],
            'Primary Modality': loinc_result['primary_modality'],
            'Expanded Description': loinc_result['expanded_description'],
            'Body Parts': ', '.join(loinc_result['body_parts']),
            'Laterality': loinc_result['laterality'] if loinc_result['laterality'] else '',

            # LOINC columns
            'LOINC Code': loinc_result['loinc_code'] if loinc_result['loinc_code'] else '',
            'LOINC Name': loinc_result['loinc_long_name'] if loinc_result['loinc_long_name'] else '',
            'LOINC Component': loinc_result['loinc_component'] if loinc_result['loinc_component'] else '',
            'LOINC Method': loinc_result['loinc_method'] if loinc_result['loinc_method'] else '',
            'LOINC Confidence': loinc_result['mapping_confidence'],

            # ICD-10-PCS columns
            'ICD-10-PCS Code': icd10pcs_result['icd10pcs_code'] if icd10pcs_result['icd10pcs_code'] else '',
            'ICD-10-PCS Description': icd10pcs_result['icd10pcs_description'] if icd10pcs_result['icd10pcs_description'] else '',
            'ICD-10-PCS Section': icd10pcs_result['icd10pcs_section'] if icd10pcs_result['icd10pcs_section'] else '',
            'ICD-10-PCS Body System': icd10pcs_result['icd10pcs_body_system'] if icd10pcs_result['icd10pcs_body_system'] else '',
            'ICD-10-PCS Root Type': icd10pcs_result['icd10pcs_root_type'] if icd10pcs_result['icd10pcs_root_type'] else '',
            'ICD-10-PCS Confidence': icd10pcs_result['mapping_confidence'],

            # Combined issues
            'Has Issues': 'Yes' if has_any_issues else 'No',
            'Issues': '; '.join(sorted(all_issues)) if all_issues else ''
        }
        output_data.append(row)

    df = pd.DataFrame(output_data)
    return df


def generate_dual_summary(loinc_results, icd10pcs_results):
    """
    Generate summary statistics from both mapping results

    Args:
        loinc_results: List of LOINC mapping results
        icd10pcs_results: List of ICD-10-PCS mapping results

    Returns:
        Dictionary with summary statistics
    """
    total = len(loinc_results)

    # LOINC stats
    loinc_mapped = sum(1 for r in loinc_results if r['loinc_code'])
    loinc_high = sum(1 for r in loinc_results if r['mapping_confidence'] == 'High')
    loinc_low = sum(1 for r in loinc_results if r['mapping_confidence'] == 'Low')
    loinc_none = sum(1 for r in loinc_results if r['mapping_confidence'] == 'None')

    # ICD-10-PCS stats
    icd10pcs_mapped = sum(1 for r in icd10pcs_results if r['icd10pcs_code'])
    icd10pcs_high = sum(1 for r in icd10pcs_results if r['mapping_confidence'] == 'High')
    icd10pcs_none = sum(1 for r in icd10pcs_results if r['mapping_confidence'] == 'None')

    # Combined stats
    both_mapped = sum(1 for l, i in zip(loinc_results, icd10pcs_results)
                     if l['loinc_code'] and i['icd10pcs_code'])

    with_issues = sum(1 for l, i in zip(loinc_results, icd10pcs_results)
                     if l['has_issues'] or i['has_issues'])

    # Count by modality
    modality_counts = {}
    for r in loinc_results:
        mod = r['primary_modality']
        modality_counts[mod] = modality_counts.get(mod, 0) + 1

    summary = {
        'total_studies': total,
        'both_mapped': both_mapped,
        'loinc_mapped': loinc_mapped,
        'icd10pcs_mapped': icd10pcs_mapped,
        'with_issues': with_issues,
        'loinc_high': loinc_high,
        'loinc_low': loinc_low,
        'loinc_none': loinc_none,
        'icd10pcs_high': icd10pcs_high,
        'icd10pcs_none': icd10pcs_none,
        'loinc_rate': f"{(loinc_mapped/total*100):.1f}%" if total > 0 else "0%",
        'icd10pcs_rate': f"{(icd10pcs_mapped/total*100):.1f}%" if total > 0 else "0%",
        'both_rate': f"{(both_mapped/total*100):.1f}%" if total > 0 else "0%",
        'modality_distribution': modality_counts
    }

    return summary


def print_dual_summary(summary):
    """Print summary statistics for both coding systems"""
    print("\n" + "="*70)
    print("Dual Coding Mapping Summary (LOINC + ICD-10-PCS)")
    print("="*70)
    print(f"Total Studies: {summary['total_studies']}")
    print(f"Both Systems Mapped: {summary['both_mapped']} ({summary['both_rate']})")
    print(f"With Issues: {summary['with_issues']}")
    print(f"\nLOINC Mapping:")
    print(f"  Mapped: {summary['loinc_mapped']} ({summary['loinc_rate']})")
    print(f"  High Confidence: {summary['loinc_high']}")
    print(f"  Low Confidence: {summary['loinc_low']}")
    print(f"  Not Mapped: {summary['loinc_none']}")
    print(f"\nICD-10-PCS Mapping:")
    print(f"  Mapped: {summary['icd10pcs_mapped']} ({summary['icd10pcs_rate']})")
    print(f"  High Confidence: {summary['icd10pcs_high']}")
    print(f"  Not Mapped: {summary['icd10pcs_none']}")
    print(f"\nModality Distribution:")
    for modality, count in sorted(summary['modality_distribution'].items()):
        print(f"  {modality}: {count}")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Map radiology examinations to both LOINC and ICD-10-PCS codes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Map studies from Excel file to both coding systems
  python rad_dual_mapper.py -i input.xlsx -o output.xlsx

  # Map with verbose output
  python rad_dual_mapper.py -i input.xlsx -o output.xlsx -v

Required Excel columns:
  - value_code: Internal code
  - modality: Imaging modality (CR, CT, MR, US, etc.)
  - Study Description: English description

Optional Excel columns:
  - Chinese Study Description: Chinese description
  - Contrast: Y/N/N+Y
  - Combine Modality: Comma-separated modalities (e.g., RF,CT)
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input Excel/CSV file path'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output Excel file path (default: dual_output_TIMESTAMP.xlsx)'
    )

    parser.add_argument(
        '--sheet',
        default='Dual Coding',
        help='Output sheet name (default: Dual Coding)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Initialize components
    loinc_mapper = LOINCMapper()
    icd10pcs_mapper = ICD10PCSMapper()
    processor = ExcelProcessor()

    try:
        # Read input file
        print(f"Reading input file: {args.input}")
        df = processor.read_excel(args.input)
        print(f"Found {len(df)} studies to process")

        # Prepare studies
        studies = processor.prepare_studies(df)

        # Map to both coding systems
        print("\nMapping studies to LOINC and ICD-10-PCS codes...")
        loinc_results = loinc_mapper.map_batch(studies)
        icd10pcs_results = icd10pcs_mapper.map_batch(studies)

        # Generate summary
        summary = generate_dual_summary(loinc_results, icd10pcs_results)
        print_dual_summary(summary)

        # Create output DataFrame
        output_df = create_dual_output_dataframe(loinc_results, icd10pcs_results)

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"dual_output_{timestamp}.xlsx"

        # Write output
        processor.write_excel(output_df, output_path, args.sheet)

        # Print detailed issues if verbose
        if args.verbose:
            print("\nStudies with issues:")
            for loinc_r, icd10pcs_r in zip(loinc_results, icd10pcs_results):
                if loinc_r['has_issues'] or icd10pcs_r['has_issues']:
                    print(f"\n{loinc_r['value_code']} - {loinc_r['study_description']}")
                    if loinc_r['issues']:
                        print(f"  LOINC issues:")
                        for issue in loinc_r['issues']:
                            print(f"    - {issue}")
                    if icd10pcs_r['issues']:
                        print(f"  ICD-10-PCS issues:")
                        for issue in icd10pcs_r['issues']:
                            print(f"    - {issue}")

        print("\nDual coding mapping completed successfully!")
        return 0

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
