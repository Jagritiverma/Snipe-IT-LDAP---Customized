#!/usr/bin/python2.7
import requests
import json
from ldap3 import Server, \
    AUTO_BIND_NO_TLS, \
    Connection, \
    SUBTREE, \
    ALL_ATTRIBUTES, \
    NTLM
import urllib3
import config
import re
import time
import random
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# stops warning for disabling ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global vars and the LDAP connection
# Global vars
BindUser = config.username
BindPassword = config.password
ADServer = config.server
SearchGroup = config.SearchGroup
SearchBase = 'DC=xxx,DC=yy,DC=z,DC=edu'
res = []
dic = {}

# LDAP connection
server = Server(ADServer)
conn = Connection(server, user=BindUser, password=BindPassword, authentication=NTLM, auto_bind=True)
conn.bind()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# function - user info (LDAP)
def get_ldap_info(u):
    conn.search(search_base='DC=yy,DC=z,DC=edu',
                search_filter='(&(samAccountName=' + u + '))',
                search_scope=SUBTREE,
                attributes=ALL_ATTRIBUTES,
                get_operational_attributes=True)
    return conn.entries


def get_ldap_info1(u):
    with Connection(Server(config.server, port=config.port, use_ssl=False),
                    auto_bind=AUTO_BIND_NO_TLS,
                    read_only=True,
                    check_names=True,
                    user=config.username, password=config.password) as c1:
        c1.search(search_base='DC=xxx,DC=yy,DC=z,DC=edu',
                    search_filter='(&(samAccountName=' + u + '))',
                    search_scope=SUBTREE,
                    attributes=ALL_ATTRIBUTES,
                    get_operational_attributes=True)
    return c1.response

def get_ldap_info2(u):
    with Connection(Server(config.server, port=config.port, use_ssl=False),
                    auto_bind=AUTO_BIND_NO_TLS,
                    read_only=True,
                    check_names=True,
                    user=config.username, password=config.password) as c1:
        c1.search(search_base='DC=xxx,DC=yy,DC=z,DC=edu',
                    search_filter='(&(samAccountName=' + u + '))',
                    search_scope=SUBTREE,
                    attributes=ALL_ATTRIBUTES,
                    get_operational_attributes=True)
    return c1.response
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Extract all the members of the group
def get_user_from_group1(group):
    conn.search(search_base="DC=xxx,DC=yy,DC=z,DC=edu",
                search_filter='(&(objectClass=group)(CN='+group+'))', search_scope=SUBTREE,
                attributes=['member'])
    result = conn.entries
    return result

# Get a final list where all the users from three groups: AllFaculty, AllStaff and Stu. (GET-USER funtionality)
regex_short = r" +CN=([a-zA-Z0-9]+)"  # extracts username only
# regex_long = r" +(?:[O|C|D][U|N|C]=[a-zA-Z ]+,?)+"  # extracts complete DN
l1 = []
for i in SearchGroup:
    match = re.findall(regex_short, str(get_user_from_group1(group=i)))
    l1.extend(match)
res2 = []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#print("hi")
#l1 = ['jlvalle']
for p in range(len(l1)):
    name = l1[p]
   # print("name", name, p)
    if name == "DL":
        continue
    res = get_ldap_info(name)
    res1 = get_ldap_info1(name)
    res2 = get_ldap_info2(name)
    # print(res2)
    # print(res1)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if not res and not res1 and not res2:
        continue
    else:
        for i in range(len(config.list_LDAP_var)):
            try:
                y = str(res1[0]["attributes"][config.list_LDAP_var[i]]).splitlines()
                dic[config.list_SNIPE_var[i]] = ','.join(y)
            except IndexError as e:
                try:
                    y = str(res[0][config.list_LDAP_var[i]]).splitlines()
                    dic[config.list_SNIPE_var[i]] = ','.join(y)
                except KeyError as e:
                    dic[config.list_SNIPE_var[i]] = ""
                except IndexError as e:
                    dic[config.list_SNIPE_var[i]] = ""
            except KeyError as e1:
                try:
                    y = str(res[0][config.list_LDAP_var[i]]).splitlines()
                    dic[config.list_SNIPE_var[i]] = ','.join(y)
                except KeyError as e:
                    dic[config.list_SNIPE_var[i]] = ""
                except IndexError as e:
                    dic[config.list_SNIPE_var[i]] = ""
    p = 0
    for i in range(len(config.list_LDAP_var)):
        if dic[config.list_SNIPE_var[i]]:
            p = 1
        else:
            pass
    if p == 0:
        for i in range(len(config.list_LDAP_var1)):
            if dic[config.list_SNIPE_var[i]]:
                break
            else:
                try:
                    y = str(res2[0]["attributes"][config.list_LDAP_var1[i]]).splitlines()
                    dic[config.list_SNIPE_var[i]] = ','.join(y)
                except KeyError as e:
                    dic[config.list_SNIPE_var[i]] = ""
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   # print(dic)
    headers = config.headers
    url = config.url + 'users?search='+name+''
    querystring = {"limit": "50", "offset": "3"}
    response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
    if response.status_code != 200:
        pass
    else:
        result = json.loads(response.text)
        if not result["rows"]:
            # print(name)
            s = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            pwd = ''.join(random.sample(s, len(s)))
            payload1 = "{\"first_name\" :\"" + dic["first_name"] + "\",\"last_name\" :\"" + dic["last_name"] + "\", \"username\" :\"" + dic["username"] + "\",\"password\" :\"" + pwd + "\" ,\"password_confirmation\" :\"" + pwd + "\",\"activated\" :true,\"phone\" :\"" + dic['phone']+"\", \"jobtitle\" :\"" + dic['jobtitle']+"\",\"email\" :\"" + dic['email']+"\" ,\"notes\" :\"" + dic['notes']+"\", \"ldap_import\" :1}"
            #print("payload",payload1)
            url = 'https://website-name/snipe-it/api/v1/users'
            headers = {
                'authorization': 'Bearer API-key ',
                'content-type': 'application/json'}
            payload = payload1
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            # print(response)
        else:
            identity = str(result["rows"][0]["id"])
            url = config.url_user + identity
            payload = "{\"phone\" :\"" + dic['phone']+"\", \"jobtitle\" :\"" + dic['jobtitle']+"\",\"email\" :\"" + dic['email']+"\" ,\"notes\" :\"" + dic['notes']+"\", \"ldap_import\" :1}"
            response = requests.request("PATCH", url,  headers=headers, data=payload, verify=False)
            time.sleep(2)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
