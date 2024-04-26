import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import face_recognition
import numpy as np
import mysql.connector as sqltor



def main_window():
    myconn = sqltor.connect(host="localhost", user="root", passwd="", database="face_recognition")
    cursor = myconn.cursor()

    register_window = tk.Tk()
    register_window.title("Registeration Page")
    register_window.geometry("500x500")


    register_name_label = ttk.Label(register_window, text="Enter your Name :", font=("Denmark", 15)).grid(row=1, column=0, sticky=tk.W,pady=15)
    register_name_user = tk.StringVar()
    register_name = ttk.Entry(register_window, textvariable=register_name_user, width=15, font=("Denmark", 15)).grid(row=1, column=1,sticky=tk.W,pady=15)

    register_username_label = ttk.Label(register_window, text="Enter your Username :", font=("Denmark", 15)).grid(row=2,column=0,sticky=tk.W,pady=15)
    register_username_user = tk.StringVar()
    register_username = ttk.Entry(register_window, textvariable=register_username_user, width=15,font=("Denmark", 15)).grid(row=2, column=1, sticky=tk.W, pady=15)

    register_email_label = ttk.Label(register_window, text="Enter your Email :", font=("Denmark", 15)).grid(row=3,column=0,sticky=tk.W,pady=15)
    register_email_user = tk.StringVar()
    register_email = ttk.Entry(register_window, textvariable=register_email_user, width=15,font=("Denmark", 15)).grid(row=3, column=1, sticky=tk.W, pady=15)

    def register_user():

        if( register_name_user.get().strip() == "" or register_username_user.get().strip() == "" or register_email_user.get().strip() == ""):
            messagebox.showerror("Error", "Field Can't be Empty.....")

        else:

            # search_data =


            register_name_user_data = register_name_user.get().strip()
            register_username_user_data = register_username_user.get().strip()
            register_email_user_data = register_email_user.get().strip()

            print(register_name_user_data)
            print(register_username_user_data)
            print(register_email_user_data)


            def open_camera_reg():
                cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                cv2.namedWindow("Image Capture Window")
                while True:
                    ret, frame = cam.read()
                    if not ret:
                        print("Fail to grab Frame")
                    frame = cv2.flip(frame, 1)
                    cv2.imshow("Image Capture", frame)

                    k = cv2.waitKey(1)
                    if k % 256 == 27:
                        # ESC pressed
                        print("Closing Image Capture Window")
                        break
                    if k % 256 == 32:
                        # SPACE pressed
                        img_name = "{}.jpg".format(register_username_user_data)
                        cv2.imwrite(img_name, frame)
                        print("{}".format(img_name))

                        inputs_reg = (register_name_user_data, register_username_user_data, register_email_user_data, img_name)

                        insert_data_query_reg = ("INSERT INTO `user_record`(`Name`, `Username`, `Email`, `Image`) VALUES (%s,%s,%s,%s)")

                        cursor.execute(insert_data_query_reg, (inputs_reg))

                        messagebox.showinfo("Info", "Registration Successful")

                        register_name_user.set("")
                        register_username_user.set("")
                        register_email_user.set("")

                        myconn.commit()

                cam.release()
                cv2.destroyAllWindows()

            open_camera_reg_button = tk.Button(register_window, width=25, height=2, text="Open Camera", fg="blue",command=open_camera_reg)
            open_camera_reg_button.grid(row=6, column=1, sticky=tk.W, pady=10)




    register_button = tk.Button(register_window, width=25, height=2, text="Click here to Register", fg="blue", command=register_user)
    register_button.grid(row=4, column=1, sticky=tk.W, pady=10)




    def goto_login_page():
        register_window.destroy()
        login_window = tk.Tk()
        login_window.title("Login Page")
        login_window.geometry("500x500")

        login_username_label = ttk.Label(login_window, text="Enter your Username :", font=("Denmark", 15)).grid(row=2, column=0, sticky=tk.W, pady=15)
        login_username_user = tk.StringVar()
        login_username = ttk.Entry(login_window, textvariable=login_username_user, width=15,font=("Denmark", 15)).grid(row=2, column=1, sticky=tk.W, pady=15)

        def login_user():
            if (login_username_user.get().strip() == ""):
                messagebox.showerror("Error", "Field Can't be Empty.....")

            else:
                login_username_user_data = login_username_user.get().strip()

                inputs_login = (login_username_user_data)


                insert_data_query_login = ("SELECT Name, Image FROM user_record WHERE Username='%s'"%(login_username_user_data))

                cursor.execute(insert_data_query_login)


                result_login = cursor.fetchall()


                if  result_login:
                    print(result_login)

                    for i in result_login:
                        print(i)
                        lst = []
                        for j in i:
                            lst.append(j)
                        #     print(j)
                        #
                        print(lst[0])
                        print(lst[1])

                    def open_camera_login():

                        # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
                        # other example, but it includes some basic performance tweaks to make things run a lot faster:
                        #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
                        #   2. Only detect faces in every other frame of video.

                        # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
                        # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
                        # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

                        # Get a reference to webcam #0 (the default one)
                        video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

                        # Load a sample picture and learn how to recognize it.
                        obama_image = face_recognition.load_image_file(str(lst[1]))
                        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

                        # Load a second sample picture and learn how to recognize it.
                        # biden_image = face_recognition.load_image_file("biden.jpg")
                        # biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

                        # Create arrays of known face encodings and their names
                        known_face_encodings = [
                            obama_face_encoding

                        ]
                        known_face_names = [
                            str(lst[0])

                        ]

                        # Initialize some variables
                        face_locations = []
                        face_encodings = []
                        face_names = []
                        process_this_frame = True

                        while True:
                            # Grab a single frame of video
                            ret, frame = video_capture.read()

                            frame = cv2.flip(frame, 1)

                            # Only process every other frame of video to save time
                            if process_this_frame:
                                # Resize frame of video to 1/4 size for faster face recognition processing
                                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                                rgb_small_frame = small_frame[:, :, ::-1]

                                # Find all the faces and face encodings in the current frame of video
                                face_locations = face_recognition.face_locations(rgb_small_frame)
                                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                                face_names = []
                                for face_encoding in face_encodings:
                                    # See if the face is a match for the known face(s)
                                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                    name = "Invalid User ❌❌❌❌"

                                    # If a match was found in known_face_encodings, just use the first one.
                                    # if True in matches:
                                    #     first_match_index = matches.index(True)
                                    #     name = known_face_names[first_match_index]

                                    # Or instead, use the known face with the smallest distance to the new face
                                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                                    best_match_index = np.argmin(face_distances)
                                    if matches[best_match_index]:
                                        name = known_face_names[best_match_index]
                                        login_window.destroy()
                                        win3 = tk.Tk()
                                        win3.title("Home Page")
                                        win3.geometry("500x500")
                                        welcome_label = ttk.Label(win3, text="Login Successfully 🥳🥳🥳🥳:",font=("Denmark", 15)).grid(row=1, column=0,sticky=tk.W,pady=15)



                                    face_names.append(name)

                            process_this_frame = not process_this_frame

                            # Display the results
                            for (top, right, bottom, left), name in zip(face_locations, face_names):
                                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                                top *= 4
                                right *= 4
                                bottom *= 4
                                left *= 4

                                # Draw a box around the face
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                                # Draw a label with a name below the face
                                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                            # Display the resulting image
                            cv2.imshow('Video', frame)

                            # Hit 'q' on the keyboard to quit!
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                        # Release handle to the webcam
                        video_capture.release()
                        cv2.destroyAllWindows()

                    open_camera_login_button = tk.Button(login_window, width=25, height=2, text="Open Camera",fg="blue", command=open_camera_login)
                    open_camera_login_button.grid(row=5, column=1, sticky=tk.W, pady=10)

                else:
                    messagebox.showerror("Error", "No User Found....")






        login_button = tk.Button(login_window, width=25, height=2, text="Click here to Login", fg="blue",command=login_user)
        login_button.grid(row=3, column=1, sticky=tk.W, pady=10)

        def goto_register_page():
            login_window.destroy()
            main_window()

        goto_register_button = tk.Button(login_window, width=28, height=2, text="New User ? Click here to Register",command=goto_register_page)
        goto_register_button.grid(row=4, column=1, sticky=tk.W, pady=10)

    goto_login_button = tk.Button(register_window, width=28, height=2, text="Already Register? Click here to Login",command=goto_login_page)
    goto_login_button.grid(row=5, column=1, sticky=tk.W, pady=10)

    register_window.mainloop()

main_window()