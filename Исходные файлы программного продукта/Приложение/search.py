from getpass import fallback_getpass

import requests
import trafilatura, httpx
import prompts
import olama_commands
max_links = 10

def get_links(q:str) -> dict:
    url = "http://localhost:8080/search"
    params = {
        "q": q,
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    links = {}
    print(data['results'])
    for link in data['results']:
        links[link['title']] = link['url']
    # print('Cсылки собраны')
    return links

# def get_text_from_urls(urls:dict) -> (str):
#     result = ''
#     if len(urls) == 0:
#         return None
#     i = 0
#     for titel in urls:
#         html = httpx.get(urls[titel], timeout=10, verify=False).text
#         metadata = trafilatura.extract_metadata(html)
#         result +=  '\n\nИсточник: '+metadata.sitename + ' Автор: ' + metadata.author + '\n\n'
#         text = trafilatura.extract(html)
#         if metadata.date != None:
#             result += 'Дата: '+ metadata.date + '\n\n'
#             # print('Дата: '+ metadata.date)
#         if text != None:
#             result += trafilatura.extract(html)
#             i += 1
#             if i >= max_links:
#                 break
#         # print('Источник: ' + titel + "проверен")
#     # print(result)
#     return result

def get_text_from_url(url:str) -> (str, str):
    try:
        html = httpx.get(url, timeout=10, verify=False).text
        metadata = trafilatura.extract_metadata(html)
        result_metadata = ''
        result_metadata += '\nИсточник: '+metadata.sitename + 'Ссылка: '+ url + '\n'
        text = trafilatura.extract(html)
        if metadata.date != None:
            result_metadata += 'Дата: ' + metadata.date
        if text != None:
            result = trafilatura.extract(html)
            return result, result_metadata
        return None, None
    except:
        return None, None

# def check_news(request:str, facts:str) -> str:
#     links = get_links(request)
#     result = ''
#     if len(links) == 0:
#         return None
#
#     for titel in links:
#         print("\n\n\n\n\n\n\n"+links[titel])
#         print(get_text_from_url(titel, links[titel]))
#         one_article_text, metadata = get_text_from_url(titel, links[titel])
#         if one_article_text is not None:
#             prompt = prompts.ARTICLE_CHECK_PROMPT.format(news=facts, article=one_article_text)
#             res = olama_commands.to_ollama(prompt)
#             result += f"\n\n\n\nLength:{len(res)}\n\n"+metadata + "\n" + res+'\n\n'
#     return result
def compress_text(text:str) -> str:
    prompt = prompts.COMPRESS_NEWS_PROMPT.format(news=text)
    return olama_commands.to_ollama(prompt, 0)

def compress_news(request:str):
    links = get_links(request)
    result = ''
    if len(links) == 0:
        return None
    n = 0
    for title in links:
        # print("\n\n\n\n" + links[title])
        one_article_text, metadata = get_text_from_url(links[title])
        # print(one_article_text, metadata)
        if one_article_text is not None:
            res = compress_text(one_article_text)
            # isAdd, text = check_text(res, request)
            # print("\n\n\nДОБАВЛЯЕМ: " +isAdd+"\n\n\n"+ text)
            # if isAdd:
            result += f"\n\n\n\nLength:{len(res)}\n" + metadata + "\n" + res + '\n'
            n += 1
            if n >= max_links:
                print("Выход по max_link")
                break
    print("\n\n\nСтатей найдено: "+str(n))
    return result

def check_text(text:str, fact:str) -> (str, str):
    prompt = prompts.ARTICLE_CHECK_PROMPT.format(article=text, news=fact)
    return olama_commands.to_ollama(prompt, 1), text
    return 'q', text


#print(get_links("ИИ-слоп победил в номинации «Выбор народа» за 2025 год по версии австралийского словаря Macquarie Dictionary"))
# print(get_text_from_urls(get_links("коносуба обзор")))