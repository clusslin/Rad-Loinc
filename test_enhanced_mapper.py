#!/usr/bin/env python3
"""
Enhanced test suite for the Radiology LOINC/ICD-10-PCS Mapper

Tests both rule-based mapping and validates the expanded databases.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.loinc_mapper import LOINCMapper
from src.icd10pcs_mapper import ICD10PCSMapper
from src.description_parser import DescriptionParser
from src.loinc_database import LOINC_DATABASE
from src.icd10pcs_database import ICD10PCS_DATABASE


def test_database_coverage():
    """Test the coverage of the expanded databases"""
    print("\n" + "="*60)
    print("DATABASE COVERAGE TEST")
    print("="*60)

    # Count unique LOINC codes
    loinc_codes = set()
    for entry in LOINC_DATABASE.values():
        loinc_codes.add(entry['code'])
    print(f"\nLOINC Database:")
    print(f"  Total entries: {len(LOINC_DATABASE)}")
    print(f"  Unique LOINC codes: {len(loinc_codes)}")

    # Count unique ICD-10-PCS codes
    icd10pcs_codes = set()
    for entry in ICD10PCS_DATABASE.values():
        icd10pcs_codes.add(entry['code'])
    print(f"\nICD-10-PCS Database:")
    print(f"  Total entries: {len(ICD10PCS_DATABASE)}")
    print(f"  Unique ICD-10-PCS codes: {len(icd10pcs_codes)}")

    # List modalities covered
    modalities = set()
    for key in LOINC_DATABASE.keys():
        modalities.add(key[1])
    print(f"\nModalities covered in LOINC: {sorted(modalities)}")

    modalities_icd = set()
    for key in ICD10PCS_DATABASE.keys():
        modalities_icd.add(key[1])
    print(f"Modalities covered in ICD-10-PCS: {sorted(modalities_icd)}")

    # List body parts covered
    body_parts = set()
    for key in LOINC_DATABASE.keys():
        body_parts.add(key[0])
    print(f"\nBody parts in LOINC: {len(body_parts)}")
    print(f"  Examples: {sorted(list(body_parts))[:10]}...")

    return True


def test_parser_chinese():
    """Test Chinese description parsing"""
    print("\n" + "="*60)
    print("CHINESE PARSING TEST")
    print("="*60)

    parser = DescriptionParser()
    test_cases = [
        ("Chest PA", "胸部正面X光", "CR", "N"),
        ("Brain CT", "腦部電腦斷層", "CT", "N"),
        ("Brain MRI with contrast", "腦部磁振造影含對比劑", "MR", "Y"),
        ("Lt knee MRI", "左膝磁振造影", "MR", "N"),
        ("Rt shoulder", "右肩X光", "CR", "N"),
        ("C-spine", "頸椎", "CR", "N"),
        ("L-spine MRI", "腰椎磁振造影", "MR", "N"),
        ("Abd US", "腹部超音波", "US", "N"),
        ("Coronary angio", "冠狀動脈血管攝影", "XA", "Y"),
        ("Thyroid US", "甲狀腺超音波", "US", "N"),
    ]

    passed = 0
    for eng, chi, modality, contrast in test_cases:
        result = parser.parse_study_description(eng, chi, modality, contrast)
        print(f"\n  English: {eng}")
        print(f"  Chinese: {chi}")
        print(f"  Body parts: {result['body_parts']}")
        print(f"  Laterality: {result['laterality']}")
        if result['body_parts']:
            passed += 1
            print("  Status: PASS")
        else:
            print("  Status: FAIL - No body parts identified")

    print(f"\nChinese parsing: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)


def test_loinc_mapping():
    """Test LOINC mapping accuracy"""
    print("\n" + "="*60)
    print("LOINC MAPPING TEST")
    print("="*60)

    mapper = LOINCMapper()

    # Define test cases with expected LOINC codes
    test_cases = [
        # (value_code, modality, description, chinese, contrast, expected_code)
        ("T01", "CR", "Chest PA view", "胸部正面", "N", "36643-5"),
        ("T02", "CT", "Brain without contrast", "腦部CT", "N", "24558-9"),
        ("T03", "CT", "Brain with contrast", "腦部CT含對比劑", "Y", "24557-1"),
        ("T04", "MR", "Brain MRI", "腦部磁振造影", "N", "24556-3"),
        ("T05", "MR", "Brain MRI with contrast", "腦部MRI含對比劑", "Y", "24555-5"),
        ("T06", "CT", "Chest without contrast", "胸部CT", "N", "24627-2"),
        ("T07", "CT", "Chest with contrast", "胸部CT含顯影", "Y", "24626-4"),
        ("T08", "CR", "C-spine", "頸椎", "N", "36713-6"),
        ("T09", "MR", "Cervical spine MRI", "頸椎MRI", "N", "24852-6"),
        ("T10", "CR", "L-spine", "腰椎", "N", "36714-4"),
        ("T11", "MR", "Lumbar spine MRI", "腰椎MRI", "N", "24860-9"),
        ("T12", "CR", "Rt hand", "右手X光", "N", "37362-0"),
        ("T13", "CR", "Lt hand", "左手", "N", "37361-2"),
        ("T14", "MR", "Lt knee MRI", "左膝MRI", "N", "24875-7"),
        ("T15", "MR", "Rt knee MRI", "右膝磁振造影", "N", "24876-5"),
        ("T16", "CR", "Pelvis", "骨盆", "N", "37748-0"),
        ("T17", "US", "Abdomen", "腹部超音波", "N", "30704-1"),
        ("T18", "US", "Liver", "肝臟超音波", "N", "30705-8"),
        ("T19", "US", "Kidney bilateral", "雙側腎臟超音波", "N", "24642-1"),
        ("T20", "BMD", "Spine bone density", "脊椎骨密度", "N", "38262-7"),
        # Extended tests
        ("T21", "CR", "T-spine", "胸椎", "N", "36715-1"),
        ("T22", "MR", "Thoracic spine MRI", "胸椎MRI", "N", "24856-7"),
        ("T23", "CR", "Rt shoulder", "右肩", "N", "37016-2"),
        ("T24", "CR", "Lt shoulder", "左肩", "N", "37015-4"),
        ("T25", "CR", "Rt elbow", "右肘", "N", "37256-4"),
        ("T26", "CR", "Rt wrist", "右腕", "N", "37022-0"),
        ("T27", "CR", "Rt ankle", "右踝", "N", "37048-2"),
        ("T28", "CR", "Rt foot", "右足", "N", "37542-4"),
        ("T29", "CT", "Neck without contrast", "頸部CT", "N", "24551-4"),
        ("T30", "US", "Thyroid", "甲狀腺超音波", "N", "30734-8"),
    ]

    passed = 0
    high_confidence = 0

    for value_code, modality, desc, chinese, contrast, expected in test_cases:
        result = mapper.map_study_to_loinc(
            value_code=value_code,
            modality=modality,
            study_desc=desc,
            chinese_desc=chinese,
            contrast=contrast
        )

        actual = result['loinc_code']
        confidence = result['mapping_confidence']

        status = "PASS" if actual == expected else "FAIL"
        if actual == expected:
            passed += 1
        if confidence == 'High':
            high_confidence += 1

        if actual != expected:
            print(f"  {value_code}: {desc}")
            print(f"    Expected: {expected}, Got: {actual} ({confidence})")
            print(f"    Body parts: {result['body_parts']}")

    print(f"\nLOINC Mapping Results:")
    print(f"  Passed: {passed}/{len(test_cases)} ({passed/len(test_cases)*100:.1f}%)")
    print(f"  High Confidence: {high_confidence}/{len(test_cases)} ({high_confidence/len(test_cases)*100:.1f}%)")

    return passed >= len(test_cases) * 0.9  # 90% threshold


def test_icd10pcs_mapping():
    """Test ICD-10-PCS mapping accuracy"""
    print("\n" + "="*60)
    print("ICD-10-PCS MAPPING TEST")
    print("="*60)

    mapper = ICD10PCSMapper()

    # Define test cases with expected ICD-10-PCS codes
    test_cases = [
        ("T01", "CR", "Chest PA view", "胸部正面", "N", "BW03ZZZ"),
        ("T02", "CT", "Brain without contrast", "腦部CT", "N", "B020ZZZ"),
        ("T03", "CT", "Brain with contrast", "腦部CT含對比劑", "Y", "B0200ZZ"),
        ("T04", "MR", "Brain MRI", "腦部磁振造影", "N", "B030ZZZ"),
        ("T05", "MR", "Brain MRI with contrast", "腦部MRI含對比劑", "Y", "B0300ZZ"),
        ("T06", "CT", "Chest without contrast", "胸部CT", "N", "BW24ZZZ"),
        ("T07", "CT", "Chest with contrast", "胸部CT含顯影", "Y", "BW240ZZ"),
        ("T08", "CR", "C-spine", "頸椎", "N", "BR00ZZZ"),
        ("T09", "MR", "Cervical spine MRI", "頸椎MRI", "N", "BR30ZZZ"),
        ("T10", "CR", "L-spine", "腰椎", "N", "BR03ZZZ"),
        ("T11", "MR", "Lumbar spine MRI", "腰椎MRI", "N", "BR33ZZZ"),
        ("T12", "CR", "Rt hand", "右手X光", "N", "BP0JZZZ"),
        ("T13", "CR", "Lt hand", "左手", "N", "BP0KZZZ"),
        ("T14", "MR", "Lt knee MRI", "左膝MRI", "N", "BQ3DZZZ"),
        ("T15", "MR", "Rt knee MRI", "右膝磁振造影", "N", "BQ3CZZZ"),
        ("T16", "CR", "Pelvis", "骨盆", "N", "BW0HZZZ"),
        ("T17", "US", "Abdomen", "腹部超音波", "N", "BW40ZZZ"),
        ("T18", "US", "Liver", "肝臟超音波", "N", "BF45ZZZ"),
        ("T19", "US", "Kidney bilateral", "雙側腎臟超音波", "N", "BT45ZZZ"),
    ]

    passed = 0
    high_confidence = 0

    for value_code, modality, desc, chinese, contrast, expected in test_cases:
        result = mapper.map_study_to_icd10pcs(
            value_code=value_code,
            modality=modality,
            study_desc=desc,
            chinese_desc=chinese,
            contrast=contrast
        )

        actual = result['icd10pcs_code']
        confidence = result['mapping_confidence']

        if actual == expected:
            passed += 1
        if confidence == 'High':
            high_confidence += 1

        if actual != expected:
            print(f"  {value_code}: {desc}")
            print(f"    Expected: {expected}, Got: {actual} ({confidence})")
            print(f"    Body parts: {result['body_parts']}")

    print(f"\nICD-10-PCS Mapping Results:")
    print(f"  Passed: {passed}/{len(test_cases)} ({passed/len(test_cases)*100:.1f}%)")
    print(f"  High Confidence: {high_confidence}/{len(test_cases)} ({high_confidence/len(test_cases)*100:.1f}%)")

    return passed >= len(test_cases) * 0.9  # 90% threshold


def test_batch_processing():
    """Test batch processing with extended test file"""
    print("\n" + "="*60)
    print("BATCH PROCESSING TEST")
    print("="*60)

    from src.excel_processor import ExcelProcessor

    loinc_mapper = LOINCMapper()
    icd10pcs_mapper = ICD10PCSMapper()
    processor = ExcelProcessor()

    test_file = Path(__file__).parent / 'examples' / 'extended_test_input.csv'
    if not test_file.exists():
        print(f"  Test file not found: {test_file}")
        return False

    try:
        df = processor.read_excel(str(test_file))
        studies = processor.prepare_studies(df)
        print(f"  Loaded {len(studies)} studies from extended test file")

        loinc_results = loinc_mapper.map_batch(studies)
        icd10pcs_results = icd10pcs_mapper.map_batch(studies)

        # Calculate statistics
        loinc_mapped = sum(1 for r in loinc_results if r['loinc_code'])
        loinc_high = sum(1 for r in loinc_results if r['mapping_confidence'] == 'High')
        icd10pcs_mapped = sum(1 for r in icd10pcs_results if r['icd10pcs_code'])
        icd10pcs_high = sum(1 for r in icd10pcs_results if r['mapping_confidence'] == 'High')

        print(f"\n  LOINC Results:")
        print(f"    Mapped: {loinc_mapped}/{len(studies)} ({loinc_mapped/len(studies)*100:.1f}%)")
        print(f"    High Confidence: {loinc_high}/{len(studies)} ({loinc_high/len(studies)*100:.1f}%)")

        print(f"\n  ICD-10-PCS Results:")
        print(f"    Mapped: {icd10pcs_mapped}/{len(studies)} ({icd10pcs_mapped/len(studies)*100:.1f}%)")
        print(f"    High Confidence: {icd10pcs_high}/{len(studies)} ({icd10pcs_high/len(studies)*100:.1f}%)")

        # List unmapped studies
        unmapped_loinc = [r for r in loinc_results if not r['loinc_code']]
        if unmapped_loinc:
            print(f"\n  Unmapped LOINC studies ({len(unmapped_loinc)}):")
            for r in unmapped_loinc[:5]:  # Show first 5
                print(f"    - {r['value_code']}: {r['study_description']}")

        unmapped_icd10pcs = [r for r in icd10pcs_results if not r['icd10pcs_code']]
        if unmapped_icd10pcs:
            print(f"\n  Unmapped ICD-10-PCS studies ({len(unmapped_icd10pcs)}):")
            for r in unmapped_icd10pcs[:5]:  # Show first 5
                print(f"    - {r['value_code']}: {r['study_description']}")

        # Pass if > 80% mapped for both systems
        loinc_rate = loinc_mapped / len(studies)
        icd10pcs_rate = icd10pcs_mapped / len(studies)

        return loinc_rate >= 0.80 and icd10pcs_rate >= 0.80

    except Exception as e:
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("ENHANCED RADIOLOGY MAPPER TEST SUITE")
    print("="*60)

    results = {
        'Database Coverage': test_database_coverage(),
        'Chinese Parsing': test_parser_chinese(),
        'LOINC Mapping': test_loinc_mapping(),
        'ICD-10-PCS Mapping': test_icd10pcs_mapping(),
        'Batch Processing': test_batch_processing(),
    }

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False

    print("="*60)
    if all_passed:
        print("All tests PASSED!")
        return 0
    else:
        print("Some tests FAILED!")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
