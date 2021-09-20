import requests
from requests.auth import HTTPBasicAuth
import base64
import xml.etree.ElementTree as et


f = open("dzaiib1.txt","w+")
ex_groups = []
    
def print_mf_properties(ex_group, app , message_flow  , text):
    #print(text.content)
    msg_root = et.fromstring(text.content)
    print(ex_group)
    #print('\t' + app )
    print('\t\t' + message_flow  )
    for elem in msg_root.findall('{*}deployedProperties/{*}property'):
        print('\t\t\t'+elem.get('name') + ' ' + elem.get('value')  )
    for elem in msg_root.findall('{*}userDefinedProperties/{*}property'):
        print('\t\t\t'+elem.get('name') + ' ' + elem.get('value')  )        
   
        
def print_app_properties(ex_group, app , message_flow  , text):
    #print(text)
    msg_root = et.fromstring(text.content)
    print(ex_group)
    print('\t' + app )
    #print('\t\t' + message_flow )
    for elem in msg_root.findall('{*}deployedProperties/{*}property'):
        print('\t\t\t' + elem.get('name') + ' ' + elem.get('value')  )
    for elem in msg_root.findall('{*}userDefinedProperties/{*}property'):
        print('\t\t\t'+elem.get('name') + ' ' + elem.get('value')  ) 
    print(uri +'/executiongroups/' + ex_group + '/applications/' +app+'/messageflows')
    xml_app_mf = iib_call(uri +'/executiongroups/' + ex_group + '/applications/' +app+'/messageflows'  , False)
    root_app = et.fromstring(xml_app_mf.content)
    for elem_mf in root_app.findall('{*}messageFlow'):
        xml_app_mf_per = iib_call(elem_mf.get('propertiesUri')  , False)
        root_app_per = et.fromstring(xml_app_mf_per.content)
        print('\t\t' + app + ' {MessageFlowList}')
        print('\t\t' + elem_mf.get('name'))
        for elem1 in root_app_per.findall('{*}deployedProperties/{*}property'):
            print('\t\t\t' + elem1.get('name') + ' ' + elem1.get('value')  )
        for elem1 in msg_root.findall('{*}userDefinedProperties/{*}property'):
            print('\t\t\t'+elem1.get('name') + ' ' + elem1.get('value')  ) 
       
    

def iib_call(iib_uri,print_txt):
    # make call and return the text 
    resp = requests.get(base + iib_uri ,auth=HTTPBasicAuth(user, passw0rd))
    if resp.status_code != 200:
    # This means something went wrong.
        print('HttpError status code ' + str(resp.status_code)) 
        print('HttpError text ' + resp.text) 
        print(iib_uri)
    if print_txt:
        print(resp.content)
    return resp


def rest_tree_iib ():
    #get list of iib integration servers
    xml = iib_call(uri + '/executiongroups', False)
    root = et.fromstring(xml.content)
    for elem in root.findall('{*}executionGroup'):
        ex_groups.append(elem.get('name'))
        
    for g in ex_groups:
        # get apps per ex group
        app_uri = uri +'/executiongroups/' + g + '/applications'     
        xml_app = iib_call(app_uri , False)        
        root_app = et.fromstring(xml_app.content)
        #print( g )
        for elem in root_app.findall('{*}application'):
            #print('\t\t' + elem.get('name') )
            app_uri_prop = uri +'/executiongroups/' + g + '/applications'     
            xml_app = iib_call(elem.get('propertiesUri') , False)
            print_app_properties(g , elem.get('name') , '' , xml_app )
        
        xml_app_mf = iib_call( uri +'/executiongroups/' + g +  '/messageflows'  , False)
        root_app = et.fromstring(xml_app_mf.content)
        for elem_mf in root_app.findall('{*}messageFlow'):
            xml_app_mf_per = iib_call(elem_mf.get('propertiesUri')  , False)
            root_app_per = et.fromstring(xml_app_mf_per.content)
            print_mf_properties(g , '' , elem_mf.get('name') , xml_app_mf_per )
          
        
                      
user = 'admin'
passw0rd = 'password'
base = 'http://dev.iib.com:4414'
uri = '/apiv1'

rest_tree_iib()
f.close()
