#!/usr/bin/env python3
import boto3
import json

# Khởi tạo DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='ap-southeast-1')

def convert_to_dynamodb_item(data):
    """Chuyển đổi JSON object sang DynamoDB item format"""
    item = {}
    for key, value in data.items():
        if isinstance(value, str):
            item[key] = {"S": value}
        elif isinstance(value, (int, float)):
            item[key] = {"N": str(value)}
        elif isinstance(value, bool):
            item[key] = {"BOOL": value}
        elif value is None:
            item[key] = {"NULL": True}
        else:
            item[key] = {"S": str(value)}
    return item

# Đọc dữ liệu từ file JSON
with open('complex-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Import PhuKien
print("Importing PhuKien...")
if data.get('PhuKien'):
    for item in data['PhuKien']:
        dynamodb_item = convert_to_dynamodb_item(item)
        dynamodb.put_item(TableName='PhuKien', Item=dynamodb_item)
    print(f"✓ Imported {len(data['PhuKien'])} items to PhuKien")

# Import TinTuc
print("Importing TinTuc...")
if data.get('TinTuc'):
    for item in data['TinTuc']:
        dynamodb_item = convert_to_dynamodb_item(item)
        dynamodb.put_item(TableName='TinTuc', Item=dynamodb_item)
    print(f"✓ Imported {len(data['TinTuc'])} items to TinTuc")

# Import XeOto
print("Importing XeOto...")
if data.get('XeOto'):
    for item in data['XeOto']:
        dynamodb_item = convert_to_dynamodb_item(item)
        dynamodb.put_item(TableName='XeOto', Item=dynamodb_item)
    print(f"✓ Imported {len(data['XeOto'])} items to XeOto")

# Import User
print("Importing User...")
if data.get('User'):
    for item in data['User']:
        dynamodb_item = convert_to_dynamodb_item(item)
        dynamodb.put_item(TableName='User', Item=dynamodb_item)
    print(f"✓ Imported {len(data['User'])} items to User")

print("\nImport completed!")
