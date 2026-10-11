from django_tables2.paginators import LazyPaginator
from django.core.paginator import Page

class LimitedLazyPaginator(LazyPaginator):
    MAX_PAGES = 1024
    
    def page(self, number):
        number = self.validate_number(number)
        if number > self.MAX_PAGES:
            # Return an empty page - no error, just empty table
            return Page([], number, self)
        return super().page(number)
    
    def validate_number(self, number):
        # Don't raise exception for high page numbers, just validate format
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            from django.core.paginator import PageNotAnInteger
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            from django.core.paginator import EmptyPage
            raise EmptyPage('That page number is less than 1')
        return number
    
    @property
    def num_pages(self):
        """Return the maximum number of pages or actual pages, whichever is smaller."""
        actual_pages = super().num_pages
        return min(actual_pages, self.MAX_PAGES)

