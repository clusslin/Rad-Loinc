# Radiology LOINC Mapper

一個將放射線檢查項目自動對應到LOINC編碼的工具。

A tool for automatically mapping radiology examinations to LOINC (Logical Observation Identifiers Names and Codes) codes.

## 功能特點 (Features)

- 自動解析放射線檢查描述 (Automatic parsing of radiology study descriptions)
- 識別醫學縮寫 (Medical abbreviation recognition)
- 提取身體部位、側性資訊 (Body part and laterality extraction)
- 支援中英文描述 (Support for both English and Chinese descriptions)
- 自動對應LOINC編碼 (Automatic LOINC code mapping)
- 批次處理Excel檔案 (Batch processing of Excel files)
- 問題標記與信心度評估 (Issue flagging and confidence assessment)

## 支援的影像檢查類型 (Supported Modalities)

- CR/XR (Conventional Radiography / X-ray)
- CT (Computed Tomography)
- MR/MRI (Magnetic Resonance Imaging)
- US (Ultrasound)
- XA (Angiography)
- RF (Fluoroscopy)
- BMD (Bone Mineral Density / DXA)
- OT (Other)

## 安裝 (Installation)

### 系統需求 (Requirements)

- Python 3.7 或更高版本
- pip (Python package installer)

### 安裝步驟 (Installation Steps)

```bash
# Clone the repository
git clone https://github.com/yourusername/Rad-Loinc.git
cd Rad-Loinc

# Install dependencies
pip install -r requirements.txt
```

## 使用方式 (Usage)

### 基本用法 (Basic Usage)

```bash
python rad_loinc_mapper.py -i input.xlsx -o output.xlsx
```

### 命令列參數 (Command-line Arguments)

- `-i, --input`: 輸入Excel檔案路徑 (Required)
- `-o, --output`: 輸出Excel檔案路徑 (Optional, 預設: output_TIMESTAMP.xlsx)
- `--sheet`: 輸出工作表名稱 (Optional, 預設: LOINC Mapping)
- `-v, --verbose`: 顯示詳細輸出 (Optional)

### 範例 (Examples)

```bash
# 使用範例資料
python rad_loinc_mapper.py -i examples/sample_input.csv -o results/mapped_output.xlsx

# 顯示詳細資訊
python rad_loinc_mapper.py -i input.xlsx -o output.xlsx -v

# 自動生成輸出檔名
python rad_loinc_mapper.py -i input.xlsx
```

## 輸入格式 (Input Format)

### 必要欄位 (Required Columns)

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| value_code | 內部編碼 | RAD001 |
| modality | 檢查類型 | CT, MR, CR, US |
| Study Description | 檢查描述(英文) | Chest PA view |

### 選用欄位 (Optional Columns)

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| Chinese Study Description | 檢查描述(中文) | 胸部正面 |
| Contrast | 對比劑使用情況 | Y, N, N+Y |
| Combine Modality | 複合檢查類型 | RF,CT |

### Contrast 欄位說明

- `Y`: 有使用對比劑
- `N`: 無使用對比劑
- `N+Y`: 包含有對比劑及無對比劑兩種檢查

### 輸入範例 (Input Example)

```csv
value_code,modality,Study Description,Chinese Study Description,Contrast,Combine Modality
RAD001,CR,Chest PA view,胸部正面,N,
RAD002,CT,Brain without contrast,腦部電腦斷層,N,
RAD003,CT,Chest with IV contrast,胸部含對比劑,Y,
RAD004,MR,Lt knee without contrast,左膝磁振造影,N,
```

## 輸出格式 (Output Format)

輸出Excel檔案包含以下欄位:

| 欄位名稱 | 說明 |
|---------|------|
| value_code | 原始內部編碼 |
| modality | 原始檢查類型 |
| Study Description | 原始檢查描述 |
| Chinese Study Description | 原始中文描述 |
| Contrast | 對比劑資訊 |
| Combine Modality | 複合檢查類型 |
| Primary Modality | 主要檢查類型 |
| Expanded Description | 展開縮寫後的描述 |
| Body Parts | 識別出的身體部位 |
| Laterality | 側性(左/右/雙側) |
| LOINC Code | 對應的LOINC編碼 |
| LOINC Name | LOINC完整名稱 |
| LOINC Component | LOINC組件 |
| LOINC Method | LOINC方法 |
| Mapping Confidence | 對應信心度 (High/Low/None) |
| Has Issues | 是否有問題 (Yes/No) |
| Issues | 問題說明 |

## 功能說明 (Features Details)

