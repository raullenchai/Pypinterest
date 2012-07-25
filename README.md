#Pypinterest: A (Homemade) Python Library for Pinterest API#

##Introduction##

This library provides a pure python API to intereact with Pinterest.com, which lets people organize and share all the beautiful things they find on the web. (read more: http://pinterest.com/about/)

##Get the code##

View the trunk at:

https://github.com/raullenchai/Pypinterest


Check out the latest development version anonymously with:

    $ git clone https://github.com/raullenchai/Pypinterest.git


##Preparation##

To use this library, BeautifulSoup library is presumably installed:

    easy_install BeautifulSoup

##Get Started##

To create an instance with login credentials

    >>> from lib import pypinterest
    >>> myclient = Client('email_address', 'username', 'password')

##Board Operations##

To create a new board with a boardname and a boardcategory:

    >>> myclient.createboard('board name', 'board category')


To fetch the existed boards associated to this account:

    >>> boards = myclient.getboards()

To delete an existed board associated to this account:

    >>> boards = myclient.deleteboard('board Name')

##Pin Operations##

To post a new pin:

    >>> myclient.pin('board number', 'title', 'picture url', 'linke to a website', 'content')

To delete a pin:

    >>> myclient.deletepin('pin ID')

To search pins accoriding to a given keyword:

    >>> myclient.searchpins('keywords with spaces', 'number of pages required, say 10')

To repin a post to an existed board:

    >>> myclient.repin('board number', 'pin ID', 'content')

To like a pin:

    >>> myclient.like('pin ID')

To unlike a pin:

    >>> myclient.unlike('pin ID')

To read information from a pin:
    
    >>> myclient.readpin('pin ID')

##Example##
See example.py

##License (MIT)##

    Copyright © 2012 <Raullen Chai>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


##Please Do Not Abuse##

##Contributions are Welcomed##