from django.db import models

class Postac(models.Model):
    imie = models.CharField(max_length=100)
    rasa = models.CharField(max_length=50)
    klasa = models.CharField(max_length=50)
    hp = models.IntegerField(default=0)
    max_hp = models.IntegerField(default=0)
    sila = models.IntegerField(default=0)
    zrecznosc = models.IntegerField(default=0)
    wytrzymalosc = models.IntegerField(default=0)
    inteligencja = models.IntegerField(default=0)
    charyzma = models.IntegerField(default=0)
    doswiadczenie = models.IntegerField(default=0)
    poziom = models.IntegerField(default=1)
    exp_do_nastepnego_poziomu = models.IntegerField(default=100)

    # Możesz dodać pole JSONField na ekwipunek, lub osobną relację ManyToManyField
    # np. ekwipunek_items = models.ManyToManyField('Item')
    # Na razie uprośćmy i pomińmy to, ale pamiętaj o tym.

    def __str__(self):
        return f"{self.imie} ({self.rasa} {self.klasa})"

    def ustaw_poczatkowe_statystyki(self):
        # Ta logika zostanie przeniesiona do widoku lub w toku tworzenia postaci
        # Ale jeśli chcesz, aby była metodą modelu, to może być tak:
        if self.rasa == "Człowiek" and self.klasa == "Wojownik":
            self.max_hp = 100
            self.hp = self.max_hp
            self.sila = 15
            self.zrecznosc = 10
            self.wytrzymalosc = 12
            self.inteligencja = 8
            self.charyzma = 7
        else:
            self.max_hp = 50
            self.hp = self.max_hp
            self.sila = 5
            self.zrecznosc = 5
            self.wytrzymalosc = 5
            self.inteligencja = 5
            self.charyzma = 5
        self.save() # Zapisz zmiany w bazie danych

    def dodaj_doswiadczenie(self, ilosc_exp):
        self.doswiadczenie += ilosc_exp
        while self.doswiadczenie >= self.exp_do_nastepnego_poziomu:
            self.poziom_w_gore()
        self.save() # Zapisz zmiany po dodaniu doświadczenia

    def poziom_w_gore(self):
        self.poziom += 1
        self.doswiadczenie -= self.exp_do_nastepnego_poziomu
        self.exp_do_nastepnego_poziomu = int(self.exp_do_nastepnego_poziomu * 1.5)
        self.max_hp += 10
        self.hp = self.max_hp
        self.sila += 2
        self.zrecznosc += 1
        self.wytrzymalosc += 2
        self.save() # Zapisz zmiany po awansie

class Przeciwnik(models.Model):
    nazwa = models.CharField(max_length=100)
    hp = models.IntegerField()
    max_hp = models.IntegerField()
    sila = models.IntegerField()
    zrecznosc = models.IntegerField()
    # Możesz dodać pole do przechowywania doświadczenia, które daje przeciwnik po pokonaniu
    exp_do_pokonania = models.IntegerField(default=0)

    def __str__(self):
        return self.nazwa

    def otrzymuje_obrazenia(self, obrazenia):
        self.hp -= obrazenia
        if self.hp < 0:
            self.hp = 0
        self.save() # Zapisz zmiany w bazie danych

        if self.hp <= 0:
            return True # Przeciwnik pokonany
        return False # Przeciwnik żyje