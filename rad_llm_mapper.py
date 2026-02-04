#!/usr/bin/env python3
"""
Radiology LLM-Enhanced Mapper - Hybrid rule-based + LLM mapping

This tool provides enhanced mapping capabilities by combining:
1. Rule-based mapping using LOINC and ICD-10-PCS databases
2. LLM-powered fallback for unrecognized or low-confidence cases

Supports both LOINC and ICD-10-PCS coding systems with Chinese and English input.
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.excel_processor import ExcelProcessor
import pandas as pd


def check_dependencies():
    """Check if required dependencies are available"""
    missing = []
    try:
        import pandas
    except ImportError:
        missing.append('pandas')

    try:
        import openpyxl
    except ImportError:
        missing.append('openpyxl')

    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        print("Install with: pip install " + ' '.join(missing))
        sys.exit(1)


def create_enhanced_output_dataframe(results):
    """
    Create output DataFrame with LLM-enhanced results

    Args:
        results: List of hybrid mapping results

    Returns:
        DataFrame with combined results
    """
    output_data = []

    for result in results:
        row = {
            'value_code': result.get('value_code', ''),
            'modality': result.get('modality', ''),
            'Study Description': result.get('study_description', ''),
            'Chinese Study Description': result.get('chinese_description', ''),
            'Contrast': result.get('contrast', ''),
            'Combine Modality': result.get('combine_modality', ''),
            'Primary Modality': result.get('primary_modality', ''),
            'Body Parts': ', '.join(result.get('body_parts', [])),
            'Laterality': result.get('laterality', '') or '',

            # LOINC columns
            'LOINC Code': result.get('loinc_code', '') or '',
            'LOINC Name': result.get('loinc_long_name', '') or '',
            'LOINC Component': result.get('loinc_component', '') or '',
            'LOINC Method': result.get('loinc_method', '') or '',
            'LOINC Confidence': result.get('loinc_confidence', ''),
            'LOINC LLM Used': 'Yes' if result.get('loinc_llm_used') else 'No',

            # ICD-10-PCS columns
            'ICD-10-PCS Code': result.get('icd10pcs_code', '') or '',
            'ICD-10-PCS Description': result.get('icd10pcs_description', '') or '',
            'ICD-10-PCS Section': result.get('icd10pcs_section', '') or '',
            'ICD-10-PCS Body System': result.get('icd10pcs_body_system', '') or '',
            'ICD-10-PCS Root Type': result.get('icd10pcs_root_type', '') or '',
            'ICD-10-PCS Confidence': result.get('icd10pcs_confidence', ''),
            'ICD-10-PCS LLM Used': 'Yes' if result.get('icd10pcs_llm_used') else 'No',

            # Combined issues
            'Has Issues': 'Yes' if result.get('has_issues') else 'No',
            'Issues': '; '.join(result.get('issues', []))
        }
        output_data.append(row)

    return pd.DataFrame(output_data)


def generate_enhanced_summary(results):
    """
    Generate summary statistics from hybrid mapping results

    Args:
        results: List of hybrid mapping results

    Returns:
        Dictionary with summary statistics
    """
    total = len(results)

    # LOINC stats
    loinc_mapped = sum(1 for r in results if r.get('loinc_code'))
    loinc_high = sum(1 for r in results if r.get('loinc_confidence') == 'High')
    loinc_medium = sum(1 for r in results if r.get('loinc_confidence') == 'Medium')
    loinc_low = sum(1 for r in results if r.get('loinc_confidence') == 'Low')
    loinc_llm = sum(1 for r in results if r.get('loinc_llm_used'))

    # ICD-10-PCS stats
    icd10pcs_mapped = sum(1 for r in results if r.get('icd10pcs_code'))
    icd10pcs_high = sum(1 for r in results if r.get('icd10pcs_confidence') == 'High')
    icd10pcs_medium = sum(1 for r in results if r.get('icd10pcs_confidence') == 'Medium')
    icd10pcs_llm = sum(1 for r in results if r.get('icd10pcs_llm_used'))

    # Combined stats
    both_mapped = sum(1 for r in results if r.get('loinc_code') and r.get('icd10pcs_code'))
    with_issues = sum(1 for r in results if r.get('has_issues'))

    # Count by modality
    modality_counts = {}
    for r in results:
        mod = r.get('primary_modality', 'Unknown')
        modality_counts[mod] = modality_counts.get(mod, 0) + 1

    return {
        'total_studies': total,
        'both_mapped': both_mapped,
        'loinc_mapped': loinc_mapped,
        'icd10pcs_mapped': icd10pcs_mapped,
        'with_issues': with_issues,
        'loinc_high': loinc_high,
        'loinc_medium': loinc_medium,
        'loinc_low': loinc_low,
        'loinc_llm_used': loinc_llm,
        'icd10pcs_high': icd10pcs_high,
        'icd10pcs_medium': icd10pcs_medium,
        'icd10pcs_llm_used': icd10pcs_llm,
        'loinc_rate': f"{(loinc_mapped/total*100):.1f}%" if total > 0 else "0%",
        'icd10pcs_rate': f"{(icd10pcs_mapped/total*100):.1f}%" if total > 0 else "0%",
        'both_rate': f"{(both_mapped/total*100):.1f}%" if total > 0 else "0%",
        'modality_distribution': modality_counts
    }


def print_enhanced_summary(summary, use_llm):
    """Print summary statistics for LLM-enhanced mapping"""
    print("\n" + "="*70)
    print("LLM-Enhanced Dual Coding Mapping Summary")
    print("="*70)
    print(f"Total Studies: {summary['total_studies']}")
    print(f"Both Systems Mapped: {summary['both_mapped']} ({summary['both_rate']})")
    print(f"With Issues: {summary['with_issues']}")

    print(f"\nLOINC Mapping:")
    print(f"  Mapped: {summary['loinc_mapped']} ({summary['loinc_rate']})")
    print(f"  High Confidence: {summary['loinc_high']}")
    print(f"  Medium Confidence: {summary['loinc_medium']}")
    print(f"  Low Confidence: {summary['loinc_low']}")
    if use_llm:
        print(f"  LLM Assisted: {summary['loinc_llm_used']}")

    print(f"\nICD-10-PCS Mapping:")
    print(f"  Mapped: {summary['icd10pcs_mapped']} ({summary['icd10pcs_rate']})")
    print(f"  High Confidence: {summary['icd10pcs_high']}")
    print(f"  Medium Confidence: {summary['icd10pcs_medium']}")
    if use_llm:
        print(f"  LLM Assisted: {summary['icd10pcs_llm_used']}")

    print(f"\nModality Distribution:")
    for modality, count in sorted(summary['modality_distribution'].items()):
        print(f"  {modality}: {count}")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='LLM-Enhanced Radiology Code Mapper (LOINC + ICD-10-PCS)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Map using rule-based only (no LLM)
  python rad_llm_mapper.py -i input.xlsx -o output.xlsx

  # Map with LLM fallback for low-confidence cases
  python rad_llm_mapper.py -i input.xlsx -o output.xlsx --use-llm

  # Use specific LLM provider
  python rad_llm_mapper.py -i input.xlsx --use-llm --llm-provider anthropic

  # Set confidence threshold for LLM fallback
  python rad_llm_mapper.py -i input.xlsx --use-llm --confidence-threshold High

Required Excel columns:
  - value_code: Internal code
  - modality: Imaging modality (CR, CT, MR, US, etc.)
  - Study Description: English description

Optional Excel columns:
  - Chinese Study Description: Chinese description
  - Contrast: Y/N/N+Y
  - Combine Modality: Comma-separated modalities

Environment Variables:
  - ANTHROPIC_API_KEY: API key for Claude (Anthropic)
  - OPENAI_API_KEY: API key for OpenAI GPT
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input Excel/CSV file path'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output Excel file path (default: llm_output_TIMESTAMP.xlsx)'
    )

    parser.add_argument(
        '--sheet',
        default='LLM Enhanced Coding',
        help='Output sheet name (default: LLM Enhanced Coding)'
    )

    parser.add_argument(
        '--use-llm',
        action='store_true',
        help='Enable LLM fallback for low-confidence mappings'
    )

    parser.add_argument(
        '--llm-provider',
        choices=['anthropic', 'openai'],
        default='anthropic',
        help='LLM provider (default: anthropic)'
    )

    parser.add_argument(
        '--llm-model',
        help='LLM model name (default: claude-sonnet-4-20250514 for anthropic, gpt-4 for openai)'
    )

    parser.add_argument(
        '--confidence-threshold',
        choices=['High', 'Medium', 'Low', 'None'],
        default='Low',
        help='Confidence threshold below which LLM is used (default: Low)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--check-llm',
        action='store_true',
        help='Check LLM availability and exit'
    )

    args = parser.parse_args()

    # Check dependencies
    check_dependencies()

    # Check LLM availability if requested
    if args.check_llm:
        from src.llm_mapper import check_llm_availability
        availability = check_llm_availability()
        print("\nLLM Availability Check:")
        print(f"  Anthropic package installed: {availability['anthropic_package']}")
        print(f"  OpenAI package installed: {availability['openai_package']}")
        print(f"  ANTHROPIC_API_KEY set: {availability['anthropic_api_key']}")
        print(f"  OPENAI_API_KEY set: {availability['openai_api_key']}")
        print(f"  LLM ready to use: {availability['any_available']}")
        return 0

    # Initialize components
    processor = ExcelProcessor()

    # Setup LLM configuration if enabled
    if args.use_llm:
        from src.llm_mapper import HybridMapper, LLMConfig, check_llm_availability

        # Check LLM availability
        availability = check_llm_availability()
        if not availability['any_available']:
            print("Warning: LLM requested but no API keys found.")
            print("Set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable.")
            print("Falling back to rule-based mapping only.\n")
            args.use_llm = False

    try:
        # Read input file
        print(f"Reading input file: {args.input}")
        df = processor.read_excel(args.input)
        print(f"Found {len(df)} studies to process")

        # Prepare studies
        studies = processor.prepare_studies(df)

        # Map studies
        if args.use_llm:
            from src.llm_mapper import HybridMapper, LLMConfig

            print(f"\nUsing hybrid mapping (rule-based + LLM fallback)")
            print(f"  LLM Provider: {args.llm_provider}")
            print(f"  Confidence Threshold: {args.confidence_threshold}")

            # Setup LLM config
            llm_config = LLMConfig(
                provider=args.llm_provider,
                model=args.llm_model or ('claude-sonnet-4-20250514' if args.llm_provider == 'anthropic' else 'gpt-4')
            )

            mapper = HybridMapper(
                llm_config=llm_config,
                use_llm_fallback=True,
                confidence_threshold=args.confidence_threshold
            )

            print("\nMapping studies with LLM-enhanced hybrid approach...")
            results = mapper.map_batch(studies, code_type="dual")
        else:
            from src.loinc_mapper import LOINCMapper
            from src.icd10pcs_mapper import ICD10PCSMapper

            print("\nUsing rule-based mapping only...")
            loinc_mapper = LOINCMapper()
            icd10pcs_mapper = ICD10PCSMapper()

            loinc_results = loinc_mapper.map_batch(studies)
            icd10pcs_results = icd10pcs_mapper.map_batch(studies)

            # Combine results into dual format
            results = []
            for loinc_r, icd10pcs_r in zip(loinc_results, icd10pcs_results):
                combined = {
                    'value_code': loinc_r['value_code'],
                    'modality': loinc_r['modality'],
                    'study_description': loinc_r['study_description'],
                    'chinese_description': loinc_r['chinese_description'],
                    'contrast': loinc_r['contrast'],
                    'combine_modality': loinc_r['combine_modality'],
                    'primary_modality': loinc_r['primary_modality'],
                    'body_parts': loinc_r['body_parts'],
                    'laterality': loinc_r['laterality'],
                    'loinc_code': loinc_r['loinc_code'],
                    'loinc_long_name': loinc_r['loinc_long_name'],
                    'loinc_component': loinc_r['loinc_component'],
                    'loinc_method': loinc_r['loinc_method'],
                    'loinc_confidence': loinc_r['mapping_confidence'],
                    'loinc_llm_used': False,
                    'icd10pcs_code': icd10pcs_r['icd10pcs_code'],
                    'icd10pcs_description': icd10pcs_r['icd10pcs_description'],
                    'icd10pcs_section': icd10pcs_r['icd10pcs_section'],
                    'icd10pcs_body_system': icd10pcs_r['icd10pcs_body_system'],
                    'icd10pcs_root_type': icd10pcs_r['icd10pcs_root_type'],
                    'icd10pcs_confidence': icd10pcs_r['mapping_confidence'],
                    'icd10pcs_llm_used': False,
                    'issues': list(set(loinc_r['issues'] + icd10pcs_r['issues'])),
                    'has_issues': loinc_r['has_issues'] or icd10pcs_r['has_issues']
                }
                results.append(combined)

        # Generate summary
        summary = generate_enhanced_summary(results)
        print_enhanced_summary(summary, args.use_llm)

        # Create output DataFrame
        output_df = create_enhanced_output_dataframe(results)

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"llm_output_{timestamp}.xlsx"

        # Write output
        processor.write_excel(output_df, output_path, args.sheet)

        # Print detailed issues if verbose
        if args.verbose:
            print("\nStudies with issues or LLM assistance:")
            for result in results:
                show_detail = result.get('has_issues') or result.get('loinc_llm_used') or result.get('icd10pcs_llm_used')
                if show_detail:
                    print(f"\n{result.get('value_code')} - {result.get('study_description')}")
                    if result.get('loinc_llm_used'):
                        print(f"  LOINC: LLM assisted -> {result.get('loinc_code')}")
                    if result.get('icd10pcs_llm_used'):
                        print(f"  ICD-10-PCS: LLM assisted -> {result.get('icd10pcs_code')}")
                    if result.get('issues'):
                        for issue in result.get('issues'):
                            print(f"  Issue: {issue}")

        print("\nLLM-enhanced mapping completed successfully!")
        return 0

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
