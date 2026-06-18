from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import requests
import xml.etree.ElementTree as ET

MAX_BOOK_TITLE_LEN = 256
MAX_AUTHOR_LEN = 256
MAX_PUBLISHER_LEN = 128
MAX_TAGNAME_LEN = 64
ISBN_DIGITS = 13


class Book(models.Model):
    isbn = models.CharField(unique=True, max_length=ISBN_DIGITS, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    url = models.URLField(default="")
    imageUrl = models.URLField(default="")

    def fetch_aladin_data(self):
        """Aladin API에서 이미지 URL과 책 URL을 가져옵니다"""
        aladin_url = "https://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
        params = {
            'ttbkey': 'ttbncc17012351008',
            'itemIdType': 'ISBN13',
            'output': 'xml',
            'ItemId': self.isbn,
        }

        try:
            response = requests.get(aladin_url, params=params, timeout=5)
            if response.status_code == 200:
                namespace = {'aladin': 'http://www.aladin.co.kr/ttb/apiguide.aspx'}
                root = ET.fromstring(response.content)
                
                # item 요소 찾기
                item = root.find('.//aladin:item', namespace)
                if item is not None:
                    # 이미지 URL 처리
                    if not self.imageUrl:
                        cover_element = item.find('aladin:cover', namespace)
                        if cover_element is not None and cover_element.text:
                            self.imageUrl = cover_element.text
                    
                    # 책 URL 처리 (item 내의 link)
                    if not self.url:
                        link_element = item.find('aladin:link', namespace)
                        if link_element is not None and link_element.text:
                            # URL에서 ttbkey와 start 파라미터 제거 (너무 길어짐)
                            url = link_element.text
                            if '&ttbkey=' in url:
                                url = url.split('&ttbkey=')[0]
                            self.url = url
                    
                    self.save()
        except Exception as e:
            print(f"Aladin API Error for ISBN {self.isbn}: {e}")

    def fetch_image_from_aladin(self):
        if self.imageUrl:
            return self.imageUrl
        self.fetch_aladin_data()
        return self.imageUrl
    
    def get_book_url(self):
        """책의 URL을 반환합니다. 없으면 Aladin에서 조회합니다"""
        if self.url:
            return self.url
        self.fetch_aladin_data()
        return self.url

    def __unicode__(self):
        return self.isbn


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=MAX_TAGNAME_LEN)

    def __unicode__(self):
        return self.name


class BookRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=MAX_BOOK_TITLE_LEN)
    memo = models.TextField(null=True)
    author = models.CharField(null=True, max_length=MAX_AUTHOR_LEN)
    publisher = models.CharField(null=True, max_length=MAX_PUBLISHER_LEN)
    rating = models.IntegerField(null=True, default=0, validators=[MaxValueValidator(5), MinValueValidator(0)], help_text='Stars')
    check1 = models.BooleanField(default=False)
    check2 = models.BooleanField(default=False)
    check3 = models.BooleanField(default=False)
    dateStart = models.DateTimeField(null=True)
    dateEnd = models.DateTimeField(null=True)
    tags = models.ManyToManyField(Tag, help_text='Tags')

    class Meta:
        ordering = ['-dateEnd']

    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.title)
