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
    ('Brain', 'MRI', None, 'Y'): {
        'code': '24555-5',
        'long_name': 'MRI Brain W contrast IV',
        'component': 'Brain',
        'method': 'MRI'
    },
    ('Brain', 'MRI', None, 'N'): {
        'code': '24556-3',
        'long_name': 'MRI Brain W/O contrast',
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
    ('Cervical spine', 'MRI', None, 'N'): {
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
    ('Lumbar spine', 'XR', None, 'N'): {
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
    ('Lumbar spine', 'MRI', None, 'N'): {
        'code': '24860-9',
        'long_name': 'MRI Lumbar spine W/O contrast',
        'component': 'Lumbar spine',
        'method': 'MRI'
    },

    # Extremities - Hand
    ('Hand', 'CR', 'Right', 'N'): {
        'code': '37362-0',
        'long_name': 'XR Hand - right',
        'component': 'Hand - right',
        'method': 'XR'
    },
    ('Hand', 'XR', 'Right', 'N'): {
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
    ('Hand', 'XR', 'Left', 'N'): {
        'code': '37361-2',
        'long_name': 'XR Hand - left',
        'component': 'Hand - left',
        'method': 'XR'
    },
    # Extremities - Knee
    ('Knee', 'CR', 'Right', 'N'): {
        'code': '37628-4',
        'long_name': 'XR Knee - right',
        'component': 'Knee - right',
        'method': 'XR'
    },
    ('Knee', 'XR', 'Right', 'N'): {
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
    ('Knee', 'XR', 'Left', 'N'): {
        'code': '37627-6',
        'long_name': 'XR Knee - left',
        'component': 'Knee - left',
        'method': 'XR'
    },
    ('Knee', 'CR', 'Bilateral', 'N'): {
        'code': '69161-8',
        'long_name': 'XR Knee - bilateral',
        'component': 'Knee - bilateral',
        'method': 'XR'
    },
    ('Knee', 'XR', 'Bilateral', 'N'): {
        'code': '69161-8',
        'long_name': 'XR Knee - bilateral',
        'component': 'Knee - bilateral',
        'method': 'XR'
    },
    ('Knee', 'MR', 'Right', 'N'): {
        'code': '24876-5',
        'long_name': 'MRI Knee - right W/O contrast',
        'component': 'Knee - right',
        'method': 'MRI'
    },
    ('Knee', 'MRI', 'Right', 'N'): {
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
    ('Knee', 'MRI', 'Left', 'N'): {
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
    ('Pelvis', 'XR', None, 'N'): {
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
    ('Kidney', 'US', 'Bilateral', 'N'): {
        'code': '24642-1',
        'long_name': 'US Kidney bilateral',
        'component': 'Kidney',
        'method': 'US'
    },

    # KUB (Kidney Ureter Bladder)
    ('Kidney', 'CT', None, 'N'): {
        'code': '24645-4',
        'long_name': 'CT Kidney W/O contrast',
        'component': 'Kidney',
        'method': 'CT'
    },
    ('Ureter', 'CT', None, 'N'): {
        'code': '72171-2',
        'long_name': 'CT Ureter',
        'component': 'Ureter',
        'method': 'CT'
    },
    ('Bladder', 'CT', None, 'N'): {
        'code': '24538-1',
        'long_name': 'CT Bladder W/O contrast',
        'component': 'Bladder',
        'method': 'CT'
    },

    # Heart and Vascular
    ('Heart', 'XA', None, 'Y'): {
        'code': '42798-6',
        'long_name': 'XA Heart',
        'component': 'Heart',
        'method': 'XA'
    },
    ('Heart', 'Angio', None, 'Y'): {
        'code': '42798-6',
        'long_name': 'Angiography Heart',
        'component': 'Heart',
        'method': 'Angio'
    },
    ('Coronary artery', 'XA', None, 'Y'): {
        'code': '42798-6',
        'long_name': 'XA Coronary arteries',
        'component': 'Coronary artery',
        'method': 'XA'
    },
    ('Coronary artery', 'Angio', None, 'Y'): {
        'code': '42798-6',
        'long_name': 'Angiography Coronary arteries',
        'component': 'Coronary artery',
        'method': 'Angio'
    },

    # Bone density
    ('Spine', 'BMD', None, 'N'): {
        'code': '38262-7',
        'long_name': 'DXA Bone density in Spine',
        'component': 'Spine',
        'method': 'DXA'
    },
    ('Spine', 'DXA', None, 'N'): {
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
    ('Hip', 'DXA', None, 'N'): {
        'code': '38263-5',
        'long_name': 'DXA Bone density in Hip',
        'component': 'Hip',
        'method': 'DXA'
    },

    # === EXPANDED DATABASE - Additional common radiology studies ===

    # Thoracic spine
    ('Thoracic spine', 'CR', None, 'N'): {
        'code': '36715-1',
        'long_name': 'XR Thoracic spine',
        'component': 'Thoracic spine',
        'method': 'XR'
    },
    ('Thoracic spine', 'XR', None, 'N'): {
        'code': '36715-1',
        'long_name': 'XR Thoracic spine',
        'component': 'Thoracic spine',
        'method': 'XR'
    },
    ('Thoracic spine', 'CT', None, 'N'): {
        'code': '24801-3',
        'long_name': 'CT Thoracic spine W/O contrast',
        'component': 'Thoracic spine',
        'method': 'CT'
    },
    ('Thoracic spine', 'MR', None, 'N'): {
        'code': '24856-7',
        'long_name': 'MRI Thoracic spine W/O contrast',
        'component': 'Thoracic spine',
        'method': 'MRI'
    },
    ('Thoracic spine', 'MRI', None, 'N'): {
        'code': '24856-7',
        'long_name': 'MRI Thoracic spine W/O contrast',
        'component': 'Thoracic spine',
        'method': 'MRI'
    },

    # Spine with contrast
    ('Cervical spine', 'MR', None, 'Y'): {
        'code': '24851-8',
        'long_name': 'MRI Cervical spine W contrast IV',
        'component': 'Cervical spine',
        'method': 'MRI'
    },
    ('Cervical spine', 'MRI', None, 'Y'): {
        'code': '24851-8',
        'long_name': 'MRI Cervical spine W contrast IV',
        'component': 'Cervical spine',
        'method': 'MRI'
    },
    ('Thoracic spine', 'MR', None, 'Y'): {
        'code': '24855-9',
        'long_name': 'MRI Thoracic spine W contrast IV',
        'component': 'Thoracic spine',
        'method': 'MRI'
    },
    ('Thoracic spine', 'MRI', None, 'Y'): {
        'code': '24855-9',
        'long_name': 'MRI Thoracic spine W contrast IV',
        'component': 'Thoracic spine',
        'method': 'MRI'
    },
    ('Lumbar spine', 'MR', None, 'Y'): {
        'code': '24859-1',
        'long_name': 'MRI Lumbar spine W contrast IV',
        'component': 'Lumbar spine',
        'method': 'MRI'
    },
    ('Lumbar spine', 'MRI', None, 'Y'): {
        'code': '24859-1',
        'long_name': 'MRI Lumbar spine W contrast IV',
        'component': 'Lumbar spine',
        'method': 'MRI'
    },

    # Shoulder
    ('Shoulder', 'CR', 'Right', 'N'): {
        'code': '37016-2',
        'long_name': 'XR Shoulder - right',
        'component': 'Shoulder - right',
        'method': 'XR'
    },
    ('Shoulder', 'XR', 'Right', 'N'): {
        'code': '37016-2',
        'long_name': 'XR Shoulder - right',
        'component': 'Shoulder - right',
        'method': 'XR'
    },
    ('Shoulder', 'CR', 'Left', 'N'): {
        'code': '37015-4',
        'long_name': 'XR Shoulder - left',
        'component': 'Shoulder - left',
        'method': 'XR'
    },
    ('Shoulder', 'XR', 'Left', 'N'): {
        'code': '37015-4',
        'long_name': 'XR Shoulder - left',
        'component': 'Shoulder - left',
        'method': 'XR'
    },
    ('Shoulder', 'MR', 'Right', 'N'): {
        'code': '24882-3',
        'long_name': 'MRI Shoulder - right W/O contrast',
        'component': 'Shoulder - right',
        'method': 'MRI'
    },
    ('Shoulder', 'MRI', 'Right', 'N'): {
        'code': '24882-3',
        'long_name': 'MRI Shoulder - right W/O contrast',
        'component': 'Shoulder - right',
        'method': 'MRI'
    },
    ('Shoulder', 'MR', 'Left', 'N'): {
        'code': '24881-5',
        'long_name': 'MRI Shoulder - left W/O contrast',
        'component': 'Shoulder - left',
        'method': 'MRI'
    },
    ('Shoulder', 'MRI', 'Left', 'N'): {
        'code': '24881-5',
        'long_name': 'MRI Shoulder - left W/O contrast',
        'component': 'Shoulder - left',
        'method': 'MRI'
    },

    # Elbow
    ('Elbow', 'CR', 'Right', 'N'): {
        'code': '37256-4',
        'long_name': 'XR Elbow - right',
        'component': 'Elbow - right',
        'method': 'XR'
    },
    ('Elbow', 'XR', 'Right', 'N'): {
        'code': '37256-4',
        'long_name': 'XR Elbow - right',
        'component': 'Elbow - right',
        'method': 'XR'
    },
    ('Elbow', 'CR', 'Left', 'N'): {
        'code': '37255-6',
        'long_name': 'XR Elbow - left',
        'component': 'Elbow - left',
        'method': 'XR'
    },
    ('Elbow', 'XR', 'Left', 'N'): {
        'code': '37255-6',
        'long_name': 'XR Elbow - left',
        'component': 'Elbow - left',
        'method': 'XR'
    },

    # Wrist
    ('Wrist', 'CR', 'Right', 'N'): {
        'code': '37022-0',
        'long_name': 'XR Wrist - right',
        'component': 'Wrist - right',
        'method': 'XR'
    },
    ('Wrist', 'XR', 'Right', 'N'): {
        'code': '37022-0',
        'long_name': 'XR Wrist - right',
        'component': 'Wrist - right',
        'method': 'XR'
    },
    ('Wrist', 'CR', 'Left', 'N'): {
        'code': '37021-2',
        'long_name': 'XR Wrist - left',
        'component': 'Wrist - left',
        'method': 'XR'
    },
    ('Wrist', 'XR', 'Left', 'N'): {
        'code': '37021-2',
        'long_name': 'XR Wrist - left',
        'component': 'Wrist - left',
        'method': 'XR'
    },

    # Hip X-ray
    ('Hip', 'CR', 'Right', 'N'): {
        'code': '37606-0',
        'long_name': 'XR Hip - right',
        'component': 'Hip - right',
        'method': 'XR'
    },
    ('Hip', 'XR', 'Right', 'N'): {
        'code': '37606-0',
        'long_name': 'XR Hip - right',
        'component': 'Hip - right',
        'method': 'XR'
    },
    ('Hip', 'CR', 'Left', 'N'): {
        'code': '37605-2',
        'long_name': 'XR Hip - left',
        'component': 'Hip - left',
        'method': 'XR'
    },
    ('Hip', 'XR', 'Left', 'N'): {
        'code': '37605-2',
        'long_name': 'XR Hip - left',
        'component': 'Hip - left',
        'method': 'XR'
    },
    ('Hip', 'CR', 'Bilateral', 'N'): {
        'code': '37604-5',
        'long_name': 'XR Hip - bilateral',
        'component': 'Hip - bilateral',
        'method': 'XR'
    },
    ('Hip', 'XR', 'Bilateral', 'N'): {
        'code': '37604-5',
        'long_name': 'XR Hip - bilateral',
        'component': 'Hip - bilateral',
        'method': 'XR'
    },
    ('Hip', 'MR', 'Right', 'N'): {
        'code': '24869-0',
        'long_name': 'MRI Hip - right W/O contrast',
        'component': 'Hip - right',
        'method': 'MRI'
    },
    ('Hip', 'MRI', 'Right', 'N'): {
        'code': '24869-0',
        'long_name': 'MRI Hip - right W/O contrast',
        'component': 'Hip - right',
        'method': 'MRI'
    },
    ('Hip', 'MR', 'Left', 'N'): {
        'code': '24868-2',
        'long_name': 'MRI Hip - left W/O contrast',
        'component': 'Hip - left',
        'method': 'MRI'
    },
    ('Hip', 'MRI', 'Left', 'N'): {
        'code': '24868-2',
        'long_name': 'MRI Hip - left W/O contrast',
        'component': 'Hip - left',
        'method': 'MRI'
    },

    # Ankle
    ('Ankle', 'CR', 'Right', 'N'): {
        'code': '37048-2',
        'long_name': 'XR Ankle - right',
        'component': 'Ankle - right',
        'method': 'XR'
    },
    ('Ankle', 'XR', 'Right', 'N'): {
        'code': '37048-2',
        'long_name': 'XR Ankle - right',
        'component': 'Ankle - right',
        'method': 'XR'
    },
    ('Ankle', 'CR', 'Left', 'N'): {
        'code': '37047-4',
        'long_name': 'XR Ankle - left',
        'component': 'Ankle - left',
        'method': 'XR'
    },
    ('Ankle', 'XR', 'Left', 'N'): {
        'code': '37047-4',
        'long_name': 'XR Ankle - left',
        'component': 'Ankle - left',
        'method': 'XR'
    },
    ('Ankle', 'MR', 'Right', 'N'): {
        'code': '24900-3',
        'long_name': 'MRI Ankle - right W/O contrast',
        'component': 'Ankle - right',
        'method': 'MRI'
    },
    ('Ankle', 'MRI', 'Right', 'N'): {
        'code': '24900-3',
        'long_name': 'MRI Ankle - right W/O contrast',
        'component': 'Ankle - right',
        'method': 'MRI'
    },
    ('Ankle', 'MR', 'Left', 'N'): {
        'code': '24899-7',
        'long_name': 'MRI Ankle - left W/O contrast',
        'component': 'Ankle - left',
        'method': 'MRI'
    },
    ('Ankle', 'MRI', 'Left', 'N'): {
        'code': '24899-7',
        'long_name': 'MRI Ankle - left W/O contrast',
        'component': 'Ankle - left',
        'method': 'MRI'
    },

    # Foot
    ('Foot', 'CR', 'Right', 'N'): {
        'code': '37542-4',
        'long_name': 'XR Foot - right',
        'component': 'Foot - right',
        'method': 'XR'
    },
    ('Foot', 'XR', 'Right', 'N'): {
        'code': '37542-4',
        'long_name': 'XR Foot - right',
        'component': 'Foot - right',
        'method': 'XR'
    },
    ('Foot', 'CR', 'Left', 'N'): {
        'code': '37541-6',
        'long_name': 'XR Foot - left',
        'component': 'Foot - left',
        'method': 'XR'
    },
    ('Foot', 'XR', 'Left', 'N'): {
        'code': '37541-6',
        'long_name': 'XR Foot - left',
        'component': 'Foot - left',
        'method': 'XR'
    },

    # Skull and Facial bones
    ('Skull', 'CR', None, 'N'): {
        'code': '36588-2',
        'long_name': 'XR Skull',
        'component': 'Skull',
        'method': 'XR'
    },
    ('Skull', 'XR', None, 'N'): {
        'code': '36588-2',
        'long_name': 'XR Skull',
        'component': 'Skull',
        'method': 'XR'
    },

    # Sinus
    ('Sinus', 'CR', None, 'N'): {
        'code': '36740-9',
        'long_name': 'XR Paranasal sinuses',
        'component': 'Sinus',
        'method': 'XR'
    },
    ('Sinus', 'XR', None, 'N'): {
        'code': '36740-9',
        'long_name': 'XR Paranasal sinuses',
        'component': 'Sinus',
        'method': 'XR'
    },
    ('Sinus', 'CT', None, 'N'): {
        'code': '24671-0',
        'long_name': 'CT Paranasal sinuses W/O contrast',
        'component': 'Sinus',
        'method': 'CT'
    },

    # Neck
    ('Neck', 'CT', None, 'N'): {
        'code': '24551-4',
        'long_name': 'CT Neck W/O contrast',
        'component': 'Neck',
        'method': 'CT'
    },
    ('Neck', 'CT', None, 'Y'): {
        'code': '24550-6',
        'long_name': 'CT Neck W contrast IV',
        'component': 'Neck',
        'method': 'CT'
    },
    ('Neck', 'MR', None, 'N'): {
        'code': '24864-1',
        'long_name': 'MRI Neck W/O contrast',
        'component': 'Neck',
        'method': 'MRI'
    },
    ('Neck', 'MRI', None, 'N'): {
        'code': '24864-1',
        'long_name': 'MRI Neck W/O contrast',
        'component': 'Neck',
        'method': 'MRI'
    },
    ('Neck', 'MR', None, 'Y'): {
        'code': '24863-3',
        'long_name': 'MRI Neck W contrast IV',
        'component': 'Neck',
        'method': 'MRI'
    },
    ('Neck', 'MRI', None, 'Y'): {
        'code': '24863-3',
        'long_name': 'MRI Neck W contrast IV',
        'component': 'Neck',
        'method': 'MRI'
    },

    # Chest MRI
    ('Chest', 'MR', None, 'N'): {
        'code': '24629-8',
        'long_name': 'MRI Chest W/O contrast',
        'component': 'Chest',
        'method': 'MRI'
    },
    ('Chest', 'MRI', None, 'N'): {
        'code': '24629-8',
        'long_name': 'MRI Chest W/O contrast',
        'component': 'Chest',
        'method': 'MRI'
    },

    # Abdomen MRI
    ('Abdomen', 'MR', None, 'N'): {
        'code': '24637-1',
        'long_name': 'MRI Abdomen W/O contrast',
        'component': 'Abdomen',
        'method': 'MRI'
    },
    ('Abdomen', 'MRI', None, 'N'): {
        'code': '24637-1',
        'long_name': 'MRI Abdomen W/O contrast',
        'component': 'Abdomen',
        'method': 'MRI'
    },
    ('Abdomen', 'MR', None, 'Y'): {
        'code': '24636-3',
        'long_name': 'MRI Abdomen W contrast IV',
        'component': 'Abdomen',
        'method': 'MRI'
    },
    ('Abdomen', 'MRI', None, 'Y'): {
        'code': '24636-3',
        'long_name': 'MRI Abdomen W contrast IV',
        'component': 'Abdomen',
        'method': 'MRI'
    },

    # Pelvis CT with contrast
    ('Pelvis', 'CT', None, 'Y'): {
        'code': '24906-0',
        'long_name': 'CT Pelvis W contrast IV',
        'component': 'Pelvis',
        'method': 'CT'
    },

    # Additional Ultrasound
    ('Gallbladder', 'US', None, 'N'): {
        'code': '30707-4',
        'long_name': 'US Gallbladder',
        'component': 'Gallbladder',
        'method': 'US'
    },
    ('Pancreas', 'US', None, 'N'): {
        'code': '30708-2',
        'long_name': 'US Pancreas',
        'component': 'Pancreas',
        'method': 'US'
    },
    ('Spleen', 'US', None, 'N'): {
        'code': '30709-0',
        'long_name': 'US Spleen',
        'component': 'Spleen',
        'method': 'US'
    },
    ('Thyroid', 'US', None, 'N'): {
        'code': '30734-8',
        'long_name': 'US Thyroid',
        'component': 'Thyroid',
        'method': 'US'
    },
    ('Breast', 'US', 'Right', 'N'): {
        'code': '24604-1',
        'long_name': 'US Breast - right',
        'component': 'Breast - right',
        'method': 'US'
    },
    ('Breast', 'US', 'Left', 'N'): {
        'code': '24603-3',
        'long_name': 'US Breast - left',
        'component': 'Breast - left',
        'method': 'US'
    },
    ('Breast', 'US', 'Bilateral', 'N'): {
        'code': '24602-5',
        'long_name': 'US Breast - bilateral',
        'component': 'Breast - bilateral',
        'method': 'US'
    },
    ('Pelvis', 'US', None, 'N'): {
        'code': '30710-8',
        'long_name': 'US Pelvis',
        'component': 'Pelvis',
        'method': 'US'
    },
    ('Scrotum', 'US', None, 'N'): {
        'code': '30712-4',
        'long_name': 'US Scrotum',
        'component': 'Scrotum',
        'method': 'US'
    },

    # Vascular studies
    ('Carotid artery', 'US', None, 'N'): {
        'code': '24728-8',
        'long_name': 'US Carotid artery',
        'component': 'Carotid artery',
        'method': 'US'
    },
    ('Carotid artery', 'US', 'Bilateral', 'N'): {
        'code': '24728-8',
        'long_name': 'US Carotid artery bilateral',
        'component': 'Carotid artery',
        'method': 'US'
    },

    # CT Angiography
    ('Aorta', 'CT', None, 'Y'): {
        'code': '30598-7',
        'long_name': 'CTA Aorta',
        'component': 'Aorta',
        'method': 'CTA'
    },
    ('Coronary artery', 'CT', None, 'Y'): {
        'code': '79073-5',
        'long_name': 'CTA Coronary arteries',
        'component': 'Coronary artery',
        'method': 'CTA'
    },
    ('Pulmonary artery', 'CT', None, 'Y'): {
        'code': '36814-3',
        'long_name': 'CTA Pulmonary artery',
        'component': 'Pulmonary artery',
        'method': 'CTA'
    },

    # MR Angiography
    ('Brain', 'MRA', None, 'N'): {
        'code': '24590-2',
        'long_name': 'MRA Brain W/O contrast',
        'component': 'Brain',
        'method': 'MRA'
    },
    ('Brain', 'MRA', None, 'Y'): {
        'code': '24589-4',
        'long_name': 'MRA Brain W contrast IV',
        'component': 'Brain',
        'method': 'MRA'
    },
    ('Neck', 'MRA', None, 'N'): {
        'code': '24597-7',
        'long_name': 'MRA Neck W/O contrast',
        'component': 'Neck',
        'method': 'MRA'
    },
    ('Neck', 'MRA', None, 'Y'): {
        'code': '24596-9',
        'long_name': 'MRA Neck W contrast IV',
        'component': 'Neck',
        'method': 'MRA'
    },

    # Mammography
    ('Breast', 'MG', 'Right', 'N'): {
        'code': '24606-6',
        'long_name': 'MG Breast - right screening',
        'component': 'Breast - right',
        'method': 'MG'
    },
    ('Breast', 'MG', 'Left', 'N'): {
        'code': '24605-8',
        'long_name': 'MG Breast - left screening',
        'component': 'Breast - left',
        'method': 'MG'
    },
    ('Breast', 'MG', 'Bilateral', 'N'): {
        'code': '24604-1',
        'long_name': 'MG Breast - bilateral screening',
        'component': 'Breast - bilateral',
        'method': 'MG'
    },

    # Whole body
    ('Whole body', 'CT', None, 'Y'): {
        'code': '24962-3',
        'long_name': 'CT Whole body W contrast IV',
        'component': 'Whole body',
        'method': 'CT'
    },
    ('Whole body', 'CT', None, 'N'): {
        'code': '24963-1',
        'long_name': 'CT Whole body W/O contrast',
        'component': 'Whole body',
        'method': 'CT'
    },
    ('Whole body', 'BMD', None, 'N'): {
        'code': '38265-0',
        'long_name': 'DXA Whole body bone density',
        'component': 'Whole body',
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
