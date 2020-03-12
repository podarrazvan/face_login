import face_recognition
import cv2
from PIL import Image
import os
from pymongo import MongoClient
import os.path

mongo = MongoClient('mongodb://localhost:27017')
db = mongo["FaceLogin"]


stop = False


def face_check():
    a = 0
    video = cv2.VideoCapture(0)
    while True:
        a = a + 1
        check, frame = video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Capturing", gray)

        try:
            image = face_recognition.load_image_file(f'./users/{username}/{username}.jpg')

            image_encoding = face_recognition.face_encodings(image)[0]
        except:
            print("Who are you?!")
        pil_im = Image.fromarray(frame)
        pil_im.save("./login/img.jpg")

        unknown_image = face_recognition.load_image_file('./login/img.jpg')
        try:
            unknown_image_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces([image_encoding], unknown_image_encoding)
            if results[0]:
                print(f"Hello, {username} !")
                os.remove('./login/img.jpg')
                break
        except:
            print("No face")

    # cv2.waitKey(0)

    video.release()
    cv2.destroyAllWindows()

def new_face():
    global stop
    video = cv2.VideoCapture(0)
    while stop == False:

        check, frame = video.read()


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Capturing", gray)

        pil_im = Image.fromarray(frame)

        pil_im.save(f"./users/{username}/{username}.jpg")


        image = face_recognition.load_image_file(f'./users/{username}/{username}.jpg')
        face_loocations = face_recognition.face_locations(image)
        # this should save only the face but not working for a moment ...
        for face_location in face_loocations:
            top = face_loocations[0][0]
            right = face_loocations[0][1]
            bottom = face_loocations[0][2]
            left = face_loocations[0][3]

            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.save(f'{username}.jpg')
            print(f"Wellcome, {username}!")
            stop = True



    video.release()
    cv2.destroyAllWindows()


def new_or_old():
    new_or_not = ["Y", "N"]
    status = input("Are you a registred user? (Y/N)\n")
    status = status.upper()
    if status == "Y":
        old_user()
    elif status == "N":
        new_user()

    else:
        while status not in new_or_not:
            print("Please insert ONLY ""Y"" or ""N""! \n")
            new_or_old()

def old_user():
    global username
    username = input("Enter your username :D \n")

    check = {
        "username" : "{}".format(username)
    }
    found = db.users.find_one(check)
    if str(found) != "None":
        face_check()
    else:
        print("Wrong username! \n")
        new_user()
def new_user():
    global username
    username = input("Please create an username \n")

    add = {
        "username": "{}".format(username)
    }
    check = db.users.find_one(add)
    if str(check) == "None":
        db.users.insert_one(add)
        while os.makedirs(f"./users/{username}") is False:
            pass
        new_face()
    else:
        face_check()

new_or_old()