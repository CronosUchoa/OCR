import cv2
import pytesseract as pt
from matplotlib import pyplot as plt
import numpy as np

pt.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

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
  
def noise(image, prob):
  output = image.copy()
  probs = np.random.random(output.
  shape[:2])
  output[probs<(prob/2)] = 0
  output[probs>1-(prob/2)] = 255
  return output


##

def Image1():
  img = cv2.imread('Test.jpg')
  # img_ruido = cv2.imread('comRuido.jpg')
  # img_original = cv2.imread('Koala.jpg') #cv2.IMREAD_GRAYSCALE
  img_clara_normalizacao = cv2.normalize(img, None, 5, 200, cv2.NORM_MINMAX)
  img_escura_normalizacao = cv2.normalize(img, None, 1, 30, cv2.NORM_MINMAX)

  img_ruido_pimenta = noise(img, 0.1)


  #@img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  #print(pt.pytesseract.image_to_string(img,lang='por'))
  boxes = pt.pytesseract.image_to_boxes(img)
  imgH,imgW, _ = img.shape

  for b in boxes.splitlines():
      b = b.split(' ')
      letra,posicaoX,posicaoY,larguraW,alturaH =  remove_acentos(b[0]),int(b[1]),int(b[2]),int(b[3]),int(b[4])
    # cv2.rectangle(img, (posicaoX,imgH - posicaoY),(larguraW,imgH-alturaH),(0,0,255),2)
      cv2.rectangle(img, (posicaoX,imgH - posicaoY),(larguraW, imgH - alturaH),(0,0,255),2)
      cv2.putText(img,letra,(posicaoX,imgH-posicaoY+25),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,255),2)


  #Tirando Ruido
  median = cv2.medianBlur(img_ruido_pimenta,5)

  #Mostrando Normalização
  cv2.imshow('Imagem_clara_norma', img_clara_normalizacao)
  cv2.imshow('Imagem_escura_norma', img_escura_normalizacao)


  #Mostrando ruido e sem ruido
  plt.subplot(121),plt.imshow(img_ruido_pimenta),plt.title('Com ruido')
  plt.xticks([]),plt.yticks([])
  plt.subplot(122),plt.imshow(median),plt.title('Sem ruido')
  plt.xticks([]), plt.yticks([])
  plt.show()

  #Mostrando OCR
  cv2.imshow('Imagem', img)


  cv2.waitKey(0)
  cv2.destroyAllWindows()


def Image2():
    return "Você escolheu a opção 2."

def Image3():
    return "Você escolheu a opção 3."

def default():
    return "Opção inválida. As opções válidas 1, 2 e 3 - 0 para sair"

def switch_case(option):
    switch_dict = {
        1: Image1,
        2: Image2,
        3: Image3
    }
    return switch_dict.get(option, default)()

# Loop principal
while True:
    try:
        opcao_escolhida = int(input("Digite a opção (0 para sair): "))
        
        if opcao_escolhida == 0:
            print("Saindo do programa. Até logo!")
            break  # Encerra o loop se a opção for 0
        else:
            resultado = switch_case(opcao_escolhida)
            print(resultado)
    except ValueError:
        print("Por favor, digite um número inteiro.")



##






