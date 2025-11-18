#!/usr/bin/env python3
"""
Test script for radiology LOINC mapper
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.loinc_mapper import LOINCMapper
from src.description_parser import DescriptionParser


def test_parser():
    """Test the description parser"""
    print("Testing Description Parser")
    print("="*60)

    parser = DescriptionParser()

    test_cases = [
        {
            'desc': 'Chest PA view',
            'chinese': '胸部正面',
            'modality': 'CR'
        },
        {
            'desc': 'Rt hand AP and Lateral',
            'chinese': '右手正側面',
            'modality': 'CR'
        },
        {
            'desc': 'Brain with contrast',
            'chinese': '腦部含對比劑',
            'modality': 'MR'
        },
        {
            'desc': 'C-spine trauma',
            'chinese': '頸椎外傷',
            'modality': 'CT'
        },
        {
            'desc': 'Abd sonography',
            'chinese': '腹部超音波',
            'modality': 'US'
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['desc']}")
        result = parser.parse_study_description(
            test['desc'],
            test['chinese'],
            test['modality']
        )
        print(f"  Expanded: {result['expanded_description']}")
        print(f"  Body parts: {result['body_parts']}")
        print(f"  Laterality: {result['laterality']}")
        print(f"  Issues: {result['issues']}")

    print("\n" + "="*60 + "\n")


def test_mapper():
    """Test the LOINC mapper"""
    print("Testing LOINC Mapper")
    print("="*60)

    mapper = LOINCMapper()

    test_studies = [
        {
            'value_code': 'TEST001',
            'modality': 'CR',
            'Study Description': 'Chest PA view',
            'Chinese Study Description': '胸部正面',
            'Contrast': 'N',
            'Combine Modality': ''
        },
        {
            'value_code': 'TEST002',
            'modality': 'CT',
            'Study Description': 'Brain without contrast',
            'Chinese Study Description': '腦部電腦斷層',
            'Contrast': 'N',
            'Combine Modality': ''
        },
        {
            'value_code': 'TEST003',
            'modality': 'MR',
            'Study Description': 'Lt knee',
            'Chinese Study Description': '左膝',
            'Contrast': 'N',
            'Combine Modality': ''
        },
        {
            'value_code': 'TEST004',
            'modality': 'CT',
            'Study Description': 'Abd with contrast',
            'Chinese Study Description': '腹部',
            'Contrast': 'Y',
            'Combine Modality': ''
        }
    ]

    results = mapper.map_batch(test_studies)

    for result in results:
        print(f"\nStudy: {result['value_code']} - {result['study_description']}")
        print(f"  Body parts: {result['body_parts']}")
        print(f"  Laterality: {result['laterality']}")
        print(f"  LOINC Code: {result['loinc_code']}")
        print(f"  LOINC Name: {result['loinc_long_name']}")
        print(f"  Confidence: {result['mapping_confidence']}")
        if result['has_issues']:
            print(f"  Issues: {'; '.join(result['issues'])}")

    print("\n" + "="*60 + "\n")


def main():
    """Run all tests"""
    print("\nRadiology LOINC Mapper - Test Suite\n")

    test_parser()
    test_mapper()

    print("All tests completed!\n")


if __name__ == '__main__':
    main()
