import requests
import urllib.parse
import json

class Matrix_server():
    def __init__(self,server_name =""):
        self.server_name = server_name
        self.header=""

    def load_config(self,filename = ""):
        if filename == "":
            filename=self.server_name+'.json'
        try:
            file = open(filename)
            self.auth_user = json.load(file)
            self.set_access_token(self.auth_user['access_token'])
            self.server_name=self.auth_user['home_server']
            self.server_url='https://'+self.server_name
            file.close()
            return True
        except:
            return None

    def save_config(self,filename = ""):
        if filename == "":
            filename=self.server_name+".json"
        with open(filename,'w') as file:
            json.dump(self.auth_user,fp=file)
            

    def login(self,username,password, saveconfig=False,filename = ""):
        self.username=username
        adress= self.server_url+"/_matrix/client/r0/login"
        data = json.dumps({"user" : username, "password" : password, "type":"m.login.password"})
        try: 
            r = requests.post(adress, data)
            if r.status_code==200:
                self.auth_user = r.json()
                self.set_access_token(self.auth_user['access_token'])
                if saveconfig:
                    self.save_config(filename)
                return r.status_code
        except:
            return None

    def set_access_token(self, access_token):
        self.access_token = access_token
        self.header = {"Authorization":"Bearer " + self.access_token}
            
    def get_room_id_from_alias(self, room_alias):
        url=self.server_url+f"/_synapse/client/r0/directory/room/{urllib.parse.quote(room_alias)}"
        res = requests.get(url,headers = self.header)
        if res.status_code==200:
                return res.json()['room_id']
        else:
            return None

    def get_users_from_room(self, room_id):
        url=self.server_url+f"/_snyapse/client/r0/rooms/{urllib.parse.quote(room_id)}/joined_members"
        res = requests.get(url,headers=self.header)
        if res.status_code==200:
                return res.json()
        else:
            return None

    def get_rooms(self):
        url=self.server_url+"/_synapse/admin/v1/rooms"
        res = requests.get(url,headers=self.header)
        if res.status_code==200:
                return res.json()['rooms']
        else:
            return None

    def get_users(self):
        url=self.server_url+"/_synapse/admin/v2/users"
        res = requests.get(url,headers=self.header)
        if res.status_code==200:
            return res.json()['users']
        else:
            return None

    def delete_room(self, room_id):
        url=self.server_url+f"/_synapse/admin/v1/rooms/{room_id}/delete"
        res = requests.post(url,headers=self.header)
        if res.status_code==200:
              return res.json()
        else:
            return None

    def new_user(self, user_data):
        url=self.server_url+f"/_synapse/admin/v2/users/{urllib.parse.quote(user_data['user_id'])}"
        data = json.dumps({"password" : user_data['password'], "displayname" : user_data['displayname']})
        res = requests.put(url, data = data, headers=self.header)
        if res.status_code==200:
            return res.json()
        return None
    
    def deactivate_user(self, user_id):
        url=self.server_url+f"/_synapse/admin/v1/deactivate/{urllib.parse.quote(user_id)}"
        data = json.dumps({"erase": True})
        res = requests.post(url, data, headers=self.header)
        if res.status_code==200:
            return res.json()
        return None        

    def get_user(self, user_id):
        url=self.server_url+f"/_synapse/admin/v2/users/{urllib.parse.quote(user_id)}"
        res = requests.get(url, headers=self.header)
        if res.status_code==200:
            return res.json()
        else:
            return None

    def reset_password(self,user_id,password, logout_devices = True):
        url=self.server_url+f"/_synapse/admin/v1/reset_password/{urllib.parse.quote(user_id)}"
        data = json.dumps({"new_password":password, "logout_devices":logout_devices})
        res = requests.post(url, data, headers=self.header)
        if res.status_code==200:
            return res.json()
        else:
            return None

    def get_joined_rooms(self, user_id):
        url=self.server_url+f"/_synapse/admin/v1/users/{urllib.parse.quote(user_id)}/joined_rooms"
        res = requests.get(url, headers=self.header)
        if res.status_code==200:
            return res.json()
        else:
            return None

    def get_user_devices(self,user_id):
        url=self.server_url+f"/_synapse/admin/v2/users/{urllib.parse.quote(user_id)}/devices"
        res = requests.get(url, headers=self.header)
        if res.status_code==200:
            return res.json()
        else:
            return None


if __name__ == "__main__":
    print("This is a module, please import to your program and do not execute")







