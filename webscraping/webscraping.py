#import library modules
from urllib.request import urlopen
#enter web page URL to harvest
url = "https://bmac.libs.uga.edu/pawtucket2/index.php/Browse/objects/row_id/403788/key/2aeefa9336b4bd17c340db5490461cf1"
#open web page and pass URL
page = urlopen(url)
#urlopen () returns an HTTPResponse object
page
#extract HTML from page by reading
html_bytes = page.read()
#decode the returned sequence of bytes
html = html_bytes.decode("utf-8")
#print to see contents of web page
print(html)