"""
LOINC code database for radiology studies

LOINC format for radiology:
Component: [Body Part] [Laterality] [Protocol]
Method: [Modality]
"""

# Common LOINC codes for radiology studies
# Format: (body_part, modality, laterality, contrast) -> LOINC code
LOINC_DATABASE = {
    # Chest X-ray
    ('Chest', 'CR', None, 'N'): {
        'code': '36643-5',
        'long_name': 'XR Chest Views',
        'component': 'Chest',
        'method': 'XR'
    },
    ('Chest', 'XR', None, 'N'): {
        'code': '36643-5',
        'long_name': 'XR Chest Views',
        'component': 'Chest',
        'method': 'XR'
    },

    # Chest CT
    ('Chest', 'CT', None, 'N'): {
        'code': '24627-2',
        'long_name': 'CT Chest W/O contrast',
        'component': 'Chest',
        'method': 'CT'
    },
    ('Chest', 'CT', None, 'Y'): {
        'code': '24626-4',
        'long_name': 'CT Chest W contrast IV',
        'component': 'Chest',
        'method': 'CT'
    },

    # Abdomen CT
    ('Abdomen', 'CT', None, 'N'): {
        'code': '24640-5',
        'long_name': 'CT Abdomen W/O contrast',
        'component': 'Abdomen',
        'method': 'CT'
    },
    ('Abdomen', 'CT', None, 'Y'): {
        'code': '24639-7',
        'long_name': 'CT Abdomen W contrast IV',
        'component': 'Abdomen',
        'method': 'CT'
    },

    # Brain CT
    ('Brain', 'CT', None, 'N'): {
        'code': '24558-9',
        'long_name': 'CT Head W/O contrast',
        'component': 'Head',
        'method': 'CT'
    },
    ('Brain', 'CT', None, 'Y'): {
        'code': '24557-1',
        'long_name': 'CT Head W contrast IV',
        'component': 'Head',
        'method': 'CT'
    },
    ('Head', 'CT', None, 'N'): {
        'code': '24558-9',
        'long_name': 'CT Head W/O contrast',
        'component': 'Head',
        'method': 'CT'
    },
    ('Head', 'CT', None, 'Y'): {
        'code': '24557-1',
        'long_name': 'CT Head W contrast IV',
        'component': 'Head',
        'method': 'CT'
    },

    # Brain MRI
    ('Brain', 'MR', None, 'N'): {
        'code': '24556-3',
        'long_name': 'MRI Brain W/O contrast',
        'component': 'Brain',
        'method': 'MRI'
    },
    ('Brain', 'MR', None, 'Y'): {
        'code': '24555-5',
        'long_name': 'MRI Brain W contrast IV',
        'component': 'Brain',
        'method': 'MRI'
    },

    # Spine
    ('Cervical spine', 'CR', None, 'N'): {
        'code': '36713-6',
        'long_name': 'XR Cervical spine',
        'component': 'Cervical spine',
        'method': 'XR'
    },
    ('Cervical spine', 'CT', None, 'N'): {
        'code': '24800-5',
        'long_name': 'CT Cervical spine W/O contrast',
        'component': 'Cervical spine',
        'method': 'CT'
    },
    ('Cervical spine', 'MR', None, 'N'): {
        'code': '24852-6',
        'long_name': 'MRI Cervical spine W/O contrast',
        'component': 'Cervical spine',
        'method': 'MRI'
    },
    ('Lumbar spine', 'CR', None, 'N'): {
        'code': '36714-4',
        'long_name': 'XR Lumbar spine',
        'component': 'Lumbar spine',
        'method': 'XR'
    },
    ('Lumbar spine', 'CT', None, 'N'): {
        'code': '24802-1',
        'long_name': 'CT Lumbar spine W/O contrast',
        'component': 'Lumbar spine',
        'method': 'CT'
    },
    ('Lumbar spine', 'MR', None, 'N'): {
        'code': '24860-9',
        'long_name': 'MRI Lumbar spine W/O contrast',
        'component': 'Lumbar spine',
        'method': 'MRI'
    },

    # Extremities
    ('Hand', 'CR', 'Right', 'N'): {
        'code': '37362-0',
        'long_name': 'XR Hand - right',
        'component': 'Hand - right',
        'method': 'XR'
    },
    ('Hand', 'CR', 'Left', 'N'): {
        'code': '37361-2',
        'long_name': 'XR Hand - left',
        'component': 'Hand - left',
        'method': 'XR'
    },
    ('Knee', 'CR', 'Right', 'N'): {
        'code': '37628-4',
        'long_name': 'XR Knee - right',
        'component': 'Knee - right',
        'method': 'XR'
    },
    ('Knee', 'CR', 'Left', 'N'): {
        'code': '37627-6',
        'long_name': 'XR Knee - left',
        'component': 'Knee - left',
        'method': 'XR'
    },
    ('Knee', 'MR', 'Right', 'N'): {
        'code': '24876-5',
        'long_name': 'MRI Knee - right W/O contrast',
        'component': 'Knee - right',
        'method': 'MRI'
    },
    ('Knee', 'MR', 'Left', 'N'): {
        'code': '24875-7',
        'long_name': 'MRI Knee - left W/O contrast',
        'component': 'Knee - left',
        'method': 'MRI'
    },

    # Pelvis
    ('Pelvis', 'CR', None, 'N'): {
        'code': '37748-0',
        'long_name': 'XR Pelvis',
        'component': 'Pelvis',
        'method': 'XR'
    },
    ('Pelvis', 'CT', None, 'N'): {
        'code': '24907-8',
        'long_name': 'CT Pelvis W/O contrast',
        'component': 'Pelvis',
        'method': 'CT'
    },
    ('Pelvis', 'MR', None, 'N'): {
        'code': '24926-8',
        'long_name': 'MRI Pelvis W/O contrast',
        'component': 'Pelvis',
        'method': 'MRI'
    },

    # Abdomen and Pelvis
    ('Abdomen', 'CT', None, 'Y'): {
        'code': '79101-4',
        'long_name': 'CT Abdomen and Pelvis W contrast IV',
        'component': 'Abdomen and Pelvis',
        'method': 'CT'
    },

    # Ultrasound
    ('Abdomen', 'US', None, 'N'): {
        'code': '30704-1',
        'long_name': 'US Abdomen',
        'component': 'Abdomen',
        'method': 'US'
    },
    ('Liver', 'US', None, 'N'): {
        'code': '30705-8',
        'long_name': 'US Liver',
        'component': 'Liver',
        'method': 'US'
    },
    ('Kidney', 'US', None, 'N'): {
        'code': '24642-1',
        'long_name': 'US Kidney',
        'component': 'Kidney',
        'method': 'US'
    },

    # Bone density
    ('Spine', 'BMD', None, 'N'): {
        'code': '38262-7',
        'long_name': 'DXA Bone density in Spine',
        'component': 'Spine',
        'method': 'DXA'
    },
    ('Hip', 'BMD', None, 'N'): {
        'code': '38263-5',
        'long_name': 'DXA Bone density in Hip',
        'component': 'Hip',
        'method': 'DXA'
    },
}

# Modality to LOINC method mapping
MODALITY_TO_METHOD = {
    'CR': 'XR',
    'XR': 'XR',
    'CT': 'CT',
    'MR': 'MRI',
    'MRI': 'MRI',
    'US': 'US',
    'RF': 'Fluoro',
    'XA': 'Angio',
    'BMD': 'DXA',
    'OT': 'OT',
}

# Generic LOINC code patterns for common studies
GENERIC_LOINC_PATTERNS = {
    'XR': 'LP29684-5',  # Radiography
    'CT': 'LP29708-2',  # CT
    'MRI': 'LP29709-0', # MRI
    'US': 'LP29262-0',  # Ultrasound
    'Fluoro': 'LP29685-2', # Fluoroscopy
    'Angio': 'LP29263-8',  # Angiography
    'DXA': 'LP29697-7',  # DXA
}
