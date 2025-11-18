"""
ICD-10-PCS code database for radiology imaging procedures

ICD-10-PCS Imaging Section Structure (7 characters):
- Character 1: Section (B = Imaging)
- Character 2: Body System
- Character 3: Root Type (Modality)
- Character 4: Body Part
- Character 5: Contrast
- Character 6: Qualifier
- Character 7: Qualifier

Root Types (Character 3):
- 0: Plain Radiography (XR/CR)
- 1: Fluoroscopy (RF)
- 2: Computerized Tomography (CT)
- 3: Magnetic Resonance Imaging (MRI)
- 4: Ultrasonography (US)

Contrast (Character 5):
- 0: High Osmolar
- 1: Low Osmolar
- Y: Other Contrast
- Z: None

Qualifiers (Characters 6-7):
- 0: Unenhanced and Enhanced
- 1: Laser
- Z: None
"""

# ICD-10-PCS codes for common radiology procedures
# Format: (body_part, modality, laterality, contrast) -> ICD-10-PCS code
ICD10PCS_DATABASE = {
    # Central Nervous System (B0)
    # Brain
    ('Brain', 'CT', None, 'N'): {
        'code': 'B020ZZZ',
        'description': 'CT Brain without contrast',
        'section': 'B',
        'body_system': '0',
        'root_type': '2',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Brain', 'CT', None, 'Y'): {
        'code': 'B0200ZZ',
        'description': 'CT Brain with contrast, unenhanced and enhanced',
        'section': 'B',
        'body_system': '0',
        'root_type': '2',
        'body_part': '0',
        'contrast': '0',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Brain', 'MR', None, 'N'): {
        'code': 'B030ZZZ',
        'description': 'MRI Brain without contrast',
        'section': 'B',
        'body_system': '0',
        'root_type': '3',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Brain', 'MR', None, 'Y'): {
        'code': 'B0300ZZ',
        'description': 'MRI Brain with contrast, unenhanced and enhanced',
        'section': 'B',
        'body_system': '0',
        'root_type': '3',
        'body_part': '0',
        'contrast': '0',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Brain', 'MRI', None, 'N'): {
        'code': 'B030ZZZ',
        'description': 'MRI Brain without contrast',
        'section': 'B',
        'body_system': '0',
        'root_type': '3',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Brain', 'MRI', None, 'Y'): {
        'code': 'B0300ZZ',
        'description': 'MRI Brain with contrast, unenhanced and enhanced',
        'section': 'B',
        'body_system': '0',
        'root_type': '3',
        'body_part': '0',
        'contrast': '0',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Chest (BW)
    ('Chest', 'CR', None, 'N'): {
        'code': 'BW03ZZZ',
        'description': 'Plain Radiography Chest',
        'section': 'B',
        'body_system': 'W',
        'root_type': '0',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Chest', 'XR', None, 'N'): {
        'code': 'BW03ZZZ',
        'description': 'Plain Radiography Chest',
        'section': 'B',
        'body_system': 'W',
        'root_type': '0',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Chest', 'CT', None, 'N'): {
        'code': 'BW24ZZZ',
        'description': 'CT Chest without contrast',
        'section': 'B',
        'body_system': 'W',
        'root_type': '2',
        'body_part': '4',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Chest', 'CT', None, 'Y'): {
        'code': 'BW240ZZ',
        'description': 'CT Chest with contrast',
        'section': 'B',
        'body_system': 'W',
        'root_type': '2',
        'body_part': '4',
        'contrast': '0',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Spine (BR)
    # Cervical Spine
    ('Cervical spine', 'CR', None, 'N'): {
        'code': 'BR00ZZZ',
        'description': 'Plain Radiography Cervical Spine',
        'section': 'B',
        'body_system': 'R',
        'root_type': '0',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Cervical spine', 'XR', None, 'N'): {
        'code': 'BR00ZZZ',
        'description': 'Plain Radiography Cervical Spine',
        'section': 'B',
        'body_system': 'R',
        'root_type': '0',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Cervical spine', 'CT', None, 'N'): {
        'code': 'BR20ZZZ',
        'description': 'CT Cervical Spine without contrast',
        'section': 'B',
        'body_system': 'R',
        'root_type': '2',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Cervical spine', 'MR', None, 'N'): {
        'code': 'BR30ZZZ',
        'description': 'MRI Cervical Spine without contrast',
        'section': 'B',
        'body_system': 'R',
        'root_type': '3',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Cervical spine', 'MRI', None, 'N'): {
        'code': 'BR30ZZZ',
        'description': 'MRI Cervical Spine without contrast',
        'section': 'B',
        'body_system': 'R',
        'root_type': '3',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Lumbar Spine
    ('Lumbar spine', 'CR', None, 'N'): {
        'code': 'BR03ZZZ',
        'description': 'Plain Radiography Lumbar Spine',
        'section': 'B',
        'body_system': 'R',
        'root_type': '0',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Lumbar spine', 'XR', None, 'N'): {
        'code': 'BR03ZZZ',
        'description': 'Plain Radiography Lumbar Spine',
        'section': 'B',
        'body_system': 'R',
        'root_type': '0',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Lumbar spine', 'CT', None, 'N'): {
        'code': 'BR23ZZZ',
        'description': 'CT Lumbar Spine without contrast',
        'section': 'B',
        'body_system': 'R',
        'root_type': '2',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Lumbar spine', 'MR', None, 'N'): {
        'code': 'BR33ZZZ',
        'description': 'MRI Lumbar Spine without contrast',
        'section': 'B',
        'body_system': 'R',
        'root_type': '3',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Lumbar spine', 'MRI', None, 'N'): {
        'code': 'BR33ZZZ',
        'description': 'MRI Lumbar Spine without contrast',
        'section': 'B',
        'body_system': 'R',
        'root_type': '3',
        'body_part': '3',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Upper Extremities (BP)
    # Hand
    ('Hand', 'CR', 'Right', 'N'): {
        'code': 'BP0JZZZ',
        'description': 'Plain Radiography Right Hand',
        'section': 'B',
        'body_system': 'P',
        'root_type': '0',
        'body_part': 'J',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Hand', 'XR', 'Right', 'N'): {
        'code': 'BP0JZZZ',
        'description': 'Plain Radiography Right Hand',
        'section': 'B',
        'body_system': 'P',
        'root_type': '0',
        'body_part': 'J',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Hand', 'CR', 'Left', 'N'): {
        'code': 'BP0KZZZ',
        'description': 'Plain Radiography Left Hand',
        'section': 'B',
        'body_system': 'P',
        'root_type': '0',
        'body_part': 'K',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Hand', 'XR', 'Left', 'N'): {
        'code': 'BP0KZZZ',
        'description': 'Plain Radiography Left Hand',
        'section': 'B',
        'body_system': 'P',
        'root_type': '0',
        'body_part': 'K',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Lower Extremities (BQ)
    # Knee
    ('Knee', 'CR', 'Right', 'N'): {
        'code': 'BQ0CZZZ',
        'description': 'Plain Radiography Right Knee',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '0',
        'body_part': 'C',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'XR', 'Right', 'N'): {
        'code': 'BQ0CZZZ',
        'description': 'Plain Radiography Right Knee',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '0',
        'body_part': 'C',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'CR', 'Left', 'N'): {
        'code': 'BQ0DZZZ',
        'description': 'Plain Radiography Left Knee',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '0',
        'body_part': 'D',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'XR', 'Left', 'N'): {
        'code': 'BQ0DZZZ',
        'description': 'Plain Radiography Left Knee',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '0',
        'body_part': 'D',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'CR', 'Bilateral', 'N'): {
        'code': 'BQ09ZZZ',
        'description': 'Plain Radiography Bilateral Knees',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '0',
        'body_part': '9',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'XR', 'Bilateral', 'N'): {
        'code': 'BQ09ZZZ',
        'description': 'Plain Radiography Bilateral Knees',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '0',
        'body_part': '9',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'MR', 'Right', 'N'): {
        'code': 'BQ3CZZZ',
        'description': 'MRI Right Knee without contrast',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '3',
        'body_part': 'C',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'MRI', 'Right', 'N'): {
        'code': 'BQ3CZZZ',
        'description': 'MRI Right Knee without contrast',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '3',
        'body_part': 'C',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'MR', 'Left', 'N'): {
        'code': 'BQ3DZZZ',
        'description': 'MRI Left Knee without contrast',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '3',
        'body_part': 'D',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Knee', 'MRI', 'Left', 'N'): {
        'code': 'BQ3DZZZ',
        'description': 'MRI Left Knee without contrast',
        'section': 'B',
        'body_system': 'Q',
        'root_type': '3',
        'body_part': 'D',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Abdomen (BW)
    ('Abdomen', 'CT', None, 'N'): {
        'code': 'BW20ZZZ',
        'description': 'CT Abdomen without contrast',
        'section': 'B',
        'body_system': 'W',
        'root_type': '2',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Abdomen', 'CT', None, 'Y'): {
        'code': 'BW200ZZ',
        'description': 'CT Abdomen with contrast',
        'section': 'B',
        'body_system': 'W',
        'root_type': '2',
        'body_part': '0',
        'contrast': '0',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Abdomen', 'US', None, 'N'): {
        'code': 'BW40ZZZ',
        'description': 'Ultrasonography Abdomen',
        'section': 'B',
        'body_system': 'W',
        'root_type': '4',
        'body_part': '0',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Pelvis (BW)
    ('Pelvis', 'CR', None, 'N'): {
        'code': 'BW0HZZZ',
        'description': 'Plain Radiography Pelvis',
        'section': 'B',
        'body_system': 'W',
        'root_type': '0',
        'body_part': 'H',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Pelvis', 'XR', None, 'N'): {
        'code': 'BW0HZZZ',
        'description': 'Plain Radiography Pelvis',
        'section': 'B',
        'body_system': 'W',
        'root_type': '0',
        'body_part': 'H',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Pelvis', 'CT', None, 'N'): {
        'code': 'BW2GZZZ',
        'description': 'CT Pelvis without contrast',
        'section': 'B',
        'body_system': 'W',
        'root_type': '2',
        'body_part': 'G',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Hepatobiliary System and Pancreas (BF)
    ('Liver', 'US', None, 'N'): {
        'code': 'BF45ZZZ',
        'description': 'Ultrasonography Liver',
        'section': 'B',
        'body_system': 'F',
        'root_type': '4',
        'body_part': '5',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Urinary System (BT)
    ('Kidney', 'US', None, 'N'): {
        'code': 'BT45ZZZ',
        'description': 'Ultrasonography Kidney',
        'section': 'B',
        'body_system': 'T',
        'root_type': '4',
        'body_part': '5',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Kidney', 'US', 'Bilateral', 'N'): {
        'code': 'BT45ZZZ',
        'description': 'Ultrasonography Bilateral Kidneys',
        'section': 'B',
        'body_system': 'T',
        'root_type': '4',
        'body_part': '5',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Kidney', 'CT', None, 'N'): {
        'code': 'BT25ZZZ',
        'description': 'CT Kidney without contrast',
        'section': 'B',
        'body_system': 'T',
        'root_type': '2',
        'body_part': '5',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Ureter', 'CT', None, 'N'): {
        'code': 'BT26ZZZ',
        'description': 'CT Ureter without contrast',
        'section': 'B',
        'body_system': 'T',
        'root_type': '2',
        'body_part': '6',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Bladder', 'CT', None, 'N'): {
        'code': 'BT27ZZZ',
        'description': 'CT Bladder without contrast',
        'section': 'B',
        'body_system': 'T',
        'root_type': '2',
        'body_part': '7',
        'contrast': 'Z',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },

    # Heart (B2)
    ('Heart', 'XA', None, 'Y'): {
        'code': 'B2161ZZ',
        'description': 'Fluoroscopy Heart with contrast',
        'section': 'B',
        'body_system': '2',
        'root_type': '1',
        'body_part': '6',
        'contrast': '1',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
    ('Coronary artery', 'XA', None, 'Y'): {
        'code': 'B2101ZZ',
        'description': 'Fluoroscopy Coronary Arteries with contrast',
        'section': 'B',
        'body_system': '2',
        'root_type': '1',
        'body_part': '0',
        'contrast': '1',
        'qualifier1': 'Z',
        'qualifier2': 'Z'
    },
}

# Modality to ICD-10-PCS Root Type mapping
MODALITY_TO_ROOT_TYPE = {
    'CR': '0',  # Plain Radiography
    'XR': '0',  # Plain Radiography
    'RF': '1',  # Fluoroscopy
    'XA': '1',  # Fluoroscopy/Angiography
    'CT': '2',  # Computerized Tomography
    'MR': '3',  # Magnetic Resonance Imaging
    'MRI': '3', # Magnetic Resonance Imaging
    'US': '4',  # Ultrasonography
}
