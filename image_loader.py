import requests
import base64
import json
import os
import logging

from simple_salesforce import Salesforce

# verbose logging.....
logging.basicConfig(level=logging.DEBUG)

# config your environment
imageDir = os.environ['IMAGE_DIR']
password = os.environ['SF_PASS']
securityToken = os.environ['SF_SECURITY_TOKEN']
username = os.environ['SF_USER']

logging.debug('We are about to login to Salesforce')

# authorise to your Salesforce org... add 'domain=test' as fourth param if using SBox
sf = Salesforce(username=username, password=password, security_token=securityToken)

# get the list of objects you want to attach images to..
animals = sf.query_all('select id, name, l_id__c from animal__c')

# this is the file we are giong to upload
img = 'file.png'

# open it as a binary file
with open (os.path.join(imageDir,img), 'rb') as f:

   # and read it to a base64 encoded string (python3)
   encoded_string = base64.b64encode(f.read()).decode(encoding='utf-8', errors='string')

   # creating a file is three things in Salesforce
   # 1. Create the ContentVersion

   r = requests.post('https://%s/services/data/v43.0/sobjects/ContentVersion/' % sf.sf_instance,
      headers = {'Content-Type':'application/json','Accept-Encoding': 'gzip', 'Authorization': 'Bearer %s' % sf.session_id},
      json = {
         'Title':img,
         'PathOnClient':img,
         'VersionData':encoded_string,
      }
   )

   if(r.status_code < 300):

      # 2. Get the ContentDcoumentId
      content_version_id = r.json().get('id')
      r = requests.get('https://%s/services/data/v43.0/sobjects/ContentVersion/%s' % (sf.sf_instance, content_version_id),
         headers = {'Content-Type':'application/json','Accept-Encoding': 'gzip', 'Authorization': 'Bearer %s' % sf.session_id})

      if r.status_code < 300:
         content_document_id = r.json().get('ContentDocumentId')

         # 3. Create a ContentDocumentLink
         r = requests.post('https://%s/services/data/v43.0/sobjects/ContentDocumentLink' % sf.sf_instance,
            headers = {'Content-Type':'application/json','Accept-Encoding': 'gzip', 'Authorization': 'Bearer %s' % sf.session_id},
            json = {
               'ContentDocumentId' : content_document_id,
               'LinkedEntityId' : animals["records"][0]["Id"],
               'ShareType' : 'V'
            }
         )
         if r.status_code < 300:
            logging.info('Have uploaded img %s', img)
         else:
            logging.error('Unable to create ContentDocumentLink!')
            logging.error(r.text)
      else :
         logging.error('Unable to retrieve our previously loaded content version? [%s]' % content_version_id)
         logging.error(r.text)
   else:
      logging.error('Unable to load ContentVersion?')
      logging.error(r.text)








