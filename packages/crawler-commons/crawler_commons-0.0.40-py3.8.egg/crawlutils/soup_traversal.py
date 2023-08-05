import re
from typing import List, Tuple
from bs4 import PageElement
from crawlutils.num_utils import defaultIfNumber
from crawlutils.text_utils import remove_strs


def get_td(td_list: List[PageElement], *text_in) -> PageElement:
    """
    해당 keyword 를 포함하는 td 를 찾아서 반환한다.
    :param td_list:
    :param text_in:
    :return:
    """
    for td in td_list:
        for text in text_in:
            if text in td.text.replace(" ", ""):
                return td
    return None

def get_td_regex(td_list: List[PageElement], regex) -> PageElement:
    """
    해당 keyword 를 포함하는 td 를 찾아서 반환한다.
    :param td_list:
    :param text_in:
    :return:
    """
    compiled_regex = re.compile(regex)
    for td in td_list:
        if compiled_regex.search(td.text.replace(" ", "")):
            return td
    return None


def get_td_text(td_list: List[PageElement], *text_in) -> str:
    """
    해당 td 를 찾아서 그 다음 td 의 text 를 가져온다.
    :param td_list:
    :param text_in:
    :return:
    """
    r = get_td(td_list, *text_in)
    return r.findNext('td').text.strip() if r is not None else r


def get_td_value(td_list: List[PageElement], *text_in) -> str:
    """
    해당 td 를 찾아서 그 다음 td 의 text 를 가져온다.
    :param td_list:
    :param text_in:
    :return:
    """
    r = get_td(td_list, *text_in)
    return r.findNext('td').text.strip() if r is not None else r


def get_td_text_regex(td_list: List[PageElement], regex) -> str:
    """
    해당 td 를 찾아서 그 다음 td 의 text 를 가져온다.
    :param td_list:
    :param text_in:
    :return:
    """
    r = get_td_regex(td_list, regex)
    return r.findNext('td').text.strip() if r is not None else r

def get_td_value_after(td_anchor: PageElement, limit=5, *keyword) -> str:
    """
    :param td_anchor: 기준이 되는 td
    :param limit: anchor 부모 tr 로 부터 몇개의 tr 을 가져올 것인지
    :param keyword: 찾으려는 키워드, 가변키워드, 우선순위가 높은 키워드 부터
    :return:
    """
    if td_anchor is None:
        return None
    trs: List[PageElement] = td_anchor.parent.findNextSiblings('tr')

    if len(trs) < 1:
        return None

    trs = trs[:limit]
    tds = []
    for tr in trs:
        tds.extend(tr.findAll('td'))

    return get_td_value(tds, *keyword)


def find_tr_has_text(text, trlist) -> PageElement:
    target_tr = None
    for tr in trlist:
        if text in tr.text.replace(' ', ''):
            target_tr = tr
            break
    return target_tr


def find_table_has_text(table_list: List[PageElement], *keywords) -> PageElement:
    for table in table_list:
        for keyword in keywords:
            if keyword in table.text.replace(' ', ''):
                return table
    return None


def find_table(tables: List[PageElement], contains_any: List[str], not_contains_any: List[str] = None, contains_all: List[str] = None, not_contains_all: List[str] = None):
    for table in tables:
        table_text = remove_strs(table.text, [" ", "\n", "\t", "\xa0"])
        if contains_any and not any([text in table_text for text in contains_any]):
            continue
        if not_contains_any and any([text in table_text for text in not_contains_any]):
            continue
        if contains_all and not all([text in table_text for text in contains_all]):
            continue
        if not_contains_all and all([text in table_text for text in not_contains_all]):
            continue
        return table
    return None


def extract_correction(tables: List[PageElement]) -> Tuple[str, str]:
    """
    정정관련 정보 추출
    :param tables:
    :return: Tuple(corr_reason, corr_date)
    """
    mod_table = find_table(tables, contains_any=["정정사유", "정정전"])
    if mod_table is not None:
        mod_td_list = mod_table.findAll('td')
        correction_reason = get_td_value(mod_td_list, '정정사유')
        correction_date = get_td_value(mod_td_list, '공시서류제출일')
        return correction_reason, correction_date
    return None, None


def defaultNumberInTR(text, tr3, unit_multiplier, default="-"):
    np_tr = find_tr_has_text(text, tr3)
    np = defaultIfNumber(np_tr.findAll('td')[1].text, unit_multiplier, default=default)
    return np