# coding=utf-8

from oauth2 import Client, Token, Consumer
import urllib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

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
        #keywords = company.decode('utf8','ignore')
        encoded_keywords = urllib.quote(keywords.encode("ascii","replace"))
        url += '&keywords=%s' % encoded_keywords
    if company:
        #company = company.decode('utf8','ignore')
        encoded_company = urllib.quote(company.encode("ascii","replace"))
        url += '&company-name=%s' % encoded_company
        
    response = linkedin_client.request(url)
    if response[0]['status'] != '200':
        raise Exception("Error conectando con linkedin")
    xml = ET.fromstring(response[1])
    total = int(xml.find('people').attrib['total'])
    count = int(xml.find('people').attrib['count']) if xml.find('people').attrib.get('count') else total
    people = xml.findall('people/person')
    while count<total:
        url2 = url + '&start=%s' % count
        response = linkedin_client.request(url2)
        if response[0]['status'] != '200':
            raise Exception("Error conectando con linkedin")
        xml = ET.fromstring(response[1])
        try:
            count += int(xml.find('people').attrib['count']) if xml.find('people').attrib.get('count') else total
        except: # list is empty
            break
        people.extend(xml.findall('people/person'))
    return total, people


def do_search_profile(people):
    result = []
    for id in _id_generator(people):
        response = linkedin_client.request('%(url)s/id=%(id)s:(id,public-profile-url,formatted-name,location,three-current-positions,primary-twitter-account)' % {'url': linkedin_people_url,
                                                                                   'id': id
                                                                                   }
                                       )
        if response[0]['status'] == '403':
            continue
        elif response[0]['status'] != '200':
            return response
        result.append(ET.fromstring(response[1]))
    return result
    
    
def _id_generator(people):
    for p in people:
        id = p.find('id').text
        if id != 'private':
            yield id
                      
def _profile_url_generator(people):
    for p in people:
        #url = p.find('public-profile-url').text
        if p.find('public-profile-url') is not None:
            yield p.find('public-profile-url').text

def _profile_generator(people):
    # id,first-name,last-name,public-profile-url,location,three-current-positions,primary-twitter-account
    for p in people:
        d = {
             'id': p.find('id').text,
             'first-name': p.find('first-name').text,
             'last-name': p.find('last-name').text,
             'public-profile-url': p.find('public-profile-url').text if p.find('public-profile-url') is not None else None,
             'location': {'name': p.find('location/name').text if p.find('location/name') is not None else None,
                          'country': p.find('location/country').text if p.find('location/country') is not None else None,
                          'code': p.find('location/country/code').text if p.find('location/country/code') is not None else None, 
                          },
             'three-current-positions': {
                                         'total': p.find('three-current-positions').attrib['total'] if p.find('three-current-positions') is not None else 0,
                                         'positions': [],
                                         }
             }
        positions = p.findall('three-current-positions/position')
        for position in positions:
            d['three-current-positions']['positions'].append(
                                                             {'id': position.find('id').text if position.find('id') is not None else '',
                                                              'title': position.find('title').text if position.find('title') is not None else '',
                                                              'summary': position.find('summary').text if position.find('summary') is not None else '',
                                                              'size': position.find('company/size').text if position.find('company/size') is not None else '',
                                                              'company': position.find('company/name').text if position.find('company') is not None else '',
                                                              }
                                                             )
            
        yield d
