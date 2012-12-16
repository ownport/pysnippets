# XPathSelectors

Based on XPathSelectors from [Scrapy project]<https://github.com/scrapy/scrapy>. Most of this information was taken from original project. XPathSelectors is just a one part fork of Scrapy project. 

When you’re scraping web pages, the most common task you need to perform is to extract data from the HTML source. Scrapy comes with its own mechanism for extracting data. They’re called XPath selectors (or just “selectors”, for short) because they “select” certain parts of the HTML document specified by XPath expressions. XPath selectors are embedded in Scrapy. If you just need to have a mechanism which are allows to extract information from documents without installation whole Scrapy framework, you can use xpathselectors.py. There's only one requirement - lxml library. If Scrapy supports lxml and libxml2 libraries, xpathselectors supports only one - lxml.

XPath is a language for selecting nodes in XML documents, which can also be used with HTML.

This page explains how selectors work and describes their API which is very small and simple, unlike the lxml API which is much bigger because the lxml library can be used for many other tasks, besides selecting markup documents.

## Using selectors

### Constructing selectors

There are two types of selectors bundled with XPathSelectors. Those are:

- HtmlXPathSelector - for working with HTML documents
- XmlXPathSelector - for working with XML documents

Both share the same selector API, and are constructed with a content (string) as their first parameter. 

Example:
```python
hxs = HtmlXPathSelector(response) # a HTML selector
xxs = XmlXPathSelector(response) # a XML selector
```

