import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_tagbook.settings')
django.setup()

import requests
import xml.etree.ElementTree as ET

isbn = "9788972915089"
aladin_url = "https://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
params = {
    'ttbkey': 'ttbncc17012351008',
    'itemIdType': 'ISBN13',
    'output': 'xml',
    'ItemId': isbn,
}

response = requests.get(aladin_url, params=params)
print("Status Code:", response.status_code)
print("\nResponse Text (first 1500 chars):")
print(response.text[:1500])

# XML 파싱
try:
    root = ET.fromstring(response.content)
    
    # 모든 요소 출력
    print("\n===== XML Elements =====")
    for elem in root.iter():
        tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if elem.text and elem.text.strip():
            print(f"{tag_name}: {elem.text[:100]}")
    
    # link 요소 찾기
    print("\n===== Link Elements =====")
    for elem in root.iter():
        if 'link' in elem.tag.lower():
            print(f"{elem.tag}: {elem.text}")
            
except Exception as e:
    print(f"Error: {e}")

