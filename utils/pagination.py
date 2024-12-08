from rest_framework.pagination import LimitOffsetPagination


class MyCustomPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 49