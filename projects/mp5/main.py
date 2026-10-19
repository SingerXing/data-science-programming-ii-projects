'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP5
Student 1: Singer Xing, mxing7
Student 2: <Name>, <NETID>
Student 3: <Name>, <NETID>
'''
# Add additional imports if needed

import io
import re
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify, make_response, request, Response

# Add implementation here
import pandas as pd
from flask import Flask, request, jsonify
# TODO: Add a comment about your data source
#source of data: https://www.kaggle.com/datasets/junaid512/bmw-car-sales-classification-dataset/data
app = Flask(__name__)
df = pd.read_csv("main.csv")
address_dict = {}
a_counter = 0
b_counter = 0
counter = 0
num_subscribed = 0
@app.route('/')
def home():
    global counter, a_counter, b_counter
    with open("index.html") as f:
        A = f.read()
    B = A.replace("""<ul>
      <li><a href="browse.html">Browse</a></li>
      <li><a href="donate.html?from=A">Donate</a></li>
    </ul>""", """<a href="browse.html">Browse</a>
        <a href="donate.html?from=B">Donate</a>""")
    counter += 1
    if counter <= 10:
        if counter % 2 == 1:
            return A
        else:
            return B
    else:
        if a_counter >= b_counter:
            return A
        if a_counter < b_counter:
            return B
#coverting the csv file to html
with open("browse.html", "w") as f:
    f.write(df.to_html())
#create the browse html page
@app.route('/browse.html')
def browse_page():
    with open("browse.html", 'r') as f:
        browse = f.read()
    return "<html><body><h1>Browse</h1>" + browse + "</body></html>"
#create the browse json page 
@app.route("/browse.json")
def browse_json_page():
    global address_dict
    main_dict = df.to_dict()
    if request.remote_addr not in address_dict or time.time() - address_dict[request.remote_addr] > 60:
        address_dict[request.remote_addr] = time.time()
        return jsonify(main_dict)
    else:
        return Response("Please wait for some time", status = 429 , headers = {'Retry-After': 60})
# create the visitors json page
@app.route("/visitors.json")
def visitors_json_page():
    return list(address_dict.keys())
# create the donation page
@app.route("/donate.html")
def donate_html_page():
    global counter, a_counter, b_counter
    with open("donate.html",'r')as f:
        donate = f.read()
    source = request.args.get("from")
    if source == "A":
        a_counter += 1
    if source == "B":
        b_counter += 1
    return donate
@app.route('/email', methods=["POST"])
#create the subscription
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if len(re.findall(r"^[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]{3}$", email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
            num_subscribed += 1
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify("Invalid Email") # 3
#create the dashboard
def make_dashboard1_svg(bins=20):
    fig, ax = plt.subplots(figsize=(3, 2))
    df["Price_USD"].dropna().plot.hist(ax=ax, bins=bins)
    ax.set_xlabel("The price of BMW M5 in USD")
    ax.set_ylabel("Count")
    plt.tight_layout()

    f = io.BytesIO()
    fig.savefig(f, format="svg")
    plt.close(fig)
    return f.getvalue().decode("utf-8")

def make_dashboard2_svg():
    s = pd.Series(sorted(df["Price_USD"].dropna()))
    rev = pd.Series((s.index + 1) / len(s) * 100, index=s.values)

    fig, ax = plt.subplots(figsize=(3, 2))
    rev.plot.line(ax=ax, ylim=(0, 100), drawstyle="steps-post")
    ax.set_xlabel("The price of BMW M5 in USD")
    ax.set_ylabel("Distribution")
    plt.tight_layout()

    f = io.BytesIO()
    fig.savefig(f, format="svg")
    plt.close(fig)
    return f.getvalue().decode("utf-8")
@app.route("/dashboard1.svg")
def dashboard1():
    bins = request.args.get("bins", default=20, type=int)
    svg = make_dashboard1_svg(bins).encode("utf-8")
    resp = Response(svg)
    resp.content_type = "image/svg+xml"
    return resp

@app.route("/dashboard2.svg")
def dashboard2():
    svg = make_dashboard2_svg().encode("utf-8")
    resp = Response(svg)
    resp.content_type = "image/svg+xml"
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
