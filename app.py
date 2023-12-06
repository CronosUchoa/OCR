import cv2
import pytesseract as pt
#from matplotlib import pyplot as plt
import numpy as np


#2pt.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

#função
def encontrarRoiPlaca(source):
    img = cv2.imread(source)
    #cv2.imshow("img", img)

    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("cinza", img)

    _, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
    # cv2.imshow("binary", img)

    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    # cv2.imshow("defoque", desfoque)

    contornos, hierarquia = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, contornos, -1, (0, 255, 0), 1)

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro > 150:
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(aprox) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + alt, y + lar), (0, 255, 0), 2)
                roi = img[y:y + lar, x:x + alt]
                cv2.imwrite('./Imagens/roi.jpg', roi)

    #cv2.imshow("contornos", img)


def preProcessamentoRoiPlaca():
    img_roi = cv2.imread("./Imagens/roi.jpg")

    if img_roi is None:
        return

    resize_img_roi = cv2.resize(img_roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img_cinza = cv2.cvtColor(resize_img_roi, cv2.COLOR_BGR2GRAY)

    # Binariza imagem
    _, img_binary = cv2.threshold(img_cinza, 31, 255, cv2.THRESH_BINARY)

    # Desfoque na Imagem
    img_desfoque = cv2.GaussianBlur(img_binary, (5, 5), 1)

    # Grava o pre-processamento para o OCR
    cv2.imwrite("./Imagens/roi-ocr.jpg", img_desfoque)

    cv2.imshow("ROI", img_desfoque)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img_desfoque


def ocrImageRoiPlaca():
    image = cv2.imread("./Imagens/roi-ocr.jpg")

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    saida = pt.pytesseract.image_to_string(image, lang='eng', config=config)

    return saida


def remove_acentos(text):
  temAcento = 0
  letras_com_acento = ['á','ã','â','é','ê','í','ó','õ','ô','ú','ü', '_']

  letras_sem_acento = ['a','a','a','e','e','i','o','o','o','u','u', '']

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


## Menu0

def ImagemSimplesCapturaDeCaracteres():
  
  pt.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
 
  img = cv2.imread('./Imagens/Test.jpg')

  #@img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  print(pt.pytesseract.image_to_string(img))
  boxes = pt.pytesseract.image_to_boxes(img, lang = 'por')
  imgH,imgW, _ = img.shape

  for b in boxes.splitlines():
      b = b.split(' ')
      letra,posicaoX,posicaoY,larguraW,alturaH =  remove_acentos(b[0]),int(b[1]),int(b[2]),int(b[3]),int(b[4])
      cv2.rectangle(img, (posicaoX,imgH - posicaoY),(larguraW,imgH-alturaH),(0,0,255),2)
      cv2.rectangle(img, (posicaoX,imgH - posicaoY),(larguraW, imgH - alturaH),(0,0,255),2)
      cv2.putText(img,letra,(posicaoX,imgH-posicaoY+25),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,255),2)

  #Mostrando OCR1
  cv2.imshow('Imagem', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


def Placa_de_carro():
  pt.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
  config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

  encontrarRoiPlaca("./Imagens/carro4.jpg")

  pre = preProcessamentoRoiPlaca()

  ocr = ocrImageRoiPlaca()
  ocr_new  = ocr.replace("_","")
  print(ocr_new)
 
  #cv2.imshow('Imagem', new_roi)
 
  #Mostrando OCR2
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def default():
    return "Opção inválida. As opções válidas 1, 2 e 3 - 0 para sair"

def switch_case(option):
    switch_dict = {
        1: ImagemSimplesCapturaDeCaracteres,
        2: Placa_de_carro,
    }
    return switch_dict.get(option, default)()

# Loop principal
while True:
    try:
        opcao_escolhida = int(input("Digite a opção 1,2,3 e (0 para sair): "))
        
        if opcao_escolhida == 0:
            print("Saindo do programa. Até logo!")
            break  # Encerra o loop se a opção for 0
        else:
            resultado = switch_case(opcao_escolhida)
            print(resultado)
    except ValueError:
        print("Por favor, digite um número inteiro.")



##



#Tecnicas que talvez seja utilizados
  # img_ruido = cv2.imread('comRuido.jpg')
  # img_original = cv2.imread('Koala.jpg') #cv2.IMREAD_GRAYSCALE
  # img_clara_normalizacao = cv2.normalize(img, None, 5, 200, cv2.NORM_MINMAX)
  # img_escura_normalizacao = cv2.normalize(img, None, 1, 30, cv2.NORM_MINMAX)

  # img_ruido_pimenta = noise(img, 0.1)

 #Tirando Ruido
 # median = cv2.medianBlur(img_ruido_pimenta,5)

  #Mostrando Normalização
  # cv2.imshow('Imagem_clara_norma', img_clara_normalizacao)
  # cv2.imshow('Imagem_escura_norma', img_escura_normalizacao)


  # #Mostrando ruido e sem ruido
  # plt.subplot(121),plt.imshow(img_ruido_pimenta),plt.title('Com ruido')
  # plt.xticks([]),plt.yticks([])
  # plt.subplot(122),plt.imshow(median),plt.title('Sem ruido')
  # plt.xticks([]), plt.yticks([])
  # plt.show()