### 1. 醫學縮寫識別 (Medical Abbreviation Recognition)

系統能識別常見的放射線檢查縮寫:

- C-spine → Cervical spine
- L-spine → Lumbar spine
- Abd → Abdomen
- Rt → Right
- Lt → Left
- KUB → Kidney Ureter Bladder
- 等超過50種常見縮寫

### 2. 身體部位識別 (Body Part Extraction)

- 從英文描述提取身體部位
- 從中文描述輔助識別
- 支援複數身體部位
- 標準化部位名稱

### 3. 側性識別 (Laterality Detection)

自動識別:
- Right (右側): Rt, Right, 右
- Left (左側): Lt, Left, 左
- Bilateral (雙側): Bil, Bilateral, Both, 雙側

### 4. 對比劑檢測 (Contrast Detection)

- 從Contrast欄位讀取
- 從描述文字自動偵測
- 支援中英文對比劑關鍵字

### 5. LOINC對應邏輯 (LOINC Mapping Logic)

對應考慮因素:
1. 身體部位 (Body part)
2. 檢查類型 (Modality)
3. 側性 (Laterality)
4. 對比劑使用 (Contrast usage)

信心度評估:
- **High**: 找到完全匹配的LOINC編碼
- **Low**: 使用通用LOINC編碼
- **None**: 無法找到適合的編碼

### 6. 問題標記 (Issue Flagging)

系統會標記以下問題:
- 無法識別身體部位
- 多種可能的LOINC編碼
- 使用通用編碼
- 複合檢查類型
- 對比劑資訊不明確

## 測試 (Testing)

執行測試腳本驗證功能:

```bash
python test_mapper.py
```

這將測試:
- 描述解析器功能
- LOINC對應功能
- 各種檢查類型的處理

## 專案結構 (Project Structure)

```
Rad-Loinc/
├── README.md                    # 專案說明文件
├── LICENSE                      # 授權文件
├── requirements.txt             # Python相依套件
├── rad_loinc_mapper.py         # 主程式
├── test_mapper.py              # 測試腳本
├── src/                        # 原始碼目錄
│   ├── __init__.py
│   ├── medical_terminology.py  # 醫學術語與縮寫
│   ├── description_parser.py   # 描述解析器
│   ├── loinc_database.py       # LOINC資料庫
│   ├── loinc_mapper.py         # LOINC對應引擎
│   └── excel_processor.py      # Excel處理器
└── examples/                    # 範例資料
    └── sample_input.csv        # 範例輸入檔
```

## 擴充LOINC資料庫 (Extending LOINC Database)

要新增更多LOINC編碼，編輯 `src/loinc_database.py`:

```python
LOINC_DATABASE = {
    # 新增格式: (body_part, modality, laterality, contrast) -> LOINC info
    ('Shoulder', 'MR', 'Right', 'N'): {
        'code': 'XXXXX-X',
        'long_name': 'MRI Shoulder - right W/O contrast',
        'component': 'Shoulder - right',
        'method': 'MRI'
    },
}
```

## 常見問題 (FAQ)

### Q: 為什麼有些檢查無法對應到LOINC編碼?

A: 可能的原因:
1. LOINC資料庫中沒有該檢查類型
2. 描述文字無法識別身體部位
3. 檢查類型組合較特殊

這些情況會在Issues欄位中說明，可以手動補充或擴充LOINC資料庫。

### Q: 如何提高對應準確度?

A: 建議:
1. 提供完整的Study Description
2. 同時提供Chinese Study Description輔助識別
3. 明確指定Contrast資訊
4. 使用標準化的描述用語

### Q: 可以處理多大的資料量?

A: 工具可以處理數千筆資料。對於超大資料量，建議分批處理。

### Q: 支援其他語言嗎?

A: 目前支援英文和中文。可以擴充 `medical_terminology.py` 來支援其他語言。

## 貢獻 (Contributing)

歡迎貢獻! 請:
1. Fork 本專案
2. 建立您的feature branch
3. Commit 您的變更
4. Push 到 branch
5. 建立 Pull Request

## 授權 (License)

MIT License - 詳見 LICENSE 檔案

## 聯絡方式 (Contact)

如有問題或建議，請開 Issue 或聯絡專案維護者。

## 致謝 (Acknowledgments)

- LOINC® is a registered trademark of Regenstrief Institute, Inc.
- 本工具使用 LOINC 標準進行放射線檢查編碼

## 版本歷史 (Version History)

### v1.0.0 (2024)
- 初始版本
- 支援基本LOINC對應功能
- 支援中英文描述解析
- Excel批次處理功能
