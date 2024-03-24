import requests

from rest_api.models import URLModel
from bs4 import BeautifulSoup as bs


def url_validity_check():
    list_urls = URLModel.objects.all()
    for url_object in list_urls:
        url = url_object.url
        try:
            """
            beatifulsoup: https://www.tutorialspoint.com/extract-the-title-from-a-webpage-using-python
            web scapper
            """

            response = requests.get(url)
            status_code = int(response.status_code)
            soup = bs(response.content, "html.parser")
            title = soup.title.string

        except:
            status_code = 400
            title = None

        url_object.status_code = status_code
        url_object.title = title
        url_object.save()
