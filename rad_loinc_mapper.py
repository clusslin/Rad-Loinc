#!/usr/bin/env python3
"""
Radiology LOINC Mapper - Main Application
Map radiology examinations to LOINC codes
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.loinc_mapper import LOINCMapper
from src.excel_processor import ExcelProcessor


def main():
    parser = argparse.ArgumentParser(
        description='Map radiology examinations to LOINC codes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Map studies from Excel file
  python rad_loinc_mapper.py -i input.xlsx -o output.xlsx

  # Specify custom output directory
  python rad_loinc_mapper.py -i input.xlsx -o results/output.xlsx

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
        help='Input Excel file path'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output Excel file path (default: output_TIMESTAMP.xlsx)'
    )

    parser.add_argument(
        '--sheet',
        default='LOINC Mapping',
        help='Output sheet name (default: LOINC Mapping)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Initialize components
    mapper = LOINCMapper()
    processor = ExcelProcessor()

    try:
        # Read input file
        print(f"Reading input file: {args.input}")
        df = processor.read_excel(args.input)
        print(f"Found {len(df)} studies to process")

        # Prepare studies
        studies = processor.prepare_studies(df)

        # Map to LOINC
        print("\nMapping studies to LOINC codes...")
        results = mapper.map_batch(studies)

        # Generate summary
        summary = processor.generate_summary(results)
        processor.print_summary(summary)

        # Create output DataFrame
        output_df = processor.create_output_dataframe(results)

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output_{timestamp}.xlsx"

        # Write output
        processor.write_excel(output_df, output_path, args.sheet)

        # Print issues if verbose
        if args.verbose:
            print("\nStudies with issues:")
            for result in results:
                if result['has_issues']:
                    print(f"\n{result['value_code']} - {result['study_description']}")
                    for issue in result['issues']:
                        print(f"  - {issue}")

        print("\nMapping completed successfully!")
        return 0

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
