from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.db.models import Q
from .models import Books
from .serializers import BookSerializer

class BookPagination(PageNumberPagination):
	page_size = 25
	page_size_query_param = 'page_size'
	max_page_size = 100


class BookFilterBackend():
    def filter_queryset(self, request, queryset, view):
        filters = request.query_params

        # Filter by Gutenberg ID (allow multiple IDs)
        if filters.get('id'):
            gutenberg_ids = filters.getlist('id')[0].split(',')
            queryset = queryset.filter(gutenberg_id__in=gutenberg_ids)

        # Filter by Language (multiple languages, comma-separated)

        if filters.get('language'):
            languages = filters.getlist('language')[0].split(',')
            queryset = queryset.filter(booklanguages__language__code__in=languages)

        # Filter by Mime-type (multiple mime types, comma-separated)
        if filters.get('mime-type'):
            mime_types = filters.getlist('mime-type')[0].split(',')
            queryset = queryset.filter(bookformats__mime_type__in=mime_types)

        # Filter by Topic (multiple topics, comma-separated)
        if filters.get('topic'):
            topics = filters.getlist('topic')[0].split(',')
            queryset = queryset.filter(
                Q(booksubjects__subject__name__icontains=topics[0]) |
                Q(bookshelves__bookshelf__name__icontains=topics[0])
            )
            if len(topics) > 1:
                for topic in topics[1:]:
                    queryset = queryset.filter(
                        Q(booksubjects__subject__name__icontains=topic) |
                        Q(bookshelves__bookshelf__name__icontains=topic)
                    )

        # Filter by Author (case-insensitive partial match, comma-separated)
        if filters.get('author'):
            authors = filters.getlist('author')[0].split(',')
            queryset = queryset.filter(booksauthors__author__name__icontains=' '.join(authors))

        # Filter by Title (case-insensitive partial match, comma-separated)
        if filters.get('title'):
            titles = filters.getlist('title')[0].split(',')
            queryset = queryset.filter(title__icontains=' '.join(titles))

        # Prefetch related objects for the response to avoid additional queries
        queryset = queryset.prefetch_related(
            'booksauthors__author',  # Prefetch authors related to books
            'booklanguages__language',  # Prefetch languages related to books
            'booksubjects__subject',  # Prefetch subjects related to books
            'bookshelves',  # Prefetch bookshelves related to books
            'bookformats'  # Prefetch formats related to books
        )

        return queryset

class BookListView(generics.ListAPIView):
    queryset = Books.objects.all().order_by('-download_count')  # Base queryset
    serializer_class = BookSerializer
    pagination_class = BookPagination  # Pagination class for limiting results
    filter_backends = [BookFilterBackend]  # Specify custom filter backend

    def list(self, request, *args, **kwargs):
        # Fetch filtered queryset based on query params
        queryset = self.filter_queryset(self.get_queryset())

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is needed, serialize and return all books
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),  # Total count of books
            "next": self.get_next_link(),  # Link for the next page
            "previous": self.get_previous_link(),  # Link for the previous page
            "results": serializer.data  # Actual book data (with nested fields)
        })
