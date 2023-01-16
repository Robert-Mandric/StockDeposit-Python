# StockDeposit-Python

**Avem aplicatia care tine stocul unui depozit. Efectuati urmatoarele imbunatatiri:**
	
1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o                          
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o 
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa                          
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului); 	--SMTP--

4. Utilizati Regex pentru a cauta:
    - un produs introdus de utilizator;
    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--                                              

5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
   
      - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
      - denc VARCHAR(255) (text in loc de varchar in sqlite3)
   
      - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
      - idc INT NOT NULL
      - denp VARCHAR(255)
      - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
      - FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
 
      - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
      - idp INT NOT NULL
      - cant DECIMAL(10,3) DEFAULT 0
      - data DATE

6. Implementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date.

8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).                      
Pretul de iesire va fi pretul din acel moment;  

9. Creati doua metode noi, diferite de cele facute la clasa, testatile si asigurativa ca functioneaza cu succes;
