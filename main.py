import gpt_2_simple as gpt2
import os, requests, sys, json, urllib.parse
from requests.structures import CaseInsensitiveDict
from datetime import datetime

token = os.environ['TOKEN']
owner = os.environ['OWNER']

headers = CaseInsensitiveDict()
headers["Accept"] = "application/vnd.github+json"
headers["Authorization"] = "token " + token

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='Multichannel_SgVideosArticles_titles_keywords_v3')
gen_file = 'gpt2_gentext.txt'
gpt2.generate_to_file(sess,
              run_name='Multichannel_SgVideosArticles_titles_keywords_v3',
              length=100,
              temperature=0.8,
              prefix='<|startoftext|>~^~@',
              nsamples=20,
              batch_size=20,
              truncate='<|endoftext|>',
              include_prefix=False,
              top_k=40,
              top_p=0.9,
              destination_path=gen_file                      
              )

open_api_url = f"https://api.github.com/repos/{owner}/gpt2-titlegen/issues" # Close the issue
#data = '{"title":"today","body":'+'finalmsg'+'}'
data = '{"title":"' + datetime.today().strftime("%Y%m%d") + '","body":"' + mailmsg + '"}'
#print(data)
resp = requests.post(open_api_url, headers=headers, data=data)
if resp.status_code == 201: 
  #print(issue_number)
  issue_number = resp.json()["number"]
  print(f'Issue {issue_number} was opened.')

  close_api_url = f"https://api.github.com/repos/{owner}/gpt2-titlegen/issues/{issue_number}" # Close the issue
  data = '{"state":"closed"}'
  resp = requests.patch(close_api_url, headers=headers, data=data)
  if resp.status_code == 200: print(f'Issue {resp.json()["number"]} was closed.')
  else: print(f'Issue {resp.json()["number"]} closing failed with status {resp.status_code}, and reason {resp.reason}')

else: print(resp.status_code, resp.text)
