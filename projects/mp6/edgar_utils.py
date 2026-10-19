# Add additional imports if needed

from bisect import bisect
import re
import netaddr
import pandas as pd

# Load IP-to-location data
ips = pd.read_csv("ip2location.csv")


def lookup_region(ip):
    """
    Given an IP address (string), return its region.
    Steps:
    - Clean the IP (replace letters with 0)
    - Convert to integer using netaddr.IPAddress
    - Use bisect on ips["low"] to find the index
    - Return the corresponding region
    """
    # TODO: implement IP lookup
    # replace any letters with 0
    clean_ip = re.sub(r"[A-Za-z]", "0", ip)

    # convert IP string to integer
    ip_int = int(netaddr.IPAddress(clean_ip))

    # find the correct interval
    idx = bisect(ips["low"], ip_int) - 1

    # return the matching region
    return ips.iloc[idx]["region"]


class Filing:
    def __init__(self, html):
        self.dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", html)

        m = re.search(r"SIC=(\d{3,4})", html)
        self.sic = int(m.group(1)) if m else None

        self.addresses = []

        blocks = re.findall(r'<div class="mailer">(.*?)</div>', html, re.DOTALL)

        for block in blocks:
            # turn <br> into line breaks first
            block = re.sub(r"<br\s*/?>", "\n", block)

            # remove all remaining html tags
            text = re.sub(r"<.*?>", "\n", block, flags=re.DOTALL)

            # split into lines and clean spaces
            lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]

            # remove empty lines and label lines
            lines = [
                line for line in lines
                if line and line not in ["Mailing Address", "Business Address"]
            ]

            if lines:
                self.addresses.append("\n".join(lines))

    def state(self):
        for addr in self.addresses:
            m = re.search(r"\b([A-Z]{2})\s+\d{5}(?:-\d{4})?\b", addr)
            if m:
                return m.group(1)
        return None
