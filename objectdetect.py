import cv2
import utlis
from tkinter import *
from tkinter import filedialog

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("jpg files",
                                                      "*.jpg*"),
                                                     ("all files",
                                                      "*.*")))


def oper():
    webcam = False
    cap = cv2.VideoCapture(0)
    cap.set(10,160)
    cap.set(3,1920)
    cap.set(4,1080)
    scale = 3
    wP = 210 *scale
    hP= 297 *scale

    c=0
    while True:
        if webcam:success,img = cap.read()
        else: img = cv2.imread(filename)

        imgContours , conts = utlis.getContours(img,minArea=50000,filter=4)
        if len(conts) != 0:
            biggest = conts[0][2]
            #print(biggest)
            imgWarp = utlis.warpImg(img, biggest, wP,hP)
            imgContours2, conts2 = utlis.getContours(imgWarp,
                                                     minArea=2000, filter=4,
                                                     cThr=[50,50],draw = False)
            if len(conts) != 0:
                for obj in conts2:
                    cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)
                    nPoints = utlis.reorder(obj[2])
                    nW = round((utlis.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1)
                    nH = round((utlis.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1)
                    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    x, y, w, h = obj[3]
                    cv2.putText(imgContours2, 'width-{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (255, 0, 255), 2)
                    cv2.putText(imgContours2, 'height-{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (255, 0, 255), 2)

            cv2.imshow('A4', imgContours2)
            if c==0:
                c=1
                f=open("abc1.txt","a")
                f.write("The width and height of the "+ filename + " is: ")
                width=str(nW)
                height=str(nH)
                f.write(width)
                f.write(" ")
                f.write(height)
                f.write("\n")
                f.close()
        img = cv2.resize(img,(0,0),None,0.5,0.5)
        cv2.imshow('Original',img)

        window=Tk()
        window.title('exit')
        button_exit2 = Button(window, text="exit", height=2, width=25, command=quit,activebackground='cyan',
    activeforeground='black').pack()
        cv2.waitKey(1)
        window.mainloop()


window = Tk()

window.title('Object detection and dimension measurement')

window.geometry("1920x1080")

window['background']='#856ff8'

canvas = Canvas(window, width = 290, height = 230,bg='black')
canvas.pack()
img = PhotoImage(file="8.jpg")
canvas.create_image(20,20, anchor=NW, image=img,)


button_explore = Button(window,
                        text="Browse Files",height=4,width=250,
                        command=browseFiles,bg='black',fg='white').pack()

#photo = PhotoImage(file = r"C:\Users\DELL\Desktop\mini project\enter.jpg")
button_enter = Button(window,
                          text='Enter',command=oper, height=3, width=250
                          ,activebackground='cyan',
    activeforeground='black').pack()

button_exit2=Button(window,text="Stop",height=2,width=250,command=quit,bg='black',fg='white').pack()

window.mainloop()
