from rest_framework import filters


class MessageFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        search_fields = []

        if request.query_params.get('sender'):
            search_fields.append('sender_id')
        if request.query_params.get('recipient'):
            search_fields.append('recipient_id')

        # Default fallback if no filter is applied
        return search_fields or ['sent_at']