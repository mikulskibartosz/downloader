from . import SteamSpider
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

html = open('scrapers/test_data/steam_games_racing.html', 'r').read()

def test_should_return_empty_list_from_empty_input():
    #given
    url = UrlWithCategories('https://store.steampowered.com/tags/en/Racing/', 'game', 'racing')
    test_response = fake_response(url, '')
    object_under_test = SteamSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    assert list(response) == []

def test_should_return_15_results():
    #given
    url = UrlWithCategories('https://store.steampowered.com/tags/en/Racing/', 'game', 'racing')
    test_response = fake_response(url, html)

    object_under_test = SteamSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    response_as_list = list(response)
    assert len(response_as_list) == 15

def test_should_return_the_first_element():
    #given
    url = UrlWithCategories('https://store.steampowered.com/tags/en/Racing/', 'game', 'racing')
    test_response = fake_response(url, html)

    object_under_test = SteamSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    response_as_list = list(response)
    assert response_as_list[0] == {
        'topic': 'Deep Race: Battle',
        'category': 'game',
        'subcategory': 'racing',
        'url': 'https://store.steampowered.com/app/1136830/Deep_Race_Battle/?snr=1_241_4_racing_103'
    }

    assert len(response_as_list) == 15

def test_should_return_three_elements():
    #given
    url = UrlWithCategories('https://store.steampowered.com/tags/en/Racing/', 'game', 'racing')
    test_response = fake_response(url, html)

    object_under_test = SteamSpider([url])

    #when
    response = object_under_test.parse(test_response)

    #then
    response_as_list = list(response)
    assert response_as_list[0] == {
        'topic': 'Deep Race: Battle',
        'category': 'game',
        'subcategory': 'racing',
        'url': 'https://store.steampowered.com/app/1136830/Deep_Race_Battle/?snr=1_241_4_racing_103'
    }

    assert response_as_list[1] == {
        'topic': 'MXGP 2019 - The Official Motocross Videogame',
        'category': 'game',
        'subcategory': 'racing',
        'url': 'https://store.steampowered.com/app/1018160/MXGP_2019__The_Official_Motocross_Videogame/?snr=1_241_4_racing_103'
    }

    assert response_as_list[2] == {
        'topic': 'CRAZY DRIVER',
        'category': 'game',
        'subcategory': 'racing',
        'url': 'https://store.steampowered.com/app/1101760/CRAZY_DRIVER/?snr=1_241_4_racing_103'
    }
