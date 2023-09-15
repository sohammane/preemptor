class Pagination:
    page = 1
    limit = 10


def get_pagination(request):
    pagination = Pagination()

    if request.query_params.get("page"):
        try:
            pagination.page = int(request.query_params.get("page"))
        except:
            pass

        if pagination.page <= 0:
            pagination.page = 1

    if request.query_params.get("limit"):
        try:
            pagination.limit = int(request.query_params.get("limit"))
        except:
            pass

        if pagination.limit <= 0:
            pagination.limit = 1

    return pagination


def make_pagination(page):
    return {
        "meta": {
            "total_objects": page.paginator.count,
            "page": {
                "current": page.number,
                "total": page.paginator.num_pages,
                "start_index": page.start_index(),
                "end_index": page.end_index(),
            },
        }
    }


class FieldMixin(object):
    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names

        return super(FieldMixin, self).get_field_names(*args, **kwargs)
