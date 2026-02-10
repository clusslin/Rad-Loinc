
import pandas as pd
import sys

def prepare_file():
    input_file = 'examples/rad.xlsx'
    output_file = 'examples/rad_prepared.xlsx'

    print(f"Reading {input_file}...")
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Rename columns
    column_map = {
        '計價碼': 'value_code',
        '類別': 'modality',
        '英文名稱': 'Study Description',
        '中文名稱': 'Chinese Study Description'
    }
    
    # Check if columns exist
    for ch_col, en_col in column_map.items():
        if ch_col not in df.columns:
            print(f"Warning: Column '{ch_col}' not found. Available columns: {df.columns.tolist()}")
            # If standard columns are already there, we might skips
            if en_col not in df.columns:
                print(f"Error: Neither '{ch_col}' nor '{en_col}' found.")
                # We can't proceed if critical columns are missing
                if en_col in ['value_code', 'modality', 'Study Description']:
                    # Try to fuzzy match or just fail? 
                    # Let's assume the user provided file structure matches the one we viewed.
                    pass

    df = df.rename(columns=column_map)

    # Normalize modality
    if 'modality' in df.columns:
        # Convert to string to avoid errors
        df['modality'] = df['modality'].astype(str)
        
        # Function to normalize
        def normalize_modality(val):
            val_lower = val.lower().strip()
            if 'x-ray' in val_lower:
                return 'XR'
            if 'cardiac cath' in val_lower:
                return 'XA'
            # Add more manual mappings if needed
            return val # Return original if not matched, though it might fail in mapper if not standard

        df['modality'] = df['modality'].apply(normalize_modality)
        
        # Standardize standard modalities to uppercase just in case (e.g. "ct" -> "CT")
        df['modality'] = df['modality'].str.upper()

        # Fix specific cases if any (e.g. "MRI" is fine, "MR" is fine)
        # Based on loinc_database, keys can be 'MR' or 'MRI'.

    print(f"Writing prepared file to {output_file}...")
    df.to_excel(output_file, index=False)
    print("Done.")

if __name__ == "__main__":
    prepare_file()
