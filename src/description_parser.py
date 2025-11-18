"""
Parser for radiology study descriptions to extract structured information
"""

import re
from typing import Dict, List, Optional, Tuple
from .medical_terminology import (
    ABBREVIATIONS, BODY_PARTS, CHINESE_BODY_PARTS,
    LATERALITY, CHINESE_LATERALITY, CONTRAST_KEYWORDS, CHINESE_CONTRAST
)


class DescriptionParser:
    """Parse radiology study descriptions to extract body parts, laterality, etc."""

    def __init__(self):
        self.abbreviations = ABBREVIATIONS
        self.body_parts = BODY_PARTS
        self.chinese_body_parts = CHINESE_BODY_PARTS
        self.laterality = LATERALITY
        self.chinese_laterality = CHINESE_LATERALITY
        self.contrast_keywords = CONTRAST_KEYWORDS
        self.chinese_contrast = CHINESE_CONTRAST

    def expand_abbreviations(self, text: str) -> str:
        """Expand medical abbreviations in text"""
        if not text:
            return ""

        expanded = text
        for abbr, full in self.abbreviations.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(abbr) + r'\b'
            expanded = re.sub(pattern, full, expanded, flags=re.IGNORECASE)

        return expanded

    def extract_body_parts(self, text: str, chinese_text: str = "") -> List[str]:
        """Extract body parts from English and Chinese descriptions"""
        body_parts = []

        if text:
            # Expand abbreviations first
            expanded_text = self.expand_abbreviations(text)
            text_lower = expanded_text.lower()

            # Extract from English text
            for keyword, standardized in self.body_parts.items():
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    if standardized not in body_parts:
                        body_parts.append(standardized)

        if chinese_text:
            # Extract from Chinese text
            for keyword, standardized in self.chinese_body_parts.items():
                if keyword in chinese_text:
                    if standardized not in body_parts:
                        body_parts.append(standardized)

        return body_parts

    def extract_laterality(self, text: str, chinese_text: str = "") -> Optional[str]:
        """Extract laterality (Right/Left/Bilateral) from descriptions"""
        laterality_found = None

        if text:
            text_lower = text.lower()
            # Check for bilateral first (higher priority)
            for keyword in ['bilateral', 'bilat', 'bil', 'both']:
                if re.search(r'\b' + keyword + r'\b', text_lower):
                    return 'Bilateral'

            # Then check for right/left
            for keyword, lat in self.laterality.items():
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    laterality_found = lat
                    break

        if chinese_text and not laterality_found:
            for keyword, lat in self.chinese_laterality.items():
                if keyword in chinese_text:
                    laterality_found = lat
                    break

        return laterality_found

    def detect_contrast_from_description(self, text: str, chinese_text: str = "") -> Optional[str]:
        """Detect contrast information from description text"""
        if text:
            text_lower = text.lower()
            for keyword, contrast_value in self.contrast_keywords.items():
                if keyword in text_lower:
                    return contrast_value

        if chinese_text:
            for keyword, contrast_value in self.chinese_contrast.items():
                if keyword in chinese_text:
                    return contrast_value

        return None

    def parse_study_description(
        self,
        study_desc: str,
        chinese_desc: str = "",
        modality: str = "",
        contrast: str = ""
    ) -> Dict:
        """
        Parse study description and extract structured information

        Args:
            study_desc: English study description
            chinese_desc: Chinese study description
            modality: Imaging modality (CT, MR, etc.)
            contrast: Contrast information (Y/N/N+Y)

        Returns:
            Dictionary with parsed information
        """
        result = {
            'original_description': study_desc,
            'chinese_description': chinese_desc,
            'expanded_description': self.expand_abbreviations(study_desc),
            'body_parts': [],
            'laterality': None,
            'modality': modality.upper() if modality else "",
            'contrast': contrast,
            'has_issues': False,
            'issues': []
        }

        # Extract body parts
        body_parts = self.extract_body_parts(study_desc, chinese_desc)
        result['body_parts'] = body_parts

        if not body_parts:
            result['has_issues'] = True
            result['issues'].append('No body part identified')

        # Extract laterality
        laterality = self.extract_laterality(study_desc, chinese_desc)
        result['laterality'] = laterality

        # Detect contrast from description if not provided
        if not contrast:
            detected_contrast = self.detect_contrast_from_description(study_desc, chinese_desc)
            if detected_contrast:
                result['contrast'] = detected_contrast

        return result

    def parse_modality_list(self, modality_str: str) -> List[str]:
        """Parse comma-separated modality list"""
        if not modality_str:
            return []

        modalities = [m.strip().upper() for m in modality_str.split(',')]
        return modalities

    def identify_primary_modality(self, modality_list: List[str]) -> str:
        """
        Identify primary modality from a list
        Priority: CT > MR > US > XA > RF > CR
        """
        if not modality_list:
            return ""

        priority_order = ['CT', 'MR', 'US', 'XA', 'RF', 'CR', 'BMD', 'OT']

        for modality in priority_order:
            if modality in modality_list:
                return modality

        return modality_list[0] if modality_list else ""
