from pocketbase import PocketBase
from pocketbase.client import FileUpload

class Test():
    def __init__(self):
        self.pb = PocketBase('http://127.0.0.1:8090')
        admin_data = self.pb.admins.auth_with_password('antkjc@gmail.com', 'adminpassword')
        print(admin_data.is_valid)

        result = self.pb.collection("clothes").create(
        {
            "title": "Test Title",
        })
                             

if __name__ == "__main__":
    Test = Test()