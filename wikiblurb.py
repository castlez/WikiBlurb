'''
WikiBlurb
Jonathan Castle

This little program was an excuse to play around
with REST api calls and GUIs. I plan on using this as
a reference in the future, and may add features to it
for fun.

What it does:
Allows a user to input a query, and then searches the query on wikipedia
and returns the result.
'''

import tkinter as tk
import urllib.request as request
import urllib.parse as parse
import json

# for building the url
base_url = "https://en.wikipedia.org/w/api.php?action=query&titles="
options = "&prop=extracts&exintro=&explaintext=&format=json"

# main driver
class WikiBlurb:

    # execute query on provided subject
    @staticmethod
    def query_wiki(self, q, outplace):
        # try to get the page
        try:
            back = request.urlopen(base_url + parse.quote(q, safe='').title() + options).read()
        except:
            outplace.delete('1.0', tk.END)
            outplace.insert('1.0', "Couldn't get data, something went wrong.")
            return

        # parse the data and present
        data = json.loads(back)
        pages = data['query']['pages']
        first = pages.popitem()
        outplace.delete('1.0', tk.END)
        outplace.insert('1.0', str(first[1]['extract']))

    # initialization
    def __init__(self, master):
        self.master = master

        # search input
        q = tk.StringVar(master=False)
        qbox = tk.Entry(master, textvariable=q)

        # scrollable box for output
        outbox = tk.Text(master)
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        outbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=outbox.yview)

        # button to excute query (or press enter)
        master.bind('<Return>', lambda x: self.query_wiki(q.get(), outbox))
        qbut = tk.Button(master, text="Get Blurb", command=lambda: self.query_wiki(q.get(), outbox))

        # put all the widgets in the window
        qbox.pack()
        qbut.pack()
        outbox.pack()
        print("job's done")


# startup
root = tk.Tk()
root.title("WikiBlurb")
my_gui = WikiBlurb(root)
root.mainloop()
