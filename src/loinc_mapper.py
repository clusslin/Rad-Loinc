"""
LOINC code mapper for radiology studies
"""

from typing import Dict, Optional, List, Tuple
from .loinc_database import LOINC_DATABASE, MODALITY_TO_METHOD, GENERIC_LOINC_PATTERNS
from .description_parser import DescriptionParser


class LOINCMapper:
    """Map radiology studies to LOINC codes"""

    def __init__(self):
        self.loinc_db = LOINC_DATABASE
        self.modality_map = MODALITY_TO_METHOD
        self.generic_patterns = GENERIC_LOINC_PATTERNS
        self.parser = DescriptionParser()

    def normalize_modality(self, modality: str) -> str:
        """Convert modality to LOINC method"""
        if not modality:
            return ""
        modality_upper = modality.upper()
        return self.modality_map.get(modality_upper, modality_upper)

    def find_loinc_code(
        self,
        body_part: str,
        modality: str,
        laterality: Optional[str] = None,
        contrast: str = "N"
    ) -> Optional[Dict]:
        """
        Find LOINC code based on study parameters

        Args:
            body_part: Anatomical body part
            modality: Imaging modality
            laterality: Right/Left/Bilateral
            contrast: Y/N/N+Y

        Returns:
            Dictionary with LOINC code and metadata, or None if not found
        """
        # Normalize modality
        method = self.normalize_modality(modality)

        # Handle contrast variations
        contrast_values = []
        if contrast == 'Y':
            contrast_values = ['Y']
        elif contrast == 'N':
            contrast_values = ['N']
        elif contrast == 'N+Y':
            contrast_values = ['Y', 'N']  # Try with contrast first
        else:
            contrast_values = ['N', 'Y']  # Default try both

        # Try to find exact match
        for contrast_val in contrast_values:
            # Try with laterality first
            if laterality:
                key = (body_part, method, laterality, contrast_val)
                if key in self.loinc_db:
                    return self.loinc_db[key].copy()

            # Try without laterality
            key = (body_part, method, None, contrast_val)
            if key in self.loinc_db:
                return self.loinc_db[key].copy()

        return None

    def map_study_to_loinc(
        self,
        value_code: str,
        modality: str,
        study_desc: str,
        chinese_desc: str = "",
        contrast: str = "",
        combine_modality: str = ""
    ) -> Dict:
        """
        Map a radiology study to LOINC code

        Args:
            value_code: Internal code
            modality: Primary modality
            study_desc: English study description
            chinese_desc: Chinese study description
            contrast: Contrast information (Y/N/N+Y)
            combine_modality: Comma-separated modalities

        Returns:
            Dictionary with mapping results and metadata
        """
        # Parse the study description
        parsed = self.parser.parse_study_description(
            study_desc, chinese_desc, modality, contrast
        )

        # Handle combined modalities
        modality_list = []
        if combine_modality:
            modality_list = self.parser.parse_modality_list(combine_modality)
        else:
            modality_list = [modality] if modality else []

        # Identify primary modality
        primary_modality = self.parser.identify_primary_modality(modality_list)
        if not primary_modality:
            primary_modality = modality

        result = {
            'value_code': value_code,
            'modality': modality,
            'combine_modality': combine_modality,
            'primary_modality': primary_modality,
            'study_description': study_desc,
            'chinese_description': chinese_desc,
            'expanded_description': parsed['expanded_description'],
            'body_parts': parsed['body_parts'],
            'laterality': parsed['laterality'],
            'contrast': contrast,
            'loinc_code': None,
            'loinc_long_name': None,
            'loinc_component': None,
            'loinc_method': None,
            'mapping_confidence': 'Unknown',
            'issues': parsed['issues'].copy(),
            'has_issues': parsed['has_issues']
        }

        # Try to find LOINC code for each body part
        loinc_codes = []
        for body_part in parsed['body_parts']:
            loinc_info = self.find_loinc_code(
                body_part,
                primary_modality,
                parsed['laterality'],
                contrast
            )
            if loinc_info:
                loinc_codes.append((body_part, loinc_info))

        if loinc_codes:
            # Use the first match (most specific)
            body_part, loinc_info = loinc_codes[0]
            result['loinc_code'] = loinc_info['code']
            result['loinc_long_name'] = loinc_info['long_name']
            result['loinc_component'] = loinc_info['component']
            result['loinc_method'] = loinc_info['method']
            result['mapping_confidence'] = 'High'

            if len(loinc_codes) > 1:
                result['issues'].append('Multiple LOINC codes possible')
                result['has_issues'] = True
        else:
            # Try to provide a generic LOINC pattern
            method = self.normalize_modality(primary_modality)
            if method in self.generic_patterns:
                result['loinc_code'] = self.generic_patterns[method]
                result['loinc_long_name'] = f'Generic {method} study'
                result['loinc_method'] = method
                result['mapping_confidence'] = 'Low'
                result['issues'].append('Using generic LOINC code - specific code not found')
                result['has_issues'] = True
            else:
                result['issues'].append('No LOINC code found')
                result['has_issues'] = True
                result['mapping_confidence'] = 'None'

        # Additional validation
        if not parsed['body_parts']:
            result['issues'].append('No body part identified')
            result['has_issues'] = True

        if combine_modality and ',' in combine_modality:
            result['issues'].append('Multiple modalities - used primary modality for LOINC mapping')

        if contrast == 'N+Y':
            result['issues'].append('Both contrast and non-contrast - LOINC code may need separate entries')

        return result

    def map_batch(self, studies: List[Dict]) -> List[Dict]:
        """
        Map multiple studies to LOINC codes

        Args:
            studies: List of dictionaries with study information

        Returns:
            List of mapping results
        """
        results = []
        for study in studies:
            result = self.map_study_to_loinc(
                value_code=study.get('value_code', ''),
                modality=study.get('modality', ''),
                study_desc=study.get('Study Description', ''),
                chinese_desc=study.get('Chinese Study Description', ''),
                contrast=study.get('Contrast', ''),
                combine_modality=study.get('Combine Modality', '')
            )
            results.append(result)
        return results
