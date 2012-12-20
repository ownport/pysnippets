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
hxs = HtmlXPathSelector(content) # a HTML selector
xxs = XmlXPathSelector(content) # a XML selector
```
To explain how to use the selectors we’ll use the next HTML code (html_content variable):
```html
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>
```
Since we’re dealing with HTML, we’ll be using the HtmlXPathSelector
```python
>>> import xpathselectors
>>> hxs = xpathselectors.HtmlXPathSelector(html_content)
>>> hxs.select('//title/text()')
[<HtmlXPathSelector xpath='//title/text()' data=u'Example website'>]
```
As you can see, the select() method returns an XPathSelectorList, which is a list of new selectors. This API can be used quickly for extracting nested data.

To actually extract the textual data, you must call the selector extract() method, as follows:
```python
>>> hxs.select('//title/text()').extract()
[u'Example website']
```
Now we’re going to get the base URL and some image links:
```python
>>> hxs.select('//base/@href').extract()
[u'http://example.com/']
>>>
>>> hxs.select('//a[contains(@href, "image")]/@href').extract()
[u'image1.html', u'image2.html', u'image3.html', u'image4.html', u'image5.html']
>>> hxs.select('//a[contains(@href, "image")]/img/@src').extract()
[u'image1_thumb.jpg', u'image2_thumb.jpg', u'image3_thumb.jpg', u'image4_thumb.jpg', u'image5_thumb.jpg']
>>>
```
### Using selectors with regular expressions

Selectors also have a re() method for extracting data using regular expressions. However, unlike using the select() method, the re() method does not return a list of XPathSelector objects, so you can’t construct nested .re() calls.

Here’s an example used to extract images names from the HTML code above:
```python
>>> hxs.select('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')
[u'My image 1 ', u'My image 2 ', u'My image 3 ', u'My image 4 ', u'My image 5 ']
```

### Nesting selectors

The select() selector method returns a list of selectors, so you can call the select() for those selectors too. Here’s an example:
```python
>>> links = hxs.select('//a[contains(@href, "image")]')
>>> links.extract()
[u'<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>',
 u'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>',
 u'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>',
 u'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>',
 u'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']

>>> for index, link in enumerate(links):
        args = (index, link.select('@href').extract(), link.select('img/@src').extract())
        print 'Link number %d points to url %s and image %s' % args

Link number 0 points to url [u'image1.html'] and image [u'image1_thumb.jpg']
Link number 1 points to url [u'image2.html'] and image [u'image2_thumb.jpg']
Link number 2 points to url [u'image3.html'] and image [u'image3_thumb.jpg']
Link number 3 points to url [u'image4.html'] and image [u'image4_thumb.jpg']
Link number 4 points to url [u'image5.html'] and image [u'image5_thumb.jpg']
```


