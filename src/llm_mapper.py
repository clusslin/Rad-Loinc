"""
LLM-based mapper for radiology studies to LOINC and ICD-10-PCS codes.

This module provides LLM-powered mapping capabilities to handle cases
that rule-based mapping cannot resolve with high confidence.
"""

import os
import json
import re
from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass

# Try to import anthropic, but make it optional
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Try to import openai as fallback
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class LLMConfig:
    """Configuration for LLM provider"""
    provider: str = "anthropic"  # "anthropic" or "openai"
    model: str = "claude-sonnet-4-20250514"  # default model
    temperature: float = 0.0  # deterministic for medical coding
    max_tokens: int = 1024
    api_key: Optional[str] = None


# System prompts for LOINC and ICD-10-PCS mapping
LOINC_SYSTEM_PROMPT = """You are a medical coding expert specializing in radiology LOINC codes.

Your task is to map radiology study descriptions (in English or Chinese) to the most appropriate LOINC code.

LOINC codes for radiology imaging follow this pattern:
- Component: Body part being imaged (e.g., "Chest", "Brain", "Knee - left")
- Method: Imaging modality (e.g., "XR", "CT", "MRI", "US")
- Contrast: With (W) or Without (W/O) contrast

Common LOINC codes for reference:
- Chest X-ray: 36643-5
- CT Head W/O contrast: 24558-9
- CT Head W contrast: 24557-1
- MRI Brain W/O contrast: 24556-3
- MRI Brain W contrast: 24555-5
- CT Chest W/O contrast: 24627-2
- CT Chest W contrast: 24626-4
- CT Abdomen W/O contrast: 24640-5
- CT Abdomen W contrast: 24639-7
- XR Cervical spine: 36713-6
- XR Lumbar spine: 36714-4
- MRI Lumbar spine W/O contrast: 24860-9
- MRI Cervical spine W/O contrast: 24852-6
- US Abdomen: 30704-1
- XR Pelvis: 37748-0
- XR Hand - right: 37362-0
- XR Hand - left: 37361-2
- XR Knee - right: 37628-4
- XR Knee - left: 37627-6
- XR Knee - bilateral: 69161-8
- MRI Knee - left W/O contrast: 24875-7
- MRI Knee - right W/O contrast: 24876-5

IMPORTANT RULES:
1. Always respond in valid JSON format
2. Include confidence level: "high", "medium", or "low"
3. For Chinese descriptions, identify the body part and modality
4. Common Chinese terms:
   - 胸部 = Chest, 腦部 = Brain, 頭部 = Head
   - 頸椎 = Cervical spine, 腰椎 = Lumbar spine
   - 膝 = Knee, 手 = Hand, 肩 = Shoulder
   - 電腦斷層 = CT, 磁振造影 = MRI, X光 = XR, 超音波 = US
   - 含對比劑 = with contrast, 無對比劑 = without contrast
   - 右 = Right, 左 = Left, 雙側 = Bilateral
"""

ICD10PCS_SYSTEM_PROMPT = """You are a medical coding expert specializing in ICD-10-PCS codes for radiology imaging.

ICD-10-PCS codes for imaging are 7 characters:
- Section B: Imaging
- Body System: 0=Central Nervous, 2=Heart, W=Chest, R=Spine, T=Urinary, etc.
- Root Type: 0=Plain Radiography, 1=Fluoroscopy, 2=CT, 3=MRI, 4=US
- Body Part: Specific anatomical region
- Contrast: 0=High, 1=Low, Y=Other, Z=None
- Qualifier: Usually Z (None)

Common ICD-10-PCS codes:
- CT Head W/O contrast: B020ZZZ
- CT Head W contrast: B0200ZZ
- MRI Brain W/O contrast: B030ZZZ
- MRI Brain W contrast: B0300ZZ
- CT Chest W/O contrast: BW24ZZZ
- CT Chest W contrast: BW240ZZ
- Plain Chest X-ray: BW03ZZZ
- CT Lumbar Spine W/O contrast: BR29ZZZ
- MRI Lumbar Spine W/O contrast: BR39ZZZ
- CT Cervical Spine W/O contrast: BR21ZZZ
- MRI Cervical Spine W/O contrast: BR31ZZZ
- US Abdomen: BW40ZZZ
- Plain Pelvis X-ray: BW01ZZZ
- CT Abdomen W contrast: BW20ZZZ

IMPORTANT RULES:
1. Always respond in valid JSON format
2. Include confidence level: "high", "medium", or "low"
3. ICD-10-PCS imaging codes always start with 'B'
4. The structure is: Section + Body System + Root Type + Body Part + Contrast + Qualifier (usually ZZ)
"""


