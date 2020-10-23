
import urllib
import sys
from datetime import datetime
from urllib.request import urlopen


# print all the first cell of all the rows
# for row in cur.fetchall():
#    print row[0]


def scrap(n):
    id = str(n)
    url = "http://sinhala.adaderana.lk/"
    print(url)

    # Fetch URL
    request = urllib.request.Request(url)
    request.add_header('Accept-Encoding', 'utf-8')

    response = urlopen(request, "lxml")
    # Response has UTF-8 charset header,
    # and HTML body which is UTF-8 encoded
    print(response)
    return

    # Parse with BeautifulSou

    # get title
    h1s = soup.find_all("h2", {"class": "completeNewsTitle"})

    # if title not found, stop the execution
    if len(h1s) < 1:
        print("An error occurred!")
        return

    title = h1s[0].get_text().strip()
    if len(title) < 1:
        print("An error occurred!")
        return
    print(title.encode('utf8'))

    # get date and time
    date = soup.find_all("p", {"class": "newsDateStamp"})
    if len(date) < 1:
        print("An error occurred!")
        return
    date = date[0].get_text().encode('utf-8').strip()
    # convert date time to a common format
    # given -> January 1, 2017&nbsp;&nbsp;10:45 am
    date = date.replace("\xc2\xa0\xc2\xa0", " ")
    date = datetime.strptime(date, '%B %d, %Y %I:%M %p')
    date = str(date)
    print(date)

    # get article content
    contents = soup.find_all("div", {"class": "newsContent"})
    contents = contents[0].get_text().strip()

    # save content to a file
    file = open("adaderana_" + id + ".txt", "w")  # docs/
    file.write("<title>" + title.encode('utf8') + "</title>\n")
    file.write("<time>" + date.encode('utf8') + "</time>\n")
    # file.write("<author></author>\n")
    file.write("<body>" + contents.encode('utf8') + "</body>")
    file.close()

# scrap news items by id (from 2017/01/01 to present)
if __name__ == '__main__':
    for n in range(67571, 67572):
        scrap(n)
        print("\n===============================\n\n")
