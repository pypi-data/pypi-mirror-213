import re
import time
import requests
from TheSilent.clear import clear
from TheSilent.link_scanner import link_scanner
from TheSilent.return_user_agent import return_user_agent

CYAN = "\033[1;36m"
RED = "\033[1;31m"

# create html sessions object
web_session = requests.Session()

tor_proxy = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050"}

# increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

# increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

def html_lint(url, secure=True, tor=False):
    clear()
    
    if url.startswith("https://") or url.startswith("http://"):
        if url.count("/") == 2:
            if url.endswith("/"):
                my_url = url

            else:
                my_url = url + "/"

        else:
            my_url = url

    else:
        if secure:
            if url.count("/") == 0:
                if url.endswith("/"):
                    my_url = "https://" + url

                else:
                    my_url = "https://" + url + "/"

            else:
                my_url = "https://" + url

        else:
            if url.count("/") == 0:
                if url.endswith("/"):
                    my_url = "http://" + url

                else:
                    my_url = "http://" + url + "/"

            else:
                my_url = "http://" + url

    linted = []
    
    print(CYAN + "checking: " + my_url)

    try:
        if tor:
            result = web_session.get(my_url, verify=False, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120)).text.lower()

        else:
            result = web_session.get(my_url, verify=False, headers={"User-Agent": return_user_agent()}, timeout=(5,30)).text.lower()

        area_tag = re.findall("<area.+>", result)

        for area in area_tag:
            if "alt" not in area:
                print(RED + f"no alt in area tag detected on {crawl}. Consider using alt (accessibility).")
                linted.append(f"no alt in area tag detected on {crawl}. Consider using alt (accessibility).")

        image_tag = re.findall("<img.+>", result)

        for image in image_tag:
            if "alt" not in image:
                print(RED + f"no alt in img tag detected on {crawl}. Consider using alt (accessibility).")
                linted.append(f"no alt in img tag detected on {crawl}. Consider using alt (accessibility).")

        input_tag = re.findall("<input.+>", result)

        for my_input in input_tag:
            if "alt" not in my_input and "image" in my_input:
                print(RED + f"no alt in input image tag detected on {crawl}. Consider using alt (accessibility).")
                linted.append(f"no alt in input image tag detected on {crawl}. Consider using alt (accessibility).")

        if "<b>" in result:
            print(RED + f"<b> detected on {crawl}. Consider using <strong> (accessibility).")
            linted.append(f"<b> detected on {crawl}. Consider using <strong> (accessibility).")

        if "document.write" in result:
            print(RED + f"document.write detected on {crawl}. This has weird behavior (behavior).")
            linted.append(f"document.write detected on {crawl}. This has weird behavior (behavior).")

        if "<i>" in result:
            print(RED + f"<i> detected on {crawl}. Consider using <em> (accessibility).")
            linted.append(f"<i> detected on {crawl}. Consider using <em> (accessibility).")

        if "innerhtml" in result:
            print(RED + f"innerhtml detected on {crawl}. This could lead to a security vulnerability (security).")
            linted.append(f"innerhtml detected on {crawl}. This could lead to a security vulnerability (security).")

    except:
        pass

    linted = list(set(linted))
    linted.sort()
    
    print(CYAN + "")
    clear()
    
    return linted
