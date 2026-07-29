"""Biblioteka tresci PixelPedzel — posty + przypisane pliki (zdjecia/wideo).
Z tego generujemy harmonogram (queue.json). Edytuj tu teksty, gdy chcesz zmienic.

Kazdy wpis: (typ, plik, tekst)
  typ:  "image" albo "video"
  plik: sciezka w repo (bedzie serwowana z SITE_BASE_URL, np. pixelpedzel.pl)

Zasada: sprzedajemy EMOCJE i MOMENT, nie produkt. Rotacja: grafika emocjonalna -> wideo.
"""

POSTS = [
    # === POSTY SPRZEDAZOWE (PRIORYTET — ida jako pierwsze) ==================
    # Dotychczasowe posty pokazywaly STYLE. Te zdejmuja obiekcje i daja powod,
    # zeby napisac DZIS. Firma bez klientow potrzebuje najpierw tych.
    ("image", "assets/social/post-oferta-start.png",
     "Startuję z pracownią i szukam 5 pierwszych osób. 🤍\n\n"
     "Robię obraz z Waszego zdjęcia ze zniżką założycielską — w zamian proszę "
     "tylko o zdjęcie obrazu na Waszej ścianie i szczerą opinię.\n\n"
     "Projekt pokazuję przed drukiem. Nie spodoba się — nie płacisz.\n"
     "Napisz w komentarzu CHCĘ albo w wiadomości 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #personalizowanyprezent #handmadepl #prezent"),
    ("image", "assets/social/post-bez-ryzyka.png",
     "„A jak mi się nie spodoba?” — to najczęstsze pytanie, więc mówię wprost:\n\n"
     "Przysyłasz zdjęcie. Robię projekt. Pokazuję Ci go ZANIM cokolwiek zapłacisz.\n"
     "Nie podoba się? Nie płacisz i się rozchodzimy. Podoba się? Wtedy drukuję.\n\n"
     "Całe ryzyko jest po mojej stronie 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #prezent #personalizowanyprezent #handmadepl"),
    ("image", "assets/social/post-cennik.png",
     "Ile kosztuje obraz z Waszego zdjęcia? Bez ukrywania cen w wiadomościach 👇\n\n"
     "30×40 — 129 zł · 40×50 — 169 zł · 50×70 — 229 zł · 60×90 — 299 zł\n"
     "Projekt i podgląd gratis. Dostawa 15 zł, od 250 zł za darmo.\n\n"
     "Płacisz dopiero, gdy zaakceptujesz projekt 👉 pixelpedzel.pl\n\n"
     "#cennik #obraznaplotnie #prezent #personalizowanyprezent"),
    ("image", "assets/social/post-jak-dziala.png",
     "Jak zamówić obraz ze zdjęcia? Trzy kroki, cała reszta po mojej stronie:\n\n"
     "1. Wysyłasz zdjęcie (telefonem, jak wygodnie)\n"
     "2. Wybierasz styl — olej, komiks, szkic, witraż i inne\n"
     "3. Odbierasz gotowy obraz na płótnie\n\n"
     "Podgląd przed drukiem 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #jaktodziala #prezent #personalizowanyprezent"),
    ("image", "assets/social/post-ktory-styl.png",
     "Pytanie do Was — który styl wybralibyście dla siebie?\n\n"
     "A — olej klasyczny\nB — pop-art komiks\nC — szkic ołówkiem\nD — witraż\n\n"
     "Napiszcie literę w komentarzu, jestem ciekaw co wygra 👇\n"
     "(a jak chcecie zobaczyć swoje zdjęcie w tym stylu — pixelpedzel.pl)\n\n"
     "#obraznaplotnie #sztuka #prezent #ankieta"),
    ("image", "assets/social/post-wakacje.png",
     "Wróciliście z wakacji z tysiącem zdjęć w telefonie.\n"
     "Ile z nich jeszcze kiedyś obejrzycie? 📱\n\n"
     "Jedno z nich zasługuje na ścianę, nie na kartę pamięci.\n"
     "Wybierzcie to jedno — resztę zrobię ja 👉 pixelpedzel.pl\n\n"
     "#wakacje2026 #obraznaplotnie #pamiątka #dekoracjawnętrz"),
    ("image", "assets/social/post-slub.png",
     "Sezon ślubny w pełni — a prezenty wciąż te same: ręczniki, świeczniki, koperta.\n\n"
     "Obraz z ich wspólnego zdjęcia to prezent, którego nie schowają do szafy.\n"
     "Zostaje na ścianie na lata 👉 pixelpedzel.pl\n\n"
     "#prezentślubny #ślub2026 #wesele #obraznaplotnie #prezent"),
    ("image", "assets/social/post-prezent-argument.png",
     "Kwiaty zwiędną. Perfumy się skończą. Czekolada zniknie w dwa dni.\n"
     "Obraz z Waszego wspólnego zdjęcia zostanie na ścianie. 🤍\n\n"
     "Nie masz pomysłu na prezent? Weź bon — obdarowany sam wybierze zdjęcie i styl.\n"
     "👉 pixelpedzel.pl\n\n"
     "#pomysłnaprezent #prezent #bonpodarunkowy #obraznaplotnie"),

    # === METAMORFOZY PRZED -> PO (najlepiej klikajacy sie typ) ===
    ("image", "assets/social/post-po-wektor.png",
     "Jedno zdjęcie — tyle możliwości ✨ Oto ta sama para w stylu wektorowym.\n"
     "Podgląd przed drukiem, płacisz gdy Ci się spodoba 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #personalizowanyprezent #prezentdlapary #wektor"),
    ("image", "assets/social/post-po-komiks.png",
     "Wasza miłość jak z komiksu 💥 Zwykłe zdjęcie → pop-art na płótnie.\n"
     "👉 pixelpedzel.pl\n\n#popart #komiks #obraznaplotnie #prezentdlapary #prezent"),
    ("image", "assets/social/post-po-bajka3d.png",
     "Wasze zdjęcie jak kadr z animacji 🎬 Styl bajkowy 3D.\n"
     "👉 pixelpedzel.pl\n\n#obraznaplotnie #3d #prezentdlapary #personalizowanyprezent"),
    ("image", "assets/social/post-po-lego.png",
     "Zbudowani z miłości 🧱 Wasze zdjęcie w klockowym świecie.\n"
     "👉 pixelpedzel.pl\n\n#klocki #obraznaplotnie #prezent #pomysłnaprezent"),

    # === METAMORFOZY — kolejne pary/style ===
    ("image", "assets/social/post-po-olej.png",
     "Wasz zachód słońca zamieniony w obraz olejny 🌅 Z jednego zdjęcia — dzieło.\n"
     "👉 pixelpedzel.pl\n\n#obraznaplotnie #olej #prezentdlapary #personalizowanyprezent"),
    ("image", "assets/social/post-po-szkic.png",
     "Tyle lat, jedna miłość ❤️ Idealny prezent dla rodziców lub dziadków — "
     "ich wspólne zdjęcie jako ręczny szkic na płótnie.\n"
     "👉 pixelpedzel.pl\n\n#prezentdladziadków #rocznicaślubu #obraznaplotnie #szkic"),
    ("image", "assets/social/post-po-cyberpunk.png",
     "Wasza miłość w roku 2099 🌆 Styl neon cyberpunk ze zwykłego zdjęcia.\n"
     "👉 pixelpedzel.pl\n\n#cyberpunk #neon #obraznaplotnie #prezentdlaniego"),
    ("image", "assets/social/post-po-vangogh.png",
     "Wasza miłość jak dzieło Van Gogha 🎨 Wzruszający prezent na rocznicę ślubu.\n"
     "👉 pixelpedzel.pl\n\n#vangogh #rocznicaślubu #prezentdlarodziców #obraznaplotnie"),
    ("image", "assets/social/post-po-witraz.png",
     "Miłość jak witraż ✨ Wasze zdjęcie w stylu mozaiki witrażowej.\n"
     "👉 pixelpedzel.pl\n\n#witraż #obraznaplotnie #sztuka #prezentdlapary"),
    ("image", "assets/social/post-po-wektor-plaza.png",
     "Wasz własny plakat retro 🌊 Nowoczesny styl wektorowy ze zdjęcia.\n"
     "👉 pixelpedzel.pl\n\n#wektor #plakat #obraznaplotnie #prezent"),

    # === FILMY METAMORFOZY (reveal zdjecie -> dzielo) ===
    ("video", "assets/video/tt-metamorfoza-wektor3d.mp4",
     "Zwykłe zdjęcie? A może dzieło sztuki 🎨 Zobacz metamorfozę: jedno zdjęcie, "
     "różne style. Podgląd przed drukiem 👉 pixelpedzel.pl\n\n"
     "#metamorfoza #obraznaplotnie #personalizowanyprezent #prezentdlapary"),
    ("video", "assets/video/tt-metamorfoza-komikslego.mp4",
     "Wasza miłość w kilku odsłonach 💥🧱 Z jednego zdjęcia — pop-art i klocki. "
     "Który styl Wasz? 👉 pixelpedzel.pl\n\n"
     "#metamorfoza #popart #obraznaplotnie #prezentdlapary #pomysłnaprezent"),
    ("video", "assets/video/tt-metamorfoza-plaza.mp4",
     "Zwykłe zdjęcie z wakacji → dzieło na płótnie 🌅 Zobacz metamorfozę i obraz "
     "gotowy na ścianę. Podgląd przed drukiem 👉 pixelpedzel.pl\n\n"
     "#metamorfoza #obraznaplotnie #prezentdlapary #olej #cyberpunk"),
    ("video", "assets/video/tt-metamorfoza-rocznica.mp4",
     "Prezent na rocznicę, który wzruszy 🥹 Zdjęcie rodziców/dziadków zamienione "
     "w dzieło na płótnie. Zobacz metamorfozę 👉 pixelpedzel.pl\n\n"
     "#prezentnarocznice #prezentdladziadków #vangogh #obraznaplotnie #metamorfoza"),
    ("video", "assets/video/tt-style-grid-plaza.mp4",
     "Jedno zdjęcie — cztery style 🎨 Olej, witraż, wektor, cyberpunk. "
     "Który wybierasz? Napisz w komentarzu 👇 pixelpedzel.pl\n\n"
     "#obraznaplotnie #metamorfoza #prezentdlapary #personalizowanyprezent"),
    ("video", "assets/video/tt-metamorfoza-witraz.mp4",
     "Ze zwykłego zdjęcia — witraż i grafika ✨ Zobacz, jak Wasze zdjęcie staje się "
     "obrazem na płótnie 👉 pixelpedzel.pl\n\n"
     "#metamorfoza #witraż #obraznaplotnie #prezentdlapary #sztuka"),
    ("video", "assets/video/tt-na-prezent.mp4",
     "Nie wiesz, co kupić? 🎁 Obraz ze zdjęcia to prezent na rocznicę, urodziny, "
     "Dzień Matki czy święta — który zostaje na lata.\n👉 pixelpedzel.pl\n\n"
     "#pomysłnaprezent #prezent #obraznaplotnie #prezentdlaniej #prezentdlaniego"),
    ("video", "assets/video/tt-na-scianie.mp4",
     "Tak Wasz obraz wygląda naprawdę na ścianie 🖼️ Prawdziwy wydruk na płótnie, "
     "gotowy do powieszenia.\n👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #dekoracjawnętrz #wystrójwnętrz #homedecor #prezent"),

    # 1. Pamiatka (emocja) — grafika
    ("image", "assets/social/post-pamiatka.png",
     "Za rok, za dziesięć lat — to zdjęcie wciąż będzie wisiało na ścianie. 🤍\n"
     "Niektóre chwile zasługują na coś więcej niż ekran telefonu.\n"
     "Zamień je w obraz na płótnie 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #pamiątka #personalizowanyprezent #dekoracjawnętrz"),

    # 2. Recenzja rocznica — wideo
    ("video", "assets/video/tt-recenzja-rocznica.mp4",
     "Prezent na rocznicę, przy którym mąż się popłakał ❤️\n"
     "Wasze wspólne zdjęcie → obraz olejny na płótnie. Podgląd przed drukiem.\n"
     "Kod START20 = −20% 👉 pixelpedzel.pl\n\n"
     "#prezentnarocznice #obraznaplotnie #prezentdlapary #pomysłnaprezent"),

    # 3. Kocham bez slow — grafika
    ("image", "assets/social/post-kocham.png",
     "Czasem „kocham Cię” mówi się bez słów — obrazem z Waszego wspólnego zdjęcia. 🤍\n"
     "Ręcznie dopracowany, na płótnie premium 👉 pixelpedzel.pl\n\n"
     "#prezentdlapary #walentynki #obraznaplotnie #handmadepl"),

    # 4. Zareczyny — grafika
    ("image", "assets/social/post-zareczyny.png",
     "Powiedzieliście sobie „tak”. 💍 Zatrzymajcie ten moment na płótnie.\n"
     "Zobaczysz projekt przed drukiem — płacisz, gdy Ci się spodoba.\n"
     "👉 pixelpedzel.pl\n\n#zaręczyny #ślub2026 #prezentślubny #obraznaplotnie"),

    # 5. Recenzja mama — wideo
    ("video", "assets/video/tt-recenzja-mama.mp4",
     "Prezent dla Mamy, który ją wzruszy 🥹\n"
     "Wasze wspólne zdjęcie jako delikatna akwarela na płótnie. Zamów z wyprzedzeniem.\n"
     "👉 pixelpedzel.pl\n\n#prezentdlamamy #dzieńmatki #prezent #obraznaplotnie"),

    # 6. Wasza historia — grafika
    ("image", "assets/social/post-historia.png",
     "Wasza historia zasługuje na ścianę. 🖼️\n"
     "Nie kolejny plakat ze sklepu — Wasz obraz, jakiego nikt inny nie ma.\n"
     "👉 pixelpedzel.pl\n\n#dekoracjawnętrz #obraznaplotnie #wystrójwnętrz #homedecor"),

    # 7. Recenzja zareczyny — wideo
    ("video", "assets/video/tt-recenzja-zareczyny.mp4",
     "Zamówione w sobotę, podgląd w poniedziałek, na ścianie w tydzień 😍\n"
     "Jedno zdjęcie zamieniam w obraz. Płacisz, gdy Ci się spodoba.\n"
     "👉 pixelpedzel.pl\n\n#zaręczyny #ślub2026 #obraznaplotnie #handmadepl"),

    # 8. Dom z dusza — grafika
    ("image", "assets/social/post-dom.png",
     "Dom, który opowiada Waszą historię. 🏡\n"
     "Obrazy z Waszych zdjęć — Wy wybieracie chwile, my tworzymy dzieło.\n"
     "👉 pixelpedzel.pl\n\n#dekoracjawnętrz #homedecor #obraznaplotnie #wnętrza"),

    # 9. Recenzja van gogh — wideo
    ("video", "assets/video/tt-recenzja-vangogh.mp4",
     "„Myślałem, że AI zepsuje twarze” — a wyszło lepiej niż na zdjęciu 🎨\n"
     "Twoje zdjęcie w stylu Van Gogha na płótnie 👉 pixelpedzel.pl\n\n"
     "#vangogh #sztuka #dekoracjawnętrz #obraznaplotnie"),

    # 10. Wybor stylu — grafika
    ("image", "assets/social/post-styl.png",
     "Zwykłe zdjęcie? A może dzieło sztuki. 🎨\n"
     "17 stylów do wyboru (olej, Van Gogh, akwarela, szkic…). Podgląd przed drukiem.\n"
     "👉 pixelpedzel.pl\n\n#obraznaplotnie #aiart #personalizowanyprezent"),

    # 11. Bez ryzyka (gwarancja) — mockup
    ("image", "assets/mockups/olej-klasyczny.png",
     "Boisz się, że wyjdzie kicz? U mnie zobaczysz projekt PRZED drukiem i poprawiam "
     "do skutku. Płacisz dopiero, gdy Ci się spodoba. Zero ryzyka. 🤝\n"
     "👉 pixelpedzel.pl\n\n#obraznaplotnie #prezent #handmadepl"),

    # 12. Polecenia — mockup
    ("image", "assets/mockups/komiks.png",
     "Zadowolony/a z obrazu? Poleć znajomemu: on ma −15%, a Ty 25 zł za polecenie. 🤝\n"
     "👉 pixelpedzel.pl\n\n#programpolecen #obraznaplotnie #prezent"),
]
