from tda import auth, client
import os, json, datetime
from chalice import Chalice
from chalicelib import config
import requests as req
import math as mm
from datetime import date

today = date.today()

d1 = today.strftime("%Y")
d2 = today.strftime("%m")
d3 = today.strftime("%d")
#this is to determine day of expiry

app = Chalice(app_name='my_app')
token_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'token')

c = auth.client_from_token_file(token_path, config.api_key)
#post trade here
url = 'aws.my_url.com/option/order'

#get option symbol autonomously. find closest expiry date
# round up price of say SPY
dat=d1[-1]+d1[2] + d2[0]+d2[-1] +d3[0]+d3[1]
sym="SPY_'+dat+"C"+str(mm.ceil(c.get_quote("SPY")["price"]))+'"'
if c.PriceHistory.Period.ONE_DAY[0] > c.PriceHistory.Period.ONE_DAY[1]:
  myobj = {
"instruction": "BUY_TO_OPEN",
"symbol": "SPY_220325C420",
"quantity": 1,
"passphrase":"xyz"
  }
  x = requests.post(url, data = myobj) # This actually places the trade

  # This is just an example. An easy template for future reference
  # I don't wish to reveal my strategies.
  # I used to use if else statements, but now I input all my parameters into directed graphs
  # self.confidence = confidence
  # self.next = next
  # I then run a depth first search adding up all the confidence values until my desired value is used
class Node:
    def __init__(self, confidence):
        self.val = confidence
        self.edges = []
def sigmoid(conf):
  return 1/(1+exp(-conf))
class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
    
    def add_node(self, confidence):
        newNode = Node(confidence)
        self.nodes.append(newNode)

    def add_edge(self, node1, node2):
        node1.edges.append(node2)
        node2.edges.append(node1)
    def dfs(self):
      conf=0
      if self.nodes is None:
          return NULL
      visited, to_visit = [], [self.nodes[0]]
      while to_visit: # I HATE recursion. I will always do searches iteratively
        # recursion leads to uncertainty
          node = to_visit.pop() #if bfs just use popleft. it's that easy!
          conf+=node.confidence
          visited.append(node)
          
          for n in node.edges:
              if n not in visited and n not in to_visit:
                  to_visit.append(n)
      if sigmoid(conf)>0.88351:
        return True
# I use ML techniques to figure out optimal confidence values
# This was amazing for runtime!
# I had the runtime reduce from ~8 seconds to 1265 ms. Graphs simplify and complicate things
