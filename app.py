import cv2
import pytesseract as pt

#função
def remove_acentos(text):
  temAcento = 0
  letras_com_acento = ['á','ã','â','é','ê','í','ó','õ','ô','ú','ü']

  letras_sem_acento = ['a','a','a','e','e','i','o','o','o','u','u']

  text_list = list(text)

  for i in range(len(text_list)):
    for letra in letras_com_acento:
      if text_list[i] == letra:
        text_list[i] = letras_sem_acento[letras_com_acento.index(letra)]
        temAcento = 1
      

  if temAcento == 1: 
   return str(text_list)[2]
  return text
  
pt.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

img = cv2.imread('Test.jpg')

#@img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#print(pt.pytesseract.image_to_string(img,lang='por'))
boxes = pt.pytesseract.image_to_boxes(img,lang='por')
imgH,imgW, _ = img.shape

for b in boxes.splitlines():
    b = b.split(' ')
    letra,posicaoX,posicaoY,larguraW,alturaH =  remove_acentos(b[0]),int(b[1]),int(b[2]),int(b[3]),int(b[4])
   # cv2.rectangle(img, (posicaoX,imgH - posicaoY),(larguraW,imgH-alturaH),(0,0,255),2)
    cv2.rectangle(img, (posicaoX,imgH - posicaoY),(larguraW, imgH - alturaH),(0,0,255),2)
    cv2.putText(img,letra,(posicaoX,imgH-posicaoY+25),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,255),2)

cv2.imshow('Imagem', img)
cv2.waitKey(0)


