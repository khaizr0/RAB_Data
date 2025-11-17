# RAB_Data - Restore And Backup Data

Thư mục chứa các công cụ backup và restore dữ liệu DynamoDB.

## 📁 Cấu trúc

```
RAB_Data/
├── backupData.js           # Script backup dữ liệu
├── restoreData.js          # Script restore dữ liệu
├── backup-*.json           # Các file backup
└── README.md              # Hướng dẫn sử dụng
```

## 🔧 Yêu cầu

### Local Development:
- DynamoDB Local đang chạy
- File `.env` ở thư mục gốc với `DYNAMODB_ENDPOINT=http://localhost:8000`

### AWS Production:
- AWS credentials trong file `.env` ở thư mục gốc
- Không cần `DYNAMODB_ENDPOINT` (tự động dùng AWS DynamoDB)

## 📦 Backup Data

```bash
cd RAB_Data
node backupData.js
```

Hoặc từ thư mục gốc:
```bash
yarn backup
```

### Kết quả:
- Tạo file `backup-YYYY-MM-DDTHH-MM-SS-MMMZ.json`
- Chứa toàn bộ data từ tất cả tables
- Tự động quét và backup tất cả tables trong DynamoDB
- Hoạt động với cả Local và AWS Production

## 🔄 Restore Data

```bash
cd RAB_Data
node restoreData.js backup-2025-10-15T03-13-22-686Z.json
```

Hoặc từ thư mục gốc:
```bash
yarn db
```

### Chức năng:
- ✅ Tự động tạo tables nếu chưa tồn tại
- ✅ Chờ tables ACTIVE trước khi restore (không còn lỗi "Requested resource not found")
- ✅ Restore toàn bộ data từ file backup
- ✅ Xử lý schema đặc biệt (User table có EmailIndex)
- ✅ Hiển thị progress chi tiết
- ✅ Hoạt động với cả Local và AWS Production

## 📝 Cấu hình

### Local Development (.env.local):
```env
DYNAMODB_ENDPOINT=http://localhost:9000
AWS_REGION=ap-southeast-1
AWS_ACCESS_KEY_ID=fakeAccessKeyId
AWS_SECRET_ACCESS_KEY=fakeSecretAccessKey
```

### AWS Production (.env):
```env
AWS_REGION=ap-southeast-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
# Không có DYNAMODB_ENDPOINT = tự động dùng AWS DynamoDB
```

## 📝 Lưu ý

1. **Script tự động detect môi trường:**
   - Có `DYNAMODB_ENDPOINT` → Dùng DynamoDB Local
   - Không có `DYNAMODB_ENDPOINT` → Dùng AWS DynamoDB

2. **Backup định kỳ:**
   - Nên backup trước khi thay đổi lớn
   - Giữ nhiều bản backup khác nhau
   - Đặt tên file có timestamp để dễ quản lý

3. **Restore:**
   - Sẽ ghi đè data hiện tại
   - Nên backup trước khi restore
   - Tables sẽ được tạo tự động nếu chưa có
   - Chờ tables ACTIVE trước khi restore data

## 🚀 Workflow

### Setup lần đầu (Local):
```bash
# 1. Khởi động DynamoDB Local
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

# 2. Restore data
cd RAB_Data
node restoreData.js backup-2025-10-15T03-13-22-686Z.json
```

### Setup lần đầu (AWS Production):
```bash
# 1. Đảm bảo file .env có AWS credentials
# 2. Restore data
cd RAB_Data
node restoreData.js backup-2025-10-15T03-13-22-686Z.json
```

### Backup định kỳ:
```bash
cd RAB_Data
node backupData.js
```

### Restore khi cần:
```bash
cd RAB_Data
node restoreData.js backup-YYYY-MM-DDTHH-MM-SS-MMMZ.json
```

## 📊 Tables được backup

- User
- XeOto
- PhuKien
- ThuongHieu
- LoaiPhuKien
- TinTuc
- DatLichKH
- DanhGia
- Slider
- KieuDang
- MauXe
- NguyenLieuXe

## ⚠️ Troubleshooting

**Lỗi: "Backup file not found"**
- Kiểm tra đường dẫn file
- Đảm bảo file tồn tại trong thư mục RAB_Data

**Lỗi: "Region is missing"**
- Đảm bảo file `.env` ở thư mục gốc có `AWS_REGION`
- Script tự động đọc `.env` từ thư mục cha

**Lỗi: "Cannot connect to DynamoDB"**
- Local: Kiểm tra DynamoDB Local đang chạy
- AWS: Kiểm tra AWS credentials trong `.env`

**Lỗi: "Requested resource not found"**
- Đã fix! Script giờ chờ tables ACTIVE trước khi restore

**Lỗi: "Table already exists"**
- Bình thường, script sẽ bỏ qua và tiếp tục restore data
