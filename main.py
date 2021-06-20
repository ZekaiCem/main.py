import cv2
import numpy as np

video = cv2.VideoCapture("video1.mp4") # video ekledim
fgbg = cv2.createBackgroundSubtractorMOG2() # arkaplan çıkarmak için kullanacağım

kernel = np.ones((10, 10), np.uint8) # matris oluşturdum


class Koordinat:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sensör:
    def __init__(self, koor1, koor2, kare_w, kare_h):
        self.koor1 = koor1
        self.koor2 = koor2
        self.kare_w = kare_w
        self.kare_h = kare_h
        self.maskenin_alanı = abs(self.koor2.x - self.koor1.x) * abs(self.koor2.y - self.koor1.y)
        self.maske = np.zeros((kare_h, kare_w, 1), np.uint8) # tamamen 1 lerden oluşan bir matris oluşturdum
        cv2.rectangle(self.maske, (self.koor1.x, self.koor1.y), (self.koor2.x, self.koor2.y), (255),
                      thickness=cv2.FILLED) # bir dikdörtgen oluşturdum
        self.Durum = False
        self.Araç_Sayısı= 0
Sensör1 = Sensör(Koordinat(280, 410), Koordinat(310, 380), 450, 480)
Sensör2 = Sensör(Koordinat(130, 410), Koordinat(160, 380), 450, 480)
#Sensör3 = Sensör(Koordinat(280, 133), Koordinat(293, 110), 634, 334)

font = cv2.FONT_ITALIC
while 1:
    bos1, Kare = video.read()
    kesme_Kare = Kare[0:480, 0:450]
    #BG_temiz= cv2.cvtColor(kesme_Kare, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("siyah beyaz",BG_temiz)
    BG_temiz= fgbg.apply(kesme_Kare)
    BG_temiz= cv2.morphologyEx(BG_temiz, cv2.MORPH_RECT,kernel) # hareketli nesneleri belirledim morphologyEx sayesinde daha katı bir biçim verdim



    _cnts, bos2 = cv2.findContours(BG_temiz, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # siyah ve beyazı birbirinden ayırıp beyaz kısımları belirledim
    Sonuc = kesme_Kare.copy()
    Doldurma = np.zeros((kesme_Kare.shape[0], kesme_Kare.shape[1], 1), np.uint8)
    for cnt in _cnts:
        x, y, w, h = cv2.boundingRect(cnt) # hareketli nesnenin boyutuna yaklaşık bir dikdörtgen oluşturdum
        if (w > 30 and h > 30):
            cv2.rectangle(Sonuc, (x, y), (x + w, y + h), (0, 255, 0), thickness=4)
            cv2.rectangle(Doldurma, (x, y), (x + w, y + h), (255), thickness=cv2.FILLED)


    Sensör_maske = cv2.bitwise_and(Doldurma, Doldurma, mask=Sensör1.maske)
    Sensör_maske2 = cv2.bitwise_and(Doldurma, Doldurma, mask=Sensör2.maske)
    #Sensör_maske3 = cv2.bitwise_and(Doldurma, Doldurma, mask=Sensör3.maske)
    Sensör_PX = np.sum(Sensör_maske == 255)
    Sensör_PX2 = np.sum(Sensör_maske2 == 255)
    #Sensör_PX3 = np.sum(Sensör_maske3 == 255)
    Sensör_oran = Sensör_PX / Sensör1.maskenin_alanı
    Sensör_oran2 = Sensör_PX2 / Sensör2.maskenin_alanı
    #Sensör_oran3 = Sensör_PX3 / Sensör3.maskenin_alanı
    if (Sensör_oran >= 1) and Sensör1.Durum == False:
        cv2.rectangle(Sonuc, (Sensör1.koor1.x, Sensör1.koor1.y), (Sensör1.koor2.x, Sensör1.koor2.y), (0, 255, 0),
                      thickness=cv2.FILLED)
        Sensör1.Durum=True
    elif(Sensör_oran <= 1) and Sensör1.Durum == True:
        cv2.rectangle(Sonuc, (Sensör1.koor1.x, Sensör1.koor1.y), (Sensör1.koor2.x, Sensör1.koor2.y), (0, 0, 255),
                      thickness=cv2.FILLED)
        Sensör1.Durum=False
        Sensör1.Araç_Sayısı += 1
    #elif(Sensör_oran3 >= 1) and Sensör3.Durum == False:
        #cv2.rectangle(Sonuc, (Sensör3.koor1.x, Sensör3.koor1.y), (Sensör3.koor2.x, Sensör3.koor2.y), (0, 255, 0),
                      #thickness=cv2.FILLED)
        #Sensör3.Durum=True
    elif(Sensör_oran2 >= 1) and Sensör2.Durum == False:
        cv2.rectangle(Sonuc, (Sensör2.koor1.x, Sensör2.koor1.y), (Sensör2.koor2.x, Sensör2.koor2.y), (0, 255, 0),
                      thickness=cv2.FILLED)
        Sensör2.Durum=True
    elif(Sensör_oran2 <= 1) and Sensör2.Durum == True:
        cv2.rectangle(Sonuc, (Sensör2.koor1.x, Sensör2.koor1.y), (Sensör2.koor2.x, Sensör2.koor2.y), (0, 0, 255),
                      thickness=cv2.FILLED)
        Sensör2.Durum=False
        Sensör1.Araç_Sayısı += 1

    #elif(Sensör_oran3 <= 1) and Sensör3.Durum == True:
        #cv2.rectangle(Sonuc, (Sensör3.koor1.x, Sensör3.koor1.y), (Sensör3.koor2.x, Sensör3.koor2.y), (0, 0, 255),
                      #thickness=cv2.FILLED)
        #Sensör3.Durum=False
        #Sensör1.Araç_Sayısı += 1


    else:
        cv2.rectangle(Sonuc, (Sensör1.koor1.x, Sensör1.koor1.y), (Sensör1.koor2.x, Sensör1.koor2.y), (0, 0, 255),
                      thickness=cv2.FILLED)
        cv2.rectangle(Sonuc, (Sensör2.koor1.x, Sensör2.koor1.y), (Sensör2.koor2.x, Sensör2.koor2.y), (0, 0, 255),
                      thickness=cv2.FILLED)
        #cv2.rectangle(Sonuc, (Sensör3.koor1.x, Sensör3.koor1.y), (Sensör3.koor2.x, Sensör3.koor2.y), (0, 0, 255),
                      #thickness=cv2.FILLED)
    cv2.putText(kesme_Kare,str((Sensör1.Araç_Sayısı)-1),(30,60),font,2,(255,255,255),thickness=2)
    cv2.putText(Sonuc, str((Sensör1.Araç_Sayısı)-1), (30, 60), font, 2, (255, 255, 255), thickness=2)
    cv2.imshow("Deneme", Sonuc)
    cv2.imshow("main",kesme_Kare)
    cv2.imshow("asdasd",BG_temiz)
    cv2.imshow("Doldurma", Doldurma)
    cv2.imshow("Maske",Sensör_maske)

    k = cv2.waitKey(30) & 0xff # "ESC" ye bas çık
    if k == 27:
        break
video.release()
cv2.destroyAllWindows()
