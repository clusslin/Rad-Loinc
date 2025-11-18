"""
ICD-10-PCS code mapper for radiology procedures
"""

from typing import Dict, Optional, List, Tuple
from .icd10pcs_database import ICD10PCS_DATABASE, MODALITY_TO_ROOT_TYPE
from .description_parser import DescriptionParser


class ICD10PCSMapper:
    """Map radiology studies to ICD-10-PCS codes"""

    def __init__(self):
        self.icd10pcs_db = ICD10PCS_DATABASE
        self.modality_map = MODALITY_TO_ROOT_TYPE
        self.parser = DescriptionParser()

    def normalize_modality(self, modality: str) -> str:
        """Convert modality to ICD-10-PCS root type"""
        if not modality:
            return ""
        modality_upper = modality.upper()
        return self.modality_map.get(modality_upper, "")

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

    def _select_best_icd10pcs(self, icd10pcs_codes: List[Tuple[str, Dict]], body_parts: List[str]) -> Tuple[str, Dict]:
        """
        Select the best ICD-10-PCS code from multiple matches

        Prioritizes more specific anatomical terms

        Args:
            icd10pcs_codes: List of (body_part, icd10pcs_info) tuples
            body_parts: Original list of body parts

        Returns:
            Best (body_part, icd10pcs_info) tuple
        """
        if len(icd10pcs_codes) == 1:
            return icd10pcs_codes[0]

        # Priority order for specific terms
        priority_keywords = [
            'Cervical spine', 'Thoracic spine', 'Lumbar spine', 'Lumbosacral spine',
            'Coronary artery', 'Carotid artery', 'Renal artery',
            'Left', 'Right', 'Bilateral'
        ]

        # First, try priority keywords
        for keyword in priority_keywords:
            for body_part, icd10pcs_info in icd10pcs_codes:
                if keyword.lower() in body_part.lower():
                    return (body_part, icd10pcs_info)

        # Prefer longer/more specific terms
        sorted_codes = sorted(icd10pcs_codes, key=lambda x: len(x[0]), reverse=True)
        return sorted_codes[0]

    def find_icd10pcs_code(
        self,
        body_part: str,
        modality: str,
        laterality: Optional[str] = None,
        contrast: str = "N"
    ) -> Optional[Dict]:
        """
        Find ICD-10-PCS code based on study parameters

        Args:
            body_part: Anatomical body part
            modality: Imaging modality
            laterality: Right/Left/Bilateral
            contrast: Y/N/N+Y

        Returns:
            Dictionary with ICD-10-PCS code and metadata, or None if not found
        """
        # Normalize modality
        root_type = self.normalize_modality(modality)

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
                key = (body_part, modality, laterality, contrast_val)
                if key in self.icd10pcs_db:
                    return self.icd10pcs_db[key].copy()

            # Try without laterality
            key = (body_part, modality, None, contrast_val)
            if key in self.icd10pcs_db:
                return self.icd10pcs_db[key].copy()

        return None

    def map_study_to_icd10pcs(
        self,
        value_code: str,
        modality: str,
        study_desc: str,
        chinese_desc: str = "",
        contrast: str = "",
        combine_modality: str = ""
    ) -> Dict:
        """
        Map a radiology study to ICD-10-PCS code

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
            'icd10pcs_code': None,
            'icd10pcs_description': None,
            'icd10pcs_section': None,
            'icd10pcs_body_system': None,
            'icd10pcs_root_type': None,
            'icd10pcs_body_part': None,
            'mapping_confidence': 'Unknown',
            'issues': parsed['issues'].copy(),
            'has_issues': parsed['has_issues']
        }

        # Try to find ICD-10-PCS code for each body part
        icd10pcs_codes = []
        for body_part in filtered_body_parts:
            icd10pcs_info = self.find_icd10pcs_code(
                body_part,
                primary_modality,
                parsed['laterality'],
                contrast
            )
            if icd10pcs_info:
                icd10pcs_codes.append((body_part, icd10pcs_info))

        if icd10pcs_codes:
            # Use the best match (most specific)
            body_part, icd10pcs_info = self._select_best_icd10pcs(icd10pcs_codes, filtered_body_parts)
            result['icd10pcs_code'] = icd10pcs_info['code']
            result['icd10pcs_description'] = icd10pcs_info['description']
            result['icd10pcs_section'] = icd10pcs_info['section']
            result['icd10pcs_body_system'] = icd10pcs_info['body_system']
            result['icd10pcs_root_type'] = icd10pcs_info['root_type']
            result['icd10pcs_body_part'] = icd10pcs_info['body_part']
            result['mapping_confidence'] = 'High'

            if len(icd10pcs_codes) > 1:
                result['issues'].append('Multiple ICD-10-PCS codes possible')
                result['has_issues'] = True
        else:
            result['issues'].append('No ICD-10-PCS code found')
            result['has_issues'] = True
            result['mapping_confidence'] = 'None'

        # Additional validation
        if not filtered_body_parts:
            result['issues'].append('No body part identified')
            result['has_issues'] = True

        if combine_modality and ',' in combine_modality:
            result['issues'].append('Multiple modalities - used primary modality for ICD-10-PCS mapping')

        if contrast == 'N+Y':
            result['issues'].append('Both contrast and non-contrast - ICD-10-PCS code may need separate entries')

        return result

    def map_batch(self, studies: List[Dict]) -> List[Dict]:
        """
        Map multiple studies to ICD-10-PCS codes

        Args:
            studies: List of dictionaries with study information

        Returns:
            List of mapping results
        """
        results = []
        for study in studies:
            result = self.map_study_to_icd10pcs(
                value_code=study.get('value_code', ''),
                modality=study.get('modality', ''),
                study_desc=study.get('Study Description', ''),
                chinese_desc=study.get('Chinese Study Description', ''),
                contrast=study.get('Contrast', ''),
                combine_modality=study.get('Combine Modality', '')
            )
            results.append(result)
        return results
