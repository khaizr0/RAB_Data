# Import Complex Data to DynamoDB

Script này dùng để import dữ liệu phức tạp (PhuKien, TinTuc, XeOto) vào DynamoDB.

## Files

- `complex-data.json` - Dữ liệu trích xuất từ backup (chỉ PhuKien, TinTuc, XeOto)
- `import-complex-data.py` - Script Python để import vào DynamoDB

## Cách sử dụng

### 1. Upload files lên AWS CloudShell

```bash
# Upload 2 files: complex-data.json và import-complex-data.py
```

### 2. Chạy script

```bash
python3 import-complex-data.py
```

### 3. Kết quả

```
Importing PhuKien...
✓ Imported 2 items to PhuKien
Importing TinTuc...
✓ Imported 2 items to TinTuc
Importing XeOto...
✓ Imported 2 items to XeOto

Import completed!
```

## Yêu cầu

- AWS CLI đã được cấu hình
- Python 3.x
- boto3 (đã có sẵn trong CloudShell)
- Tables đã được tạo trong DynamoDB

## Lưu ý

Script tự động chuyển đổi các kiểu dữ liệu:
- String → S (String)
- Number → N (Number)
- Boolean → BOOL
- Null → NULL