class LLMMapper:
    """LLM-powered mapper for radiology codes"""

    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize the LLM mapper.

        Args:
            config: LLM configuration. If None, uses defaults.
        """
        self.config = config or LLMConfig()
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the LLM client based on configuration"""
        api_key = self.config.api_key or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")

        if self.config.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            anthropic_key = self.config.api_key or os.environ.get("ANTHROPIC_API_KEY")
            if anthropic_key:
                self.client = anthropic.Anthropic(api_key=anthropic_key)
            else:
                # Will use default auth if available
                self.client = anthropic.Anthropic()
        elif self.config.provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("openai package not installed. Run: pip install openai")
            openai_key = self.config.api_key or os.environ.get("OPENAI_API_KEY")
            if openai_key:
                self.client = openai.OpenAI(api_key=openai_key)
            else:
                self.client = openai.OpenAI()

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call the LLM with the given prompts.

        Args:
            system_prompt: System prompt for the LLM
            user_prompt: User prompt with the query

        Returns:
            LLM response text
        """
        if self.client is None:
            raise RuntimeError("LLM client not initialized. Check API key configuration.")

        if self.config.provider == "anthropic":
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        elif self.config.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.config.model if self.config.model != "claude-sonnet-4-20250514" else "gpt-4",
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unknown provider: {self.config.provider}")

    def _parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON from LLM response, handling potential formatting issues.

        Args:
            response: Raw LLM response text

        Returns:
            Parsed JSON as dictionary
        """
        # Try to find JSON in the response
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Try parsing the whole response
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM response", "raw_response": response}

    def map_to_loinc(
        self,
        study_description: str,
        chinese_description: str = "",
        modality: str = "",
        contrast: str = ""
    ) -> Dict:
        """
        Map a radiology study to LOINC code using LLM.

        Args:
            study_description: English study description
            chinese_description: Chinese study description (optional)
            modality: Known imaging modality (optional)
            contrast: Contrast status Y/N (optional)

        Returns:
            Dictionary with LOINC mapping results
        """
        # Build the user prompt
        prompt_parts = [f"Study Description: {study_description}"]

        if chinese_description:
            prompt_parts.append(f"Chinese Description: {chinese_description}")
        if modality:
            prompt_parts.append(f"Modality: {modality}")
        if contrast:
            contrast_text = "with contrast" if contrast == "Y" else "without contrast" if contrast == "N" else contrast
            prompt_parts.append(f"Contrast: {contrast_text}")

        prompt_parts.append("""
Please provide the LOINC code mapping in this JSON format:
{
    "loinc_code": "XXXXX-X",
    "loinc_name": "Description of the LOINC code",
    "component": "Body part",
    "method": "Imaging modality",
    "confidence": "high/medium/low",
    "reasoning": "Brief explanation of the mapping decision"
}""")

        user_prompt = "\n".join(prompt_parts)

        try:
            response = self._call_llm(LOINC_SYSTEM_PROMPT, user_prompt)
            result = self._parse_json_response(response)
            result["llm_used"] = True
            result["provider"] = self.config.provider
            return result
        except Exception as e:
            return {
                "error": str(e),
                "llm_used": True,
                "loinc_code": None,
                "confidence": "none"
            }

    def map_to_icd10pcs(
        self,
        study_description: str,
        chinese_description: str = "",
        modality: str = "",
        contrast: str = ""
    ) -> Dict:
        """
        Map a radiology study to ICD-10-PCS code using LLM.

        Args:
            study_description: English study description
            chinese_description: Chinese study description (optional)
            modality: Known imaging modality (optional)
            contrast: Contrast status Y/N (optional)

        Returns:
            Dictionary with ICD-10-PCS mapping results
        """
        # Build the user prompt
        prompt_parts = [f"Study Description: {study_description}"]

        if chinese_description:
            prompt_parts.append(f"Chinese Description: {chinese_description}")
        if modality:
            prompt_parts.append(f"Modality: {modality}")
        if contrast:
            contrast_text = "with contrast" if contrast == "Y" else "without contrast" if contrast == "N" else contrast
            prompt_parts.append(f"Contrast: {contrast_text}")

        prompt_parts.append("""
Please provide the ICD-10-PCS code mapping in this JSON format:
{
    "icd10pcs_code": "XXXXXXX",
    "description": "Description of the procedure",
    "section": "B",
    "body_system": "X",
    "root_type": "X",
    "body_part": "X",
    "contrast": "X",
    "qualifier": "X",
    "confidence": "high/medium/low",
    "reasoning": "Brief explanation of the mapping decision"
}""")

        user_prompt = "\n".join(prompt_parts)

        try:
            response = self._call_llm(ICD10PCS_SYSTEM_PROMPT, user_prompt)
            result = self._parse_json_response(response)
            result["llm_used"] = True
            result["provider"] = self.config.provider
            return result
        except Exception as e:
            return {
                "error": str(e),
                "llm_used": True,
                "icd10pcs_code": None,
                "confidence": "none"
            }

    def map_dual(
        self,
        study_description: str,
        chinese_description: str = "",
        modality: str = "",
        contrast: str = ""
    ) -> Dict:
        """
        Map a radiology study to both LOINC and ICD-10-PCS codes using LLM.

        Args:
            study_description: English study description
            chinese_description: Chinese study description (optional)
            modality: Known imaging modality (optional)
            contrast: Contrast status Y/N (optional)

        Returns:
            Dictionary with both LOINC and ICD-10-PCS mapping results
        """
        loinc_result = self.map_to_loinc(study_description, chinese_description, modality, contrast)
        icd10pcs_result = self.map_to_icd10pcs(study_description, chinese_description, modality, contrast)

        return {
            "study_description": study_description,
            "chinese_description": chinese_description,
            "modality": modality,
            "contrast": contrast,
            "loinc": loinc_result,
            "icd10pcs": icd10pcs_result
        }


