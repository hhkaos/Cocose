# coding=utf-8

from oauth2 import Client, Token, Consumer
import urllib
from xml.dom.minidom import parseString,NodeList

__author__= 'Javier Cordero Martinez'
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Javier Cordero Martinez"
__email__ = "jcorderomartinez@gmail.com"
__status__ = "Development"

"""
    TODO: 
        better handling of requests.
        use ElementTree instead of minidom for XML.
        Use facets for location
"""    



consumer_key    =   'gg7fgmfpa1qe'
consumer_secret =   'oYlW0YBGfiS6srXk'

oauth_token        = '42552eb6-5765-4327-851a-a328e77c3a4a'
oauth_token_secret = '055784a0-8bf8-40f9-a70b-ec75b4acadda'
     
# the URLs we will use
request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
access_token_url =  'https://api.linkedin.com/uas/oauth/accessToken'
authorize_url =     'https://api.linkedin.com/uas/oauth/authorize'


linkedin_search_url = 'http://api.linkedin.com/v1/people-search'
linkedin_people_url = 'http://api.linkedin.com/v1/people'

consumer = Consumer(
                        key=consumer_key,
                        secret=consumer_secret
                         )
token = Token(
                key=oauth_token, 
                secret=oauth_token_secret,
                )
linkedin_client = Client(consumer = consumer, 
                     token = token,
                     )

def do_search(keywords=None, company=None):
    """
        Do a people-search, with keywords and/or company name.
        Currently, only search people in Spain
        
        Gets: id, first-name, last-name, public-profile-url, location, three-current-positions, primary-twitter-account
    """
    url = '%s:(people:(id,first-name,last-name,public-profile-url,location,three-current-positions,primary-twitter-account),facets:(code),num-results)?count=25&facet=location,es:0' % (linkedin_search_url)
    if keywords:
        encoded_keywords = urllib.quote(keywords)
        url += '&keywords=%s' % encoded_keywords
    if company:
        encoded_company = urllib.quote(company)
        url += '&company-name=%s' % encoded_company
        
    response = linkedin_client.request(url)
    if response[0]['status'] != '200':
        return response

    xml = parseString(response[1])
    total = int(xml.getElementsByTagName('people')[0].getAttribute('total'))
    count = int(xml.getElementsByTagName('people')[0].getAttribute('count')) if xml.getElementsByTagName('people')[0].getAttribute('count') else total
    people = xml.getElementsByTagName('person')
    while count<total:
        response = linkedin_client.request('%s:(people:(id,first-name,last-name,location),facets:(code),num-results)?keywords=%s&start=%s&count=25&facet=location,es:0' % (linkedin_search_url,encoded_keywords,count))
        if response[0]['status'] != '200':
            raise Exception("Error conectando con linkedin")
        xml2 = parseString(response[1])
        try:
            count += int(xml2.getElementsByTagName('people')[0].getAttribute('count'))
        except: # list is empty
            break
        people.extend(xml2.getElementsByTagName('person'))
    return total, people

def do_search_profile(people):
    result = NodeList()
    for id in _id_generator(people):
        response = linkedin_client.request('%(url)s/id=%(id)s:(id,public-profile-url,formatted-name,location,three-current-positions,primary-twitter-account)' % {'url': linkedin_people_url,
                                                                                   'id': id
                                                                                   }
                                       )
        if response[0]['status'] == '403':
            continue
        elif response[0]['status'] != '200':
            return response
        xml = parseString(response[1])
        result.append(xml.getElementsByTagName('person'))
    return result
    
    
def _id_generator(people):
    for p in people:
        id = [n.data for n in p.getElementsByTagName('id')[0].childNodes if n.nodeType == n.TEXT_NODE][0]
        if id != 'private':
            yield id
                        
def _profile_generator(people):
    for p in people:
        url = [n.data for n in p.getElementsByTagName('public-profile-url')[0].childNodes if n.nodeType == n.TEXT_NODE][0]
        yield url
