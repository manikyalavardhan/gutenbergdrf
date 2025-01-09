# Create your models here.
from django.db import models


class Authors(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'books_author'


class Books(models.Model):
    id = models.IntegerField(primary_key=True)
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=16)
    title = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books_book'


class BooksAuthors(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, to_field='gutenberg_id', db_column='book_id',related_name='booksauthors')
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, db_column='author_id',related_name='authors')

    class Meta:
        managed = False
        db_table = 'books_book_authors'
        unique_together = ('book_id', 'author_id')

class BooksShelf(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'books_bookshelf'

class BooksShelves(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, db_column='book_id', to_field='gutenberg_id' ,related_name='bookshelves')
    bookshelf = models.ForeignKey(BooksShelf, on_delete=models.CASCADE, db_column='bookshelf_id',related_name='shelfname')


    class Meta:
        managed = False
        db_table = 'books_book_bookshelves'

class BooksLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'books_language'

class BooksLanguages(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, db_column='book_id', to_field='gutenberg_id' ,related_name='booklanguages')
    language = models.ForeignKey(BooksLanguage, on_delete=models.CASCADE, db_column='language_id', related_name='languagename')


    class Meta:
        managed = False
        db_table = 'books_book_languages'

class BooksSubject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'books_subject'

class BooksSubjects(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, db_column='book_id',to_field='gutenberg_id', related_name = 'booksubjects')
    subject = models.ForeignKey(BooksSubject, on_delete=models.CASCADE, db_column='subject_id', related_name = 'subjectname')


    class Meta:
        managed = False
        db_table = 'books_book_subjects'

class BooksFormat(models.Model):
    id = models.IntegerField(primary_key=True)
    mime_type = models.CharField(max_length=32)
    url = models.TextField()
    book = models.ForeignKey(Books, on_delete=models.CASCADE, to_field='gutenberg_id', db_column='book_id', related_name='bookformats')


    class Meta:
        managed = False
        db_table = 'books_format'
