from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden


class OwnershipRequiredMixin:
    """
    adapted from: https://stackoverflow.com/a/54592371
    """

    def dispatch(self, request: HttpRequest, *args, **kwargs: Any) -> HttpResponse:
        if self.object.owner != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
