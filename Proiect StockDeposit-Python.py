from datetime import datetime
import email
from email.mime.multipart import MIMEMultipart
from prettytable import PrettyTable
import pygal
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Stoc:
    categorii = {}

    date = []
    listaIntrari = []
    listaIesiri = []
    listaLimite = []

    produsCalculat = 0
    countIntrari = 0

    def __init__(self, denp, categ, um='buc', limita=0, sold=0):
        self.denp = denp
        self.categ = categ
        self.limita = limita
        self.um = um
        self.sold = sold
        self.do = {}
        if categ in Stoc.categorii:
            self.categorii[categ] += [denp]
        else:
            self.categorii[categ] = [denp]

    def addToLista(self, d, intrare, iesire):
        self.date.append(d)
        self.listaIntrari.append(intrare)
        self.listaIesiri.append(iesire)

    def genChart(self, pStart=0, pStop=0):
        line_chart = pygal.Line()
        line_chart.title = f'Grafic intrari si iesiri {self.denp}'

        tempDate = []
        tempIn = []
        tempOut = []

        for k, v in self.do.items():
            if pStart and pStop:
                if pStart <= v[0] <= pStop:
                    tempDate.append(v[0])
                    tempIn.append(v[1])
                    tempOut.append(v[2])
            else:
                tempDate.append(v[0])
                tempIn.append(v[1])
                tempOut.append(v[2])

        line_chart.x_labels = tempDate
        line_chart.add('Intrari', tempIn)
        line_chart.add('Iesiri', tempOut)
        line_chart.render_to_file(f'grafic_{self.denp}.svg')

    def gen_cheia(self):
        if self.do:
            cheia = max(self.do.keys()) + 1
        else:
            cheia = 1
        return cheia

    def intrari(self, cant, pretInt, data=str(datetime.now().strftime('%Y/%m/%d'))):
        cheia = self.gen_cheia()
        self.do[cheia] = [data, cant, 0, pretInt, 0]
        self.sold += cant

    def iesiri(self, cant, pretIes, data=str(datetime.now().strftime('%Y/%m/%d'))):
        cheia = self.gen_cheia()
        if self.sold < cant:
            cant = self.sold
        self.do[cheia] = [data, 0, cant, 0, pretIes]
        self.sold -= cant

    def doAlerta(self):
        print(f"!!!!!!!!!!!! PRODUSUL {self.denp} E SUB LIMITA !!!!!!!!!!!!!!!!")
        self.sendEmail("robert.gabriel30@yahoo.com", f"Alerta produs {self.denp}",
                       f"Produsul {self.denp} a intrat sub limita!")

    def sendFisap(self):
        tabel = PrettyTable()
        tabel.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire', 'Pret Intrare', 'Pret Iesire']
        for k, v in self.do.items():
            tabel.add_row([k, v[0], v[1], v[2], v[3], v[4]])
        fisaProdus = tabel.get_html_string(
            attributes={'border': 1, 'style': 'border-width: 1px; border-collapse: collapse;'})
        self.sendEmail("robert.gabriel30@yahoo.com", f"Fisa produsului {self.denp}", fisaProdus)

    def sendEmail(self, to, subject, message):
        hostname = "mail.hexnet.space"
        port = 25
        msg = MIMEMultipart('alternative')
        msg['from'] = "test@hexnet.space"
        msg['to'] = to
        msg['Subject'] = subject
        msg.attach((MIMEText(message, 'html')))
        mailserver = smtplib.SMTP(hostname, port)
        mailserver.login(msg['from'], "test123")
        mailserver.sendmail(msg['from'], msg['to'], msg.as_string())
        mailserver.quit()

    def fisap(self):
        print(f'Fisa produsului {self.denp} {self.um}')
        listeaza = PrettyTable()
        listeaza.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire', 'Pret Intrare', 'Pret Iesire']
        for k, v in self.do.items():
            listeaza.add_row([k, v[0], v[1], v[2], v[3], v[4]])
            self.addToLista(v[0], v[1], v[2])
            self.calculPretIntrare(v[1], v[3])
        print(listeaza)
        print('Stoc final: ', self.sold)
        print('Limita: ', self.limita)
        if self.sold <= self.limita:
            self.doAlerta()
        print(f"Pretul produselor stocate este {(self.produsCalculat / self.countIntrari):.2f}")
        print("----" * 30)
        print("\n")

    def findProdus(e):
        ret = 0
        for k, v in Stoc.categorii.items():
            reg = re.compile(f".*{e}*.")
            newlist = list(filter(reg.match, v))
            for gasit in newlist:
                print(f"Am gasit produsul {gasit} in categoria {k}")
                ret = 1

        if not ret:
            print("Nu am gasit produsul!")

    def findTranzactie(val):
        count = 0
        for x in Stoc.listaIesiri:
            if re.match(val, str(x)):
                data = Stoc.date[count]
                print(f"Am gasit tranzactia cu {val} numar de iesiri pe data de {data}")
            count += 1
        if not count:
            print("Nu ma gasit nici o tranzactie!")

    def calculPretIntrare(self, intrari, pret):
        self.produsCalculat = self.produsCalculat + (intrari * pret)
        self.countIntrari = self.countIntrari + intrari


ciocan = Stoc('ciocan', 'scule', 'buc', 2)
ciocan.intrari(100, 100, '1990/1/1')
ciocan.iesiri(45, 51, '1995/1/1')
ciocan.intrari(100, 100, '2000/1/1')
ciocan.iesiri(50, 51, '2010/1/1')
ciocan.genChart('1995/1/1', '2010/1/1')
ciocan.fisap()

mere = Stoc('mere', 'fructe', 'kg', 20)
mere.intrari(15, 100, '1990/1/1')
mere.iesiri(5, 51, '1995/1/1')
mere.genChart()
mere.fisap()

prune = Stoc('prune', 'fructe', 'kg', 100)
prune.intrari(100, 200, '1990/1/1')
prune.iesiri(20, 300, '1990/1/1')
prune.intrari(120, 200, '1995/1/1')
prune.iesiri(25, 250, '1995/1/1')
prune.intrari(160, 100, '1995/1/1')
prune.iesiri(361, 170, '1995/1/1')
prune.intrari(160, 500, '2000/1/1')
prune.iesiri(100, 550, '2000/1/1')
prune.intrari(160, 600, '2050/1/1')
prune.iesiri(100, 700, '2050/1/1')
prune.genChart('2000/1/1', '2000/1/1')
prune.sendFisap()
prune.fisap()

Stoc.findProdus(input("Ce produs cautati? "))
Stoc.findTranzactie(input("Ce tranzactie cautati? "))