class HybridMapper:
    """
    Hybrid mapper that combines rule-based and LLM-based mapping.

    First attempts rule-based mapping, and falls back to LLM for
    low-confidence or failed mappings.
    """

    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        use_llm_fallback: bool = True,
        confidence_threshold: str = "Low"
    ):
        """
        Initialize the hybrid mapper.

        Args:
            llm_config: LLM configuration
            use_llm_fallback: Whether to use LLM as fallback
            confidence_threshold: Minimum confidence to skip LLM ("High", "Low", "None")
        """
        from .loinc_mapper import LOINCMapper
        from .icd10pcs_mapper import ICD10PCSMapper

        self.loinc_mapper = LOINCMapper()
        self.icd10pcs_mapper = ICD10PCSMapper()
        self.use_llm_fallback = use_llm_fallback
        self.confidence_threshold = confidence_threshold

        self.llm_mapper = None
        if use_llm_fallback:
            try:
                self.llm_mapper = LLMMapper(llm_config)
            except Exception as e:
                print(f"Warning: LLM mapper initialization failed: {e}")
                print("Falling back to rule-based mapping only.")

    def _should_use_llm(self, confidence: str) -> bool:
        """Determine if LLM should be used based on confidence level"""
        if not self.use_llm_fallback or self.llm_mapper is None:
            return False

        confidence_levels = {"High": 3, "Medium": 2, "Low": 1, "None": 0, "Unknown": 0}
        threshold_levels = {"High": 3, "Medium": 2, "Low": 1, "None": 0}

        current_level = confidence_levels.get(confidence, 0)
        threshold_level = threshold_levels.get(self.confidence_threshold, 1)

        return current_level < threshold_level

    def map_to_loinc(
        self,
        value_code: str,
        modality: str,
        study_desc: str,
        chinese_desc: str = "",
        contrast: str = "",
        combine_modality: str = ""
    ) -> Dict:
        """
        Map a study to LOINC code using hybrid approach.

        First tries rule-based mapping, then uses LLM if needed.
        """
        # Try rule-based mapping first
        result = self.loinc_mapper.map_study_to_loinc(
            value_code, modality, study_desc, chinese_desc, contrast, combine_modality
        )

        result["llm_used"] = False
        result["mapping_method"] = "rule-based"

        # Check if LLM fallback is needed
        if self._should_use_llm(result.get("mapping_confidence", "None")):
            llm_result = self.llm_mapper.map_to_loinc(
                study_desc, chinese_desc, modality, contrast
            )

            if llm_result.get("loinc_code") and llm_result.get("confidence") != "none":
                # Update with LLM results
                result["loinc_code"] = llm_result.get("loinc_code")
                result["loinc_long_name"] = llm_result.get("loinc_name")
                result["loinc_component"] = llm_result.get("component")
                result["loinc_method"] = llm_result.get("method")
                result["mapping_confidence"] = llm_result.get("confidence", "Medium").title()
                result["llm_used"] = True
                result["mapping_method"] = "llm"
                result["llm_reasoning"] = llm_result.get("reasoning", "")

                # Remove the "No LOINC code found" issue if LLM found one
                result["issues"] = [i for i in result.get("issues", [])
                                   if "No LOINC code found" not in i]
                if not result["issues"]:
                    result["has_issues"] = False

        return result

    def map_to_icd10pcs(
        self,
        value_code: str,
        modality: str,
        study_desc: str,
        chinese_desc: str = "",
        contrast: str = "",
        combine_modality: str = ""
    ) -> Dict:
        """
        Map a study to ICD-10-PCS code using hybrid approach.

        First tries rule-based mapping, then uses LLM if needed.
        """
        # Try rule-based mapping first
        result = self.icd10pcs_mapper.map_study_to_icd10pcs(
            value_code, modality, study_desc, chinese_desc, contrast, combine_modality
        )

        result["llm_used"] = False
        result["mapping_method"] = "rule-based"

        # Check if LLM fallback is needed
        if self._should_use_llm(result.get("mapping_confidence", "None")):
            llm_result = self.llm_mapper.map_to_icd10pcs(
                study_desc, chinese_desc, modality, contrast
            )

            if llm_result.get("icd10pcs_code") and llm_result.get("confidence") != "none":
                # Update with LLM results
                result["icd10pcs_code"] = llm_result.get("icd10pcs_code")
                result["icd10pcs_description"] = llm_result.get("description")
                result["icd10pcs_section"] = llm_result.get("section")
                result["icd10pcs_body_system"] = llm_result.get("body_system")
                result["icd10pcs_root_type"] = llm_result.get("root_type")
                result["icd10pcs_body_part"] = llm_result.get("body_part")
                result["mapping_confidence"] = llm_result.get("confidence", "Medium").title()
                result["llm_used"] = True
                result["mapping_method"] = "llm"
                result["llm_reasoning"] = llm_result.get("reasoning", "")

                # Remove the "No ICD-10-PCS code found" issue if LLM found one
                result["issues"] = [i for i in result.get("issues", [])
                                   if "No ICD-10-PCS code found" not in i]
                if not result["issues"]:
                    result["has_issues"] = False

        return result

    def map_dual(
        self,
        value_code: str,
        modality: str,
        study_desc: str,
        chinese_desc: str = "",
        contrast: str = "",
        combine_modality: str = ""
    ) -> Dict:
        """
        Map a study to both LOINC and ICD-10-PCS codes using hybrid approach.
        """
        loinc_result = self.map_to_loinc(
            value_code, modality, study_desc, chinese_desc, contrast, combine_modality
        )
        icd10pcs_result = self.map_to_icd10pcs(
            value_code, modality, study_desc, chinese_desc, contrast, combine_modality
        )

        # Merge results
        result = {
            "value_code": value_code,
            "modality": modality,
            "study_description": study_desc,
            "chinese_description": chinese_desc,
            "contrast": contrast,
            "combine_modality": combine_modality,
            "primary_modality": loinc_result.get("primary_modality"),
            "body_parts": loinc_result.get("body_parts"),
            "laterality": loinc_result.get("laterality"),
            # LOINC fields
            "loinc_code": loinc_result.get("loinc_code"),
            "loinc_long_name": loinc_result.get("loinc_long_name"),
            "loinc_component": loinc_result.get("loinc_component"),
            "loinc_method": loinc_result.get("loinc_method"),
            "loinc_confidence": loinc_result.get("mapping_confidence"),
            "loinc_llm_used": loinc_result.get("llm_used"),
            # ICD-10-PCS fields
            "icd10pcs_code": icd10pcs_result.get("icd10pcs_code"),
            "icd10pcs_description": icd10pcs_result.get("icd10pcs_description"),
            "icd10pcs_section": icd10pcs_result.get("icd10pcs_section"),
            "icd10pcs_body_system": icd10pcs_result.get("icd10pcs_body_system"),
            "icd10pcs_root_type": icd10pcs_result.get("icd10pcs_root_type"),
            "icd10pcs_confidence": icd10pcs_result.get("mapping_confidence"),
            "icd10pcs_llm_used": icd10pcs_result.get("llm_used"),
            # Combined
            "issues": list(set(loinc_result.get("issues", []) + icd10pcs_result.get("issues", []))),
            "has_issues": loinc_result.get("has_issues") or icd10pcs_result.get("has_issues"),
        }

        return result

    def map_batch(self, studies: List[Dict], code_type: str = "dual") -> List[Dict]:
        """
        Map multiple studies using hybrid approach.

        Args:
            studies: List of study dictionaries
            code_type: "loinc", "icd10pcs", or "dual"

        Returns:
            List of mapping results
        """
        results = []
        for study in studies:
            if code_type == "loinc":
                result = self.map_to_loinc(
                    value_code=study.get('value_code', ''),
                    modality=study.get('modality', ''),
                    study_desc=study.get('Study Description', ''),
                    chinese_desc=study.get('Chinese Study Description', ''),
                    contrast=study.get('Contrast', ''),
                    combine_modality=study.get('Combine Modality', '')
                )
            elif code_type == "icd10pcs":
                result = self.map_to_icd10pcs(
                    value_code=study.get('value_code', ''),
                    modality=study.get('modality', ''),
                    study_desc=study.get('Study Description', ''),
                    chinese_desc=study.get('Chinese Study Description', ''),
                    contrast=study.get('Contrast', ''),
                    combine_modality=study.get('Combine Modality', '')
                )
            else:  # dual
                result = self.map_dual(
                    value_code=study.get('value_code', ''),
                    modality=study.get('modality', ''),
                    study_desc=study.get('Study Description', ''),
                    chinese_desc=study.get('Chinese Study Description', ''),
                    contrast=study.get('Contrast', ''),
                    combine_modality=study.get('Combine Modality', '')
                )
            results.append(result)
        return results


def check_llm_availability() -> Dict[str, bool]:
    """Check which LLM providers are available"""
    available = {
        "anthropic_package": HAS_ANTHROPIC,
        "openai_package": HAS_OPENAI,
        "anthropic_api_key": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "openai_api_key": bool(os.environ.get("OPENAI_API_KEY")),
    }
    available["any_available"] = (
        (available["anthropic_package"] and available["anthropic_api_key"]) or
        (available["openai_package"] and available["openai_api_key"])
    )
    return available
