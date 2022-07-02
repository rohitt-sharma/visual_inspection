
import cv2

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

root = Tk()
root.title('Difference_finder_app')
root.geometry("750x700")




def open_original():
    global path_1
    root.filename1 = filedialog.askopenfilename(initialdir="my_pics", title="Select a file",
                                                filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))


    basewidth = 100
    img = Image.open(root.filename1)
    wpercetage = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercetage)))
    old_image = img.resize((basewidth,hsize),Image.ANTIALIAS)


    ##################################
    entry_field1.delete(0,END)
    entry_field1.insert(0,root.filename1)


    path_1 = str(root.filename1)
    print(path_1)

    return (path_1)


def open_new():
    global new_image
    global path_2
    root.filename2 = filedialog.askopenfilename(initialdir="my_pics", title="Select a file",
                                                filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))

    ##################################
    entry_field2.delete(0, END)
    entry_field2.insert(0, root.filename2)

    path_2 = str(root.filename2)
    print(path_2)
    return (path_2)


def visual_inspection(path_1,path_2):

    global diff_image

    print("------",path_1)
    print("-*-*-*-*-*-*--",path_2)

    first_img = cv2.imread(path_2)  # New image
    second_img = cv2.imread(path_1)  # Original image
    # compute difference
    difference = cv2.subtract(second_img, first_img)

    # color the mask read
    Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    difference[mask != 255] = [0, 0, 255]

    # add the red mask to the images to make the differences obvious
    first_img[mask != 255] = [0, 0, 255]
    #second_img[mask != 255] = [0, 0, 255]


    # resize the output images
    dim = (600,600)

    resized = cv2.resize(first_img,dim)



    # store images
    cv2.imwrite('my_pics/diffOvermy_img.png', resized)
    #cv2.imwrite('my_pics/diffOver_2nd_img.png', resized)

    # mask of difference over image 2
    cv2.imwrite('my_pics/diff.png', difference)

    diff_image = ImageTk.PhotoImage(Image.open('my_pics/diffOvermy_img.png'))
    my_image_label_original = Label(image=diff_image).grid(row=4,column=1)



my_btn_original = Button(root,text="open Origianl File",command=open_original).grid(row=0,column=0)
my_btn_new = Button(root,text="open new File",command=open_new).grid(row=1,column=0)
my_btn_show = Button(root,text="Show missing bracket",command=lambda :visual_inspection(path_1= path_1, path_2=path_2)).grid(row=3,column=0)

entry_field1 = Entry(root,width = 100,bg="white",fg="black")
entry_field1.grid(row=0,column=1)
entry_field1.insert(0,"Select old pic")

entry_field2 = Entry(root,width = 100,bg="white",fg="black")
entry_field2.grid(row=1,column=1)
entry_field2.insert(0,"Select New pic")




root.mainloop()