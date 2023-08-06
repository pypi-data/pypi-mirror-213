from fuzzywuzzy import fuzz
from urllib.parse import urlparse


def fuzzymatch(orginal_str, match_str):
    return fuzz.ratio(orginal_str, match_str), match_str


def preferred_name(name, list_data, parameter="companyname"):
    result = [fuzzymatch(name, x[parameter]) for x in list_data]
#     print(result)
    tmp_res = []
    m_score = 0
    for i, (score, strg) in enumerate(result):
        if m_score == score:
            tmp_res.append(i)
        elif m_score < score:
            tmp_res = [i]
            m_score = score
    return [list_data[x] for x in tmp_res]


def preferred_website(list_data, parameter="website"):
    tmp = []
    for x in list_data:
        if urlparse(x[parameter]).path.strip() in ["/", ""]:
            tmp.append(x)
    return tmp if tmp else list_data


def preferred_length(list_data):
    tmp = [len(str(x)) for x in list_data]
    tmp_res = []
    m_score = 0
    for i, score in enumerate(tmp):
        if m_score == score:
            tmp_res.append(i)
        elif m_score < score:
            tmp_res = [i]
            m_score = score
    return [list_data[x] for x in tmp_res]