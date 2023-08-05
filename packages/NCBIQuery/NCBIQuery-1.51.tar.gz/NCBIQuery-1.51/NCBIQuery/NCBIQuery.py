import os
import html
import requests
import xml.etree.ElementTree as ET
from tokenizers import ByteLevelBPETokenizer


base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

def query_id(db='pubmed', search_field_tags='tw', contents='', retmax=10000):
    if not isinstance(search_field_tags, list):
        search_field_tags = [search_field_tags]
    if not isinstance(contents, list):
        contents = [contents]
    n = min(len(search_field_tags), len(contents))
    if n < 1:
        return []
    query_string = contents[0] + '[' + search_field_tags[0] + ']'
    for i in range(1, n):
        query_string += ' AND ' + contents[i] + '[' + search_field_tags[i] + ']'
    query_string = html.escape(query_string)
    retmax = min(retmax, 10000) # Maximum number of results returning for a query is 10000
    search_url = base + 'esearch.fcgi?db=' + db + '&term=' + query_string + '&usehistory=y&retmax=' + str(retmax) + '&sort=relevance' # Records are sorted based on relevance to your search. For more information about PubMed’s relevance ranking, see the PubMed Help section on Computation of Weighted Relevance Order in PubMed.
    res = requests.get(search_url).content
    search_et = ET.fromstring(res)
    search_ids = []
    for child in search_et.iter('*'):
        if child.tag == 'Id':
            search_ids.append(child.text)
    return search_ids

def id_abstract(search_ids, db='pubmed'):
    def get_article_info(article_ids):
        url = base + 'efetch.fcgi'
        res = requests.post(url, data={'db':db, 'id':article_ids}).content
        et = ET.fromstring(res)
        return et
    if not isinstance(search_ids, list):
        search_ids = [search_ids]
    article_abstracts = []
    article_infos = get_article_info(search_ids)
    for article in article_infos:
        abstract = ''
        for child in article.iter('*'):
            if child.tag == 'AbstractText':
                if child.text is not None:
                    abstract = child.text
                break
        article_abstracts.append(abstract)
    return article_abstracts

def query_abstract(db='pubmed', search_field_tags='tw', contents='', retmax=10000):
    search_ids = query_id(db, search_field_tags, contents, retmax)
    return id_abstract(search_ids, db)
