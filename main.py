import gpt_2_simple as gpt2
from datetime import datetime
import smtplib, ssl # For emailer
from email.message import EmailMessage

receiverid = os.environ['receiverid']
senderid = os.environ['senderid']
mailpassword = os.environ['mailpass']

def sendmail(mailmessage):
  if mailmessage != '':
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg['Subject'] = 'Reddit Jokes Update'
    msg['To'] = receiverid 
    msg['From'] = senderid
    msg.set_content(mailmessage)
    print(mailmessage)
    #for receiverid in receiverids: # Send mail to all receiver ids
    print('Sending email')
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(senderid, mailpassword)
        server.send_message(msg)
        
    print('Email sent')
    
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

with open(gen_file, 'r') as f: mailmsg = f.read()
sendmail(mailmsg)
