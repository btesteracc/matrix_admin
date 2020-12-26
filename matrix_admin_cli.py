import argparse
from matrix_server import Matrix_server
import json
import os,sys
import getpass

parser = argparse.ArgumentParser(prog="matrix_admin_cli.py", description="A simple Matrix-Server admin tool")

# parse.add_argument('--server',help='name of the server')
# parse.add_argument('--admin',help='username of the server admin')
# parse.add_argument('--password',help='password for the admin user - DO USE WITH CAUTION!')
parser.add_argument('-au','--add_user',help='create new user - asks for username and password',action="store_true")
parser.add_argument('-du','--delete_user',help='delete user with given userid')
parser.add_argument('-dr','--delete_room',help='delete rom with given roomid')
parser.add_argument('-cp','--change_password',help='change password for given userid')
parser.add_argument('-c','--config_file',help='load config from file')
parser.add_argument('-lu','--list_users',help='list users from server', action="store_true")
parser.add_argument('-lr','--list_rooms',help='list rooms from server',action="store_true")
args = parser.parse_args()
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
server = Matrix_server()
if args.config_file:
    print('Loading config....')
    server.load_config(args.config_file)
    print('Config loaded from {}'.format(args.config_file))
else:
    print('No configuration given. Exiting')
    exit()
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
        exit()

    data = server.reset_password(args.change_password, pw)
    print('Password changed')
    print(data)
    print("\n")
    exit()

elif args.delete_user:
    data=server.deactivate_user(args.delete_user)
    print('User deactivated')
    print(data)

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
        print('User created')
    else:
        print('User creation failed')
    print(json.dump(data, indent=True,sort_keys=True))



    



