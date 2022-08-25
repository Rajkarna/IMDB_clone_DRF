from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size" 
    max_page_size = 5
    # last_page_strings = "end" default = last

class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 3 
    # max_limit = 4
    
class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = "created"
    cursor_query_param = "record"