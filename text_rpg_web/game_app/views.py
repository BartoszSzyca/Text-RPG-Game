from django.shortcuts import render, redirect, get_object_or_404
from .models import Postac, Przeciwnik
from django.http import HttpResponse  # Na potrzeby przykładu


# Pamiętaj: W realnej grze stan gracza będzie związany z zalogowanym użytkownikiem
# lub przechowywany w sesji (dla niezalogowanych).
# Dla uproszczenia, na początku, możesz użyć sesji Django.

def menu_glowne(request):
    """Wyświetla główne menu gry."""
    return render(request, 'game_app/menu_glowne.html')


def nowa_gra(request):
    """Rozpoczyna nową grę, ekran tworzenia postaci."""
    if request.method == 'POST':
        imie = request.POST.get('imie')
        rasa = request.POST.get('rasa')  # Z formularza HTML
        klasa = request.POST.get('klasa')  # Z formularza HTML

        # Walidacja danych
        if not imie or not rasa or not klasa:
            return render(request, 'game_app/nowa_gra.html',
                          {'error': 'Wypełnij wszystkie pola.'})

        gracz = Postac.objects.create(imie=imie, rasa=rasa, klasa=klasa)
        gracz.ustaw_poczatkowe_statystyki()  # Wywołaj metodę modelu

        # Zapisz ID gracza w sesji, aby móc go później odzyskać
        request.session['gracz_id'] = gracz.id
        request.session['current_scene'] = 'las'  # Ustaw początkową scenę

        # Przekieruj do pierwszej sceny
        return redirect('scena_las')
    return render(request, 'game_app/nowa_gra.html')


def wczytaj_gre(request):
    """Wczytuje grę (na razie atrapa, potem lista zapisów)."""
    # Tutaj logika wczytywania, np. wyświetlenie listy postaci użytkownika
    # i wybranie jednej z nich do wczytania ID do sesji.
    return render(request, 'game_app/wczytaj_gre.html')


def opcje_gry(request):
    """Opcje gry (atrapa)."""
    return render(request, 'game_app/opcje_gry.html')


def scena_las(request):
    """Scena w lesie z drapieżnikiem."""
    gracz_id = request.session.get('gracz_id')
    if not gracz_id:
        return redirect(
            'menu_glowne')  # Jeśli nie ma gracza w sesji, wróć do menu

    gracz = get_object_or_404(Postac, id=gracz_id)

    # Sprawdź, czy przeciwnik już istnieje w sesji/bazie (np. jeśli gracz odświeżył stronę)
    # W bardziej rozbudowanych grach, przeciwnicy byliby też modelami z ID
    # Dla uproszczenia, użyjemy sesji do przechowywania stanu drapieżnika
    if 'drapiezniki_id' not in request.session:
        # Stwórz nowego drapieżnika tylko raz na początku sceny
        drapiezniki = Przeciwnik.objects.create(
            nazwa="Skrzekliwy Leśny Drapieżnik",
            hp=50,
            max_hp=50,
            sila=10,
            zrecznosc=8,
            exp_do_pokonania=50
        )
        request.session['drapiezniki_id'] = drapiezniki.id
    else:
        drapiezniki = get_object_or_404(Przeciwnik,
                                        id=request.session['drapiezniki_id'])

    komunikat = ""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'atak':
            if gracz.hp <= 0 or drapiezniki.hp <= 0:
                komunikat = "Walka już się zakończyła!"
            else:
                obrazenia_gracza = gracz.sila - drapiezniki.zrecznosc // 2
                if obrazenia_gracza < 1:
                    obrazenia_gracza = 1

                komunikat += f"Atakujesz {drapiezniki.nazwa} i zadajesz {obrazenia_gracza} obrażeń!<br>"
                drapiezniki_pokonany = drapiezniki.otrzymuje_obrazenia(
                    obrazenia_gracza)

                if drapiezniki_pokonany:
                    komunikat += f"** {drapiezniki.nazwa} został pokonany! **<br>"
                    gracz.dodaj_doswiadczenie(drapiezniki.exp_do_pokonania)

                    # Dodaj przedmiot do ekwipunku (tutaj uproszczenie)
                    # W realnym systemie byłby to model Item
                    if 'ekwipunek' not in request.session:
                        request.session['ekwipunek'] = []
                    request.session['ekwipunek'].append("Szpon Drapieżnika")
                    request.session.modified = True  # Pamiętaj o tym dla mutable objects w sesji!

                    komunikat += f"Przeszukujesz szczątki drapieżnika i znajdujesz dziwny, połyskujący **szpon**.<br>"
                    komunikat += f"Twój ekwipunek: {', '.join(request.session['ekwipunek'])}<br>"

                    del request.session[
                        'drapiezniki_id']  # Usuń przeciwnika z sesji
                    return redirect(
                        'wybory_po_walce')  # Przekieruj do kolejnej sceny

                # Tura przeciwnika, jeśli jeszcze żyje
                if drapiezniki.hp > 0:
                    obrazenia_drapieznika = drapiezniki.sila - gracz.wytrzymalosc // 2
                    if obrazenia_drapieznika < 1:
                        obrazenia_drapieznika = 1
                    gracz.hp -= obrazenia_drapieznika
                    gracz.save()  # Zapisz zmiany HP gracza

                    komunikat += f"{drapiezniki.nazwa} atakuje! Otrzymujesz {obrazenia_drapieznika} obrażeń!<br>"

                    if gracz.hp <= 0:
                        komunikat += "<br>Twoje siły Cię opuszczają... Ciemność Cię ogarnia. Koniec gry."
                        # Możesz tu przekierować do ekranu Game Over
                        return render(request, 'game_app/game_over.html',
                                      {'gracz': gracz, 'komunikat': komunikat})

        elif action == 'uciekaj':
            if gracz.hp <= 0 or drapiezniki.hp <= 0:
                komunikat = "Walka już się zakończyła!"
            else:
                komunikat += "Próbujesz uciec! To bardzo niebezpieczne..."
                szansa_ucieczki = gracz.zrecznosc - drapiezniki.zrecznosc + 5
                if szansa_ucieczki > 10:
                    komunikat += "<br>Udało Ci się uciec od drapieżnika! Odzyskujesz oddech, ale nie masz pojęcia, gdzie jesteś."
                    del request.session[
                        'drapiezniki_id']  # Usuń przeciwnika z sesji
                    return redirect('wybory_po_walce')
                else:
                    komunikat += "<br>Drapieżnik jest zbyt szybki! Nie udało Ci się uciec i zostajesz trafiony!"
                    obrazenia_drapieznika = drapiezniki.sila - gracz.wytrzymalosc // 2
                    if obrazenia_drapieznika < 1:
                        obrazenia_drapieznika = 1
                    gracz.hp -= obrazenia_drapieznika
                    gracz.save()

                    komunikat += f"Otrzymujesz {obrazenia_drapieznika} obrażeń. Twoje HP: {gracz.hp}/{gracz.max_hp}."
                    if gracz.hp <= 0:
                        komunikat += "<br>Twoje siły Cię opuszczają... Ciemność Cię ogarnia. Koniec gry."
                        return render(request, 'game_app/game_over.html',
                                      {'gracz': gracz, 'komunikat': komunikat})

        # Jeśli akcja nie zakończyła sceny, odśwież widok
        return render(request, 'game_app/scena_las.html', {
            'gracz': gracz,
            'drapiezniki': drapiezniki,
            'komunikat': komunikat,
            'ekwipunek': request.session.get('ekwipunek', [])
            # Przekaż ekwipunek do szablonu
        })

    # Początkowe renderowanie sceny
    return render(request, 'game_app/scena_las.html', {
        'gracz': gracz,
        'drapiezniki': drapiezniki,
        'komunikat': "Słońce ledwie przebija się przez gęste korony drzew. Słyszysz niepokojące szmery...",
        'ekwipunek': request.session.get('ekwipunek', [])
        # Przekaż ekwipunek do szablonu
    })


def wybory_po_walce(request):
    """Widok po zakończeniu walki lub ucieczce."""
    gracz_id = request.session.get('gracz_id')
    if not gracz_id:
        return redirect('menu_glowne')
    gracz = get_object_or_404(Postac, id=gracz_id)

    if request.method == 'POST':
        wybor_drogi = request.POST.get('wybor_drogi')
        if wybor_drogi == 'wasna_sciezka':
            return render(request, 'game_app/koniec_demo.html',
                          {'sciezka': 'Wąskiej Ścieżce'})
        elif wybor_drogi == 'szeroki_trakt':
            return render(request, 'game_app/koniec_demo.html',
                          {'sciezka': 'Szerokim Trakcie'})
        else:
            # W przyszłości: redirect do innej sceny
            pass  # lub komunikat o błędzie

    return render(request, 'game_app/wybory_po_walce.html', {'gracz': gracz})


def game_over(request):
    """Ekran końca gry."""
    gracz_id = request.session.get('gracz_id')
    gracz = None
    if gracz_id:
        gracz = get_object_or_404(Postac, id=gracz_id)
        # Opcjonalnie: usunięcie gracza z sesji lub oznaczenie jako "martwy"
        del request.session['gracz_id']
        if 'drapiezniki_id' in request.session:
            del request.session['drapiezniki_id']
        request.session.modified = True
    return render(request, 'game_app/game_over.html', {'gracz': gracz})