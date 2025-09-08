from rest_framework.reverse import reverse


def get_api_url(basename: str, url_path: str, pk: int | None = None) -> str:
    """Получение url для запроса через APIClient."""

    if pk is None:
        return reverse(f'{basename}-{url_path}')
    return reverse(f'{basename}-{url_path}', kwargs={'pk': pk})
