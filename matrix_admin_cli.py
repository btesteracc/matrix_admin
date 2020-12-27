#!/usr/bin/env python3
import argparse
from matrix_server import Matrix_server
import json
import os,sys
import getpass
import re

parser = argparse.ArgumentParser(prog="matrix_admin_cli.py", description="A simple Matrix-Server admin tool")

parser.add_argument('-l','--login',help="Login manually",action="store_true")

# sub_parser=parser.add_subparsers(help='Sub command login_config')
# login_parser = sub_parser.add_parser("--login_config", help="Login config on commandline")
# login_parser.add_argument('-H','--host',help='hostname')
# login_parser.add_argument('-u','--user',help='username of the server admin')
# login_parser.add_argument('-p','--password',help='password for the admin user - DO USE WITH CAUTION!')

#parser.add_argument('cmd',choices=['lu','lr', 'cp', 'au'])

parser.add_argument('-au','--add_user',help='create new user - asks for username and password',action="store_true")
parser.add_argument('-du','--delete_user',help='delete user with given userid (@user:servername)')
parser.add_argument('-dr','--delete_room',help='delete rom with given roomid')
parser.add_argument('-cp','--change_password',help='change password for given userid')
parser.add_argument('-c','--config_file',help='load config from file',type=argparse.FileType('r'))
parser.add_argument('-lu','--list_users',help='list users from server')
parser.add_argument('-lr','--list_rooms',help='list rooms from server',action="store_true")
parser.add_argument('-q','--quiet', help='No comments, just JSON Output',action="store_true")
args = parser.parse_args()
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
server = Matrix_server()

if args.login:
    server_name=input('Servername: ')
    username=input('Username: ')
    password=getpass.getpass('Password: ')
    filename=""
    while ( saveconfig:=input("Do you want to save the configuration? (Enter y/n)").lower() ) not in {"y", "n"}: pass
    if saveconfig=='y':
        filename=input("Configuration Filename (optional): ")
    if server.login(server_name,username,password,saveconfig,filename)==None:
        print("Error on login. Exiting:")
        sys.exit(1)

elif args.config_file:
    data= server.load_config(file=args.config_file) 
    if data and not args.quiet:
        print('Config loaded from {}'.format(args.config_file.name))
else:
    print('No configuration given. Exiting')
    sys.exit(1)


if args.list_users:
    print(json.dumps(server.get_users(), indent=True, sort_keys=True))

elif args.list_rooms:
    print(json.dumps(server.get_rooms(), indent=True, sort_keys=True))


elif args.change_password:
    pw = getpass.getpass()
    tries=0
    while tries<3:
        tries+=1
        pw_confirm= getpass.getpass("Repeat Password: ")
        if pw == pw_confirm:
            break
    else:
        print('Passwords do not match, exiting')
        sys.exit(1)

    data = server.reset_password(args.change_password, pw)
    print('Password changed')
    print(data)
    print("\n")


elif args.delete_user:
    is_argument_a_matrix_id = re.match('@([a-zA-Z0-9_\-\.]+):(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$',args.delete_user)
    if is_argument_a_matrix_id !=None:
        data=server.deactivate_user(args.delete_user)
        if data['id_server_unbind_result']=='success':
            print(f'User {args.delete_user} deactivated')
        else:
            print('Error deactivating user')
    else:
        print('Not a valid matrix-id')
        sys.exit(1)

elif args.add_user:
    username=input("Username: ")
    pw = getpass.getpass()
    tries=0
    while tries<3:
        tries+=1
        pw_confirm= getpass.getpass("Repeat Password: ")
        if pw == pw_confirm:
            break
    else:
        print('Passwords do not match, exiting')
        exit()
    user_id = '@'+username+':'+server.server_name
    user_data={'user_id':user_id,'password': pw,'displayname':username}
    data=server.new_user(user_data)
    if data:
        print(f'User created')
        if not args.quiet:
            print(json.dumps(data, indent=True,sort_keys=True))
    else:
        print('User creation failed')



    



