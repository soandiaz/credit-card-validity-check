import streamlit as st
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import re
from datetime import datetime
import numpy as np
def main():
  st.title("Card Validity Checker")

  uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
  if uploaded_image is not None:
    file_bytes = np.frombuffer(uploaded_image.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    data=pytesseract.image_to_data(img,output_type=pytesseract.Output.DICT)
    flag=0
    def validity_check(data):
      exp_lst=[]
      for i in range(len(data['text'])):
        if re.search(r'\d{1,2}/\d{1,4}',data['text'][i]):
          exp_lst.append(data['text'][i])
      if len(exp_lst)==2:
        m1,y1=tuple(exp_lst[0].split("/")) 
        m2,y2=tuple(exp_lst[1].split("/")) 
        if int(y2)>int(y1):
          mon,yr=tuple(exp_lst[1].split("/"))
        else:
          mon,yr=tuple(exp_lst[0].split("/"))
      elif len(exp_lst)==1:
        mon,yr=tuple(exp_lst[0].split("/")) 
      else:
        flag=1
        return flag
      curdate=datetime.now()
      curyr=curdate.year
      curmon=curdate.month
      
      if len(yr)==2:
        curyr=curyr%100
      if int(yr)>curyr:
        st.success("Card is valid")
      elif int(yr)==curyr:
        if int(mon)>=curmon:
          st.success("Card is valid")
        else:
          st.error("Card is invalid")
      else:
        st.error("Card is invalid")
    flag=validity_check(data)
    if flag:
      st.error("Card is not read")
main()
    


