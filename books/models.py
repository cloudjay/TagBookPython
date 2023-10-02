from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


MAX_BOOK_TITLE_LEN = 256
MAX_AUTHOR_LEN = 256
MAX_PUBLISHER_LEN = 128
MAX_TAGNAME_LEN = 64
ISBN_DIGITS = 13


class Book(models.Model):
    isbn = models.CharField(unique=True, max_length=ISBN_DIGITS, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    url = models.URLField(default="")
    imageUrl = models.URLField(default="")

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
