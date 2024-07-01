import sys
from urllib.parse import urlparse
from urllib.request import urlopen


def verify_args():
    if len(sys.argv) != 2:
        sys.exit("Error! Need a URL as argument.")
    return sys.argv[1]


def is_valid_url(url):
    try:
        r = urlopen(url)
        return r.status == 200
    except Exception as e:
        return False


def is_valid_anchor(url):
    anchor = urlparse(url).fragment
    r = urlopen(url)
    if anchor in str(r.read()):
        print("Anchor: OK")
    else:
        print("Anchor: ERROR")
       
        
if __name__ == "__main__":
    url = verify_args()
    print(f"Checking URL: {url}")
    if is_valid_url(url):
        print("URL: OK")
    else:
        print("URL: ERROR")
    if "#" in url:
        is_valid_anchor(url)
    
