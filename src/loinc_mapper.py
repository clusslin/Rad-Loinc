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

    def _filter_body_parts(self, body_parts: List[str]) -> List[str]:
        """
        Filter out non-specific or false positive body parts

        Args:
            body_parts: List of identified body parts

        Returns:
            Filtered list of body parts
        """
        # Body parts to exclude (often false positives from abbreviations)
        exclude_list = ['Face', 'Bone']

        filtered = []
        for part in body_parts:
            if part not in exclude_list:
                filtered.append(part)

        # If filtering removed everything, keep original list
        if not filtered and body_parts:
            return body_parts

        return filtered

    def _select_best_loinc(self, loinc_codes: List[Tuple[str, Dict]], body_parts: List[str]) -> Tuple[str, Dict]:
        """
        Select the best LOINC code from multiple matches

        Prioritizes more specific anatomical terms

        Args:
            loinc_codes: List of (body_part, loinc_info) tuples
            body_parts: Original list of body parts

        Returns:
            Best (body_part, loinc_info) tuple
        """
        if len(loinc_codes) == 1:
            return loinc_codes[0]

        # Priority order for specific terms
        priority_keywords = [
            'Cervical spine', 'Thoracic spine', 'Lumbar spine', 'Lumbosacral spine',
            'Coronary artery', 'Carotid artery', 'Renal artery',
            'Left', 'Right', 'Bilateral'
        ]

        # First, try priority keywords
        for keyword in priority_keywords:
            for body_part, loinc_info in loinc_codes:
                if keyword.lower() in body_part.lower():
                    return (body_part, loinc_info)

        # Prefer longer/more specific terms
        sorted_codes = sorted(loinc_codes, key=lambda x: len(x[0]), reverse=True)
        return sorted_codes[0]

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

        # Filter out non-specific body parts that might be false positives
        filtered_body_parts = self._filter_body_parts(parsed['body_parts'])

        result = {
            'value_code': value_code,
            'modality': modality,
            'combine_modality': combine_modality,
            'primary_modality': primary_modality,
            'study_description': study_desc,
            'chinese_description': chinese_desc,
            'expanded_description': parsed['expanded_description'],
            'body_parts': filtered_body_parts,
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
        for body_part in filtered_body_parts:
            loinc_info = self.find_loinc_code(
                body_part,
                primary_modality,
                parsed['laterality'],
                contrast
            )
            if loinc_info:
                loinc_codes.append((body_part, loinc_info))

        if loinc_codes:
            # Use the best match (most specific)
            body_part, loinc_info = self._select_best_loinc(loinc_codes, filtered_body_parts)
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
        if not filtered_body_parts:
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
