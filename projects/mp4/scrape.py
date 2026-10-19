'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: Singer Xing, mxing7
Student 2: None
Student 3: None
'''

# Add additional imports if needed
import os
from collections import deque
from io import StringIO
import time
import requests
import pandas as pd
from selenium.webdriver.common.by import By

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ 
        Leave this method as is! It will be over-written the child classes
        Each child class should perform the following:
            Record the node value in self.order AND return its children
            parameter: node
            return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)
    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return 
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
    def bfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        self.bfs_visit(node)
    def bfs_visit(self, node):
        to_visit = deque([node])
        while len(to_visit) > 0:
            node = to_visit.popleft()
            if node in self.visited:
                continue
            self.visited.add(node)
            to_visit.extend(self.visit_and_get_children(node))        


class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        for child, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(child)
        # TODO: use `self.df` to determine what children the node has and append them
        return children



class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()

    def visit_and_get_children(self, node):
        # TODO: open the file in file_nodes, then parse the value and children
        path = os.path.join('file_nodes',node)
        with open(path) as f:
            content = f.read()
            self.order.append(content.split()[0])
            children = content.split()[1].split(',')
        # TODO: record value in self.order
        return children

    def concat_order(self):
        # TODO: return joined string of self.order
        return ''.join(self.order)


class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tables = []

    def visit_and_get_children(self, node):
        # TODO: record node in self.order
        self.order.append(node)
        # TODO: fetch the page, parse HTML table into pandas, store it
        self.driver.get(node)
        dfs = pd.read_html(self.driver.page_source)
        # TODO: return list of links (<a> tags)
        if len(dfs) > 0:
            self.tables.append(dfs[0])

        links = self.driver.find_elements(By.TAG_NAME, "a")
        children = []
        for link in links:
            href = link.get_attribute("href")
            if href:
                children.append(href)

        return children 

    def table(self):
        # TODO: return combined DataFrame
        return pd.concat(self.tables, ignore_index=True)


def get_password(travellog):
    """
    Given a DataFrame-like object with a 'clue' column,
    combine values into a password string.
    """
    # TODO: build string from travellog['clue']
    return ''.join(travellog['clue'].astype(str))

# def reveal_secrets(driver, url, travellog):
#     driver.get(url)
#     time.sleep(1)
#     print(driver.page_source)
#     return ""
def reveal_secrets(driver, url, travellog):
    """
    Automate secret-revealing:
    1. Generate clue/password
    2. Enter password into webpage
    3. Click buttons, wait for image
    4. Save image
    5. Return the location text
    """
    # TODO: implement using Selenium driver, retries, and requests
    driver.get(url)
    password = get_password(travellog)
    
    text = driver.find_element(By.ID, 'password-textbox')
    text.send_keys(password)
    
    button = driver.find_element(By.ID, "submit-button")
    button.click()
    
    time.sleep(2)
    
    view_location_button = driver.find_element(By.XPATH, "//*[contains(text(), 'View Location')]")
    view_location_button.click()
    
    time.sleep(2)
    
    location = driver.find_element(By.ID, "location")
    
    imgs = driver.find_elements(By.TAG_NAME, "img")
    img_url = imgs[-1].get_attribute("src")

    response = requests.get(img_url)
    with open("Current_Location.jpg", "wb") as f:
        f.write(response.content)
    return location.text
    
    