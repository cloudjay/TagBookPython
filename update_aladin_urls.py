import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_tagbook.settings')
django.setup()

from books.models import Book

# 모든 Book 레코드에 대해 Aladin 데이터 가져오기
books = Book.objects.all()
total = books.count()
updated = 0
failed = 0

print(f"총 {total}개의 책 정보를 업데이트합니다...\n")

for idx, book in enumerate(books, 1):
    try:
        # URL이 없거나 imageUrl이 없으면 Aladin에서 가져오기
        if not book.url or not book.imageUrl:
            old_url = book.url
            old_image = book.imageUrl

            book.fetch_aladin_data()

            # 변경 확인
            if book.url != old_url or book.imageUrl != old_image:
                updated += 1
                if book.url and old_url != book.url:
                    print(f"[{idx}/{total}] ISBN {book.isbn}: URL 추가됨")
                elif book.imageUrl and old_image != book.imageUrl:
                    print(f"[{idx}/{total}] ISBN {book.isbn}: 이미지 URL 추가됨")
            else:
                print(f"[{idx}/{total}] ISBN {book.isbn}: 데이터 없음")
        else:
            print(f"[{idx}/{total}] ISBN {book.isbn}: 이미 완료됨")
    except Exception as e:
        failed += 1
        print(f"[{idx}/{total}] ISBN {book.isbn}: 오류 - {e}")

print(f"\n===== 완료 =====")
print(f"업데이트됨: {updated}개")
print(f"실패: {failed}개")
print(f"총: {total}개")

