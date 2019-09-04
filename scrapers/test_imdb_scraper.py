from . import IMDbSpider
from . import UrlWithCategories
from scrapy.http import TextResponse, Request

def fake_response(url_with_categories, content):
    url = url_with_categories.url
    category = url_with_categories.category
    subcategory = url_with_categories.subcategory
    return TextResponse(
        url = url,
        body = content,
        encoding = 'utf-8',
        request = Request(url = url, meta = {'category': category, 'subcategory': subcategory})
    )

html = open('scrapers/test_data/imbd_movies_action.html', 'r').read()

def test_should_return_empty_list_from_empty_input():
    #given
    url = UrlWithCategories('https://www.imdb.com/search/title/?genres=action&title_type=feature&explore=genres', 'movie', 'action')
    test_response = fake_response(url, '')
    object_under_test = IMDbSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    assert list(response) == []

def test_should_return_50_results():
    #given
    url = UrlWithCategories('https://www.imdb.com/search/title/?genres=action&title_type=feature&explore=genres', 'movie', 'action')
    test_response = fake_response(url, html)

    object_under_test = IMDbSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    response_as_list = list(response)
    assert len(response_as_list) == 50

def test_should_return_the_first_element():
    #given
    url = UrlWithCategories('https://www.imdb.com/search/title/?genres=action&title_type=feature&explore=genres', 'movie', 'action')
    test_response = fake_response(url, html)

    object_under_test = IMDbSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    response_as_list = list(response)
    assert response_as_list[0] == {
        'topic': 'Star Wars: The Rise of Skywalker',
        'category': 'movie',
        'subcategory': 'action',
        'url': 'https://www.imdb.com/title/tt2527338/?ref_=adv_li_tt'
    }

def test_should_return_three_elements():
    #given
    url = UrlWithCategories('https://www.imdb.com/search/title/?genres=action&title_type=feature&explore=genres', 'movie', 'action')
    test_response = fake_response(url, html)

    object_under_test = IMDbSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    response_as_list = list(response)
    assert response_as_list[0] == {
        'topic': 'Star Wars: The Rise of Skywalker',
        'category': 'movie',
        'subcategory': 'action',
        'url': 'https://www.imdb.com/title/tt2527338/?ref_=adv_li_tt'
    }

    assert response_as_list[1] == {
        'topic': 'Angel Has Fallen',
        'category': 'movie',
        'subcategory': 'action',
        'url': 'https://www.imdb.com/title/tt6189022/?ref_=adv_li_tt'
    }

    assert response_as_list[2] == {
        'topic': 'Terminator: Dark Fate',
        'category': 'movie',
        'subcategory': 'action',
        'url': 'https://www.imdb.com/title/tt6450804/?ref_=adv_li_tt'
    }