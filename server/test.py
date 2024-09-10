from pocketbase import PocketBase
from pocketbase.client import FileUpload

client = PocketBase('http://127.0.0.1:8090')

def main():
    pb = PocketBase('http://127.0.0.1:8090')
    admin_data = pb.admins.auth_with_password('antkjc@gmail.com', 'adminpassword')
    print(admin_data.is_valid)

    result = pb.create_collection("example")
    result = pb.collection("example").create(
    {
        "status": "true",
        "image": FileUpload(("image.png", open("temp.jpg", "rb"))),
    })

if __name__ == "__main__":
    main()