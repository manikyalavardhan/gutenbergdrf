from rest_framework import serializers
from .models import Books, Authors, BooksLanguage, BooksLanguages, BooksShelf, BooksShelves, BooksSubject, BooksSubjects, BooksFormat, BooksAuthors

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ['name', 'birth_year', 'death_year']

# Books Author Serializer
class BooksAuthorsSerializer(serializers.ModelSerializer):
	author = AuthorSerializer()
	class Meta:
		model = BooksAuthors
		fields = ['author']

# Books Format Serializer
class BookFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksFormat
        fields = ['mime_type', 'url']

# Book Langauge Serializer
class BookLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksLanguage
        fields = ['code']

# Books Languages Serializer
class BooksLanguagesSerializer(serializers.ModelSerializer):
	language = BookLanguageSerializer()
	class Meta:
		model = BooksLanguages
		fields = ['language']

# Book Subject Serializer
class BookSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksSubject
        fields = ['name']

# Books Subject Serializer
class BookSubjectsSerializer(serializers.ModelSerializer):
	subject = BookSubjectSerializer()
	class Meta:
		model = BooksSubjects
		fields = ['subject']

# Bookshelf Serializer
class BookShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksShelf
        fields = ['name']

# Books Shelves Serializer
class BookShelvesSerializer(serializers.ModelSerializer):
	bookshelf = BookShelfSerializer()
	class Meta:
		model = BooksShelves
		fields = ['bookshelf']

# Books Serializer
class BookSerializer(serializers.ModelSerializer):
    # Nested Serializers for associated data
    booksauthors = BooksAuthorsSerializer(many=True, read_only=True)
    bookformats = BookFormatSerializer(many=True, read_only=True)
    booklanguages = BooksLanguagesSerializer(many=True, read_only=True)
    booksubjects = BookSubjectsSerializer(many=True, read_only=True)
    bookshelves = BookShelvesSerializer(many=True, read_only=True)

    class Meta:
        model = Books
        fields = ['title', 'booksauthors', 'booklanguages', 'booksubjects', 'bookshelves', 'bookformats']
