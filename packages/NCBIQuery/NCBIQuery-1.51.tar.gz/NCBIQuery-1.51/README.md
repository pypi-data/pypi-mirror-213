 # NCBIQuery
Python tool of National Center for Biotechnology Information (NCBI) paper query based on [E-utilities](https://dataguide.nlm.nih.gov/eutilities/utilities.html).

Installing
============

    pip install NCBIQuery

Usage
=====
    
See [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/) for detailed search field tags and usages.

### query_id()

Query paper ids from search text.

Arguments:
| Parameter                 | Default       | Description   |   
| :------------------------ |:-------------:| :-------------|
| db           |    pubmed           |  The database which you search from |
| search_field_tags          | tw           | A list of (or a single) search field tag(s) |
| contents         |                    | A list of (or a single) search content(s) corresponding to each tag |
| retmax           |        10000            | The maximum number of papers to return (cannot exceed 10000) |

Return: A list of paper ids.
### query_abstract()

Get paper abstracts from search text.

Arguments:
| Parameter                 | Default       | Description   |   
| :------------------------ |:-------------:| :-------------|
| db           |    pubmed           |  The database which you search from |
| search_field_tags          | tw           | A list of (or a single) search field tag(s) |
| contents         |                    | A list of (or a single) search content(s) corresponding to each tag |
| retmax           |        10000            | The maximum number of papers to return (cannot exceed 10000) |

Return: A list of paper abstracts.

### id_abstract()

Get paper abstracts from id.

Arguments:
| Parameter                 | Default       | Description   |   
| :------------------------ |:-------------:| :-------------|
| search_ids           |               |  A list of (or a single) paper id(s) |
| db           |    pubmed           |  The database from which you search from |

Return: A list of paper abstracts.
    
Example
=====
    >>> import NCBIQuery
    >>> print(NCBIQuery.query_id('pubmed', ['tw'], ['cell'],retmax=50))
    >>> print(NCBIQuery.query_abstract('pubmed', ['tw','pt', 'dp'], ['cell','review', '1990/01/01:2023/01/01'], retmax=50))
    >>> print()