import json
import os
import hashlib

class Auth:
    _DATA_FILE = "users.json"
    '''
    @classmethod
    def _ensure_data_dir(cls):
        if not os.path.exists(cls._DATA_FILE):
            os.makedirs(cls._DATA_FILE, exist_ok=True)
    '''

    @classmethod
    def _load_users(cls) -> dict:
        #cls._ensure_data_dir()
        """从本地文件加载用户数据"""
        if not os.path.exists(cls._DATA_FILE):
            return {}
        with open(cls._DATA_FILE, 'r') as f:
            return json.load(f)

    @classmethod
    def _save_users(cls, users: dict):
        #cls._ensure_data_dir()
        """保存用户数据到本地文件"""
        with open(cls._DATA_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    # 登入
    '''
    InputData{
        username: UserName,
        password: UserPassword,
    }
    '''
    @classmethod
    def login(cls,InputData):
        users = cls._load_users()
        # := 若为真则赋值，为假则返回False
        if user := users.get(InputData['username']):
            input_hash = hashlib.sha256(InputData['password'].encode()).hexdigest()
            if user['password_hash'] == input_hash:
                return 'True'
        return 'False'
    
    @classmethod
    def SignUp(cls,InputData):
        users = cls._load_users()
        if InputData['username'] in users:
            return 'False'
            
        users[InputData['username']] = {
            "password_hash": hashlib.sha256(InputData['password'].encode()).hexdigest()
        }
        cls._save_users(users)
        return 'True'