
import cv2

# For making fast api
from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class Visual_inspection(BaseModel):
    New_image: str
    Original_image : str


app = FastAPI()

@app.post("/Visual_inspection/")

def attrition_rate(item: Visual_inspection):

    # For fit and transformation to work
    first_img = cv2.imread(f"my_pics/{item.New_image}.jpg")
    second_img = cv2.imread(f"my_pics/{item.Original_image}.jpg")
    #print("111111111111111111111111111")

    # compute difference
    difference = cv2.subtract(second_img ,first_img)

    # color the mask read
    Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    ret,mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    difference[mask != 255] = [0, 0, 255]

    #print("2222222222222222222222222222222222222222")

    # add the red mask to the images to make the differences obvious
    first_img[mask != 255] = [0, 0, 255]
    second_img[mask != 255] = [0, 0, 255]

    # store images
    cv2.imwrite('my_pics/diffOvermy_img.png', first_img)
    cv2.imwrite('my_pics/diffOver_2nd_img.png', second_img)

    # mask of difference over image 2
    cv2.imwrite('my_pics/diff.png', difference)

    return {"Image shown"}



