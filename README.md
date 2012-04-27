#Pypinpinpin: An Unofficial (and Somewhat Dirty) Python API for Pinterest#

Author: *Raullen Chai <raullen@live.ca>*

##Introduction##

This (sketchy) library provides a pure python API to intereact with Pinterest.com, which lets people organize and share all the beautiful things they find on the web. (read more: http://pinterest.com/about/)

##Getting the code##

View the trunk at:

https://github.com/raullenchai/Pypinpinpin

Check out the latest development version anonymously with:

    $ git clone git@github.com:raullenchai/Pypinpinpin.git


##Using##

To use this library, BeautifulSoup library is presumably installed:

    easy_install BeautifulSoup


To create an instance with login credentials

    >>> from pinpinpin import *
    >>> myclient = Client('email_address', 'username', 'password')
    >>> myclient.login()
    Login successful (via cookie)


To fetch the existed boards associated to this account:

    >>> boards = myclient.getboards()
    >>> print boards
    {'Security &amp; Cryptography': '207447195274734789', 'Products I Love': '207447195274734682', 'Love in Love': '207447195274748396', 'My Style': '207447195274734681', 'Books Worth Reading': '207447195274734680', 'Technology': '207447195274734901', 'Charity': '207447195274734927'}


To create a new board with a boardname and a boardcategory, where boardcategory should be one of ['architecture', 'art', 'cars_motorcycles', 'design', 'diy_crafts', 'education', 'film_music_books', 'fitness', 'food_drink', 'gardening', 'geek', 'hair_beauty', 'history', 'holidays', 'home', 'humor', 'kids', 'mylife', 'women_apparel', 'men_apparel', 'outdoors', 'people', 'pets', 'photography', 'prints_posters', 'products', 'science', 'sports', 'technology', 'travel_places', 'wedding_events', 'other']:

    >>> myclient.createboard('Board Name', 'Board Category')
    [Board Name] in [Board Category] has been created!


To post a new pin with a boardno, postname, pic_url, link and content:

    >>> myclient.post('207447195274748396', 'super cutie', 'http://media-cache1.pinterest.com/upload/37576978111134514_onq8DrX9_f.jpg', 'http://www.hotoday.net/', 'I love this one!!!!!!')
    'Posted!'


To search posts accoriding to a given keyword:

    >>> ids, contents = myclient.searchpins('super woman')
    >>> print ids
    >>> print contents


To repin a post to an existed board with boardno, postid, content:
    >>> myclient.repin('207447195274748396', '116741815310976060', 'cute')
    'Repined'

To like a post with a specific postid:
    >>> myclient.like('116741815310976060')
    Liked


##License (MIT)##

    Copyright © 2012 <Raullen Chai>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


##Please Do Not Abuse##

##Contributions are Welcomed##