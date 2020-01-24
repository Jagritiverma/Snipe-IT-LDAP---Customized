# configuration file

# ldap server
server = 'ldap://server-name'
# creds to login into ldap server for authentication
username = 'usernmae'
password = 'password'
# name of the user to perform the operation
name = 'user'
# api key and port
headers = {'authorization': 'Bearer API-key ',
           'content-type': "application/json"}
port = 3268
# common url for snipe it api
url = 'https://website/snipe-it/api/v1/'
# url for various operations on user
url_user = 'https://website/snipe-it/api/v1/users/'
# url for various operations on location
url_loc = 'https://website/snipe-it/api/v1/locations/'
# all the users from the below groups. If needed, groups can be modified (add or delete)
SearchGroup = [] #Distributed-List
# variables from LDAP
list_LDAP_var = ['mail', 'telephoneNumber', 'title', 'info', 'l', 'st', 'postalCode', 'streetAddress','givenName','name','sn']
list_LDAP_var1 = ['mail', 'telephoneNumber', 'title', 'info', 'l', 'st', 'postalCode', 'streetAddress','givenName','sAMAccountName','sn']
# variables from SNIPE IT
list_SNIPE_var = ['email', 'phone', 'jobtitle', 'notes', 'city', 'state', 'zip', 'address','first_name','username','last_name','ldap_import']

