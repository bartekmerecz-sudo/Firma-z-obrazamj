"""Biblioteka tresci PixelPedzel — posty + przypisane pliki (zdjecia/wideo).
Z tego generujemy harmonogram (queue.json). Edytuj tu teksty, gdy chcesz zmienic.

Kazdy wpis: (typ, plik, tekst) albo (typ, plik, tekst, okno)
  typ:  "image" albo "video"
  plik: sciezka w repo (bedzie serwowana z SITE_BASE_URL, np. pixelpedzel.pl)
  okno: ("RRRR-MM-DD", "RRRR-MM-DD") — przedzial, poza ktorym post NIE wchodzi
        do rotacji. Potrzebne, bo post o terminie zamowien na swieta wypuszczony
        we wrzesniu jest bez sensu, a post o powrocie z wakacji w grudniu tym
        bardziej. Bez tego pola post leci caly rok.

Zasada: sprzedajemy EMOCJE i MOMENT, nie produkt. Rotacja: grafika emocjonalna -> wideo.
"""

POSTS = [
    # === POSTY SPRZEDAZOWE (PRIORYTET — ida jako pierwsze) ==================
    # Dotychczasowe posty pokazywaly STYLE. Te zdejmuja obiekcje i daja powod,
    # zeby napisac DZIS. Firma bez klientow potrzebuje najpierw tych.
    # post-oferta-start.png wycofany 22.09. Obiecywal znizke dla "5 pierwszych
    # osob", a kampania startowa mowi o "pierwszych trzech obrazach za pol ceny"
    # i post o zwierzakach o "pierwszych trzech zwierzakach". Trzy rozne
    # obietnice naraz to nie oferta, tylko halas — klient, ktory zobaczy dwie,
    # przestaje wierzyc w obie. Grafika zostaje w repo, gdyby wrocila.
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
     "#wakacje2026 #obraznaplotnie #pamiątka #dekoracjawnętrz",
     ("2026-06-15", "2026-09-30")),
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


    # 6. Wasza historia — grafika
    ("image", "assets/social/post-historia.png",
     "Wasza historia zasługuje na ścianę. 🖼️\n"
     "Nie kolejny plakat ze sklepu — Wasz obraz, jakiego nikt inny nie ma.\n"
     "👉 pixelpedzel.pl\n\n#dekoracjawnętrz #obraznaplotnie #wystrójwnętrz #homedecor"),


    # 8. Dom z dusza — grafika
    ("image", "assets/social/post-dom.png",
     "Dom, który opowiada Waszą historię. 🏡\n"
     "Obrazy z Waszych zdjęć — Wy wybieracie chwile, my tworzymy dzieło.\n"
     "👉 pixelpedzel.pl\n\n#dekoracjawnętrz #homedecor #obraznaplotnie #wnętrza"),


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

    # === SERIA reel-* (metamorfozy zdjecie -> obraz) ========================
    # Te same pliki ida na TikToka, ale tam BEZ linku w opisie. Tu link zostaje,
    # bo na Facebooku to normalny post firmowy, a nie material w feedzie FYP.
    ("video", "assets/video/reel-lata-razem.mp4",
     "Tyle lat razem — i ani jednego wspólnego zdjęcia na ścianie.\n\n"
     "Najczęściej słyszę to od dzieci, które szukają prezentu dla rodziców "
     "albo dziadków. Zdjęcia są, tylko wszystkie zostały w telefonie.\n\n"
     "Wyślij jedno, resztę zrobię ja 👉 pixelpedzel.pl\n\n"
     "#prezentdlarodzicow #obraznaplotnie #rocznica #personalizowanyprezent"),
    ("video", "assets/video/reel-zostalo-w-telefonie.mp4",
     "To zdjęcie leżało w telefonie dwa lata.\n\n"
     "Tak kończy się większość naszych najlepszych zdjęć — przewijamy je raz "
     "w roku i lecimy dalej. A wystarczy jedno, żeby zawisło na ścianie.\n\n"
     "Projekt pokazuję przed drukiem 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #wspomnienia #personalizowanyprezent #prezent"),
    ("video", "assets/video/reel-ktory-styl.mp4",
     "Jedno zdjęcie, cztery style. Który wybieracie — 1, 2, 3 czy 4? 👇\n\n"
     "Serio jestem ciekaw, bo mnie osobiście najbardziej podoba się witraż, "
     "a klienci prawie zawsze wybierają olej.\n\n"
     "#ankieta #obraznaplotnie #ktorystyl #personalizowanyprezent"),
    ("video", "assets/video/reel-prezent-klocki.mp4",
     "Zrobiłem im obraz z klocków — miny bezcenne. 🧱\n\n"
     "Ten styl działa wszędzie tam, gdzie klasyczny obraz byłby za poważny: "
     "urodziny, prezent dla dzieciaka, rocznica z przymrużeniem oka.\n\n"
     "👉 pixelpedzel.pl\n\n#prezent #klocki #obraznaplotnie #personalizowanyprezent"),
    ("video", "assets/video/reel-witraz.mp4",
     "Nie sądziłem, że wyjdzie z tego witraż.\n\n"
     "To chyba najbardziej niedoceniany styl w całej ofercie — na płótnie "
     "wygląda jak szkło, a w słońcu naprawdę gra kolorami.\n\n"
     "👉 pixelpedzel.pl\n\n#witraz #obraznaplotnie #dekoracjawnetrz #prezent"),
    ("video", "assets/video/reel-jak-z-bajki.mp4",
     "Zwykłe zdjęcie z sesji → kadr jak z animacji.\n\n"
     "Ten styl najczęściej wybierają młode pary i rodzice małych dzieci. "
     "Ciepły, kolorowy i nie nudzi się po miesiącu.\n\n"
     "👉 pixelpedzel.pl\n\n#bajkowy3d #obraznaplotnie #prezent #personalizowanyprezent"),
    ("video", "assets/video/reel-szkic-pamiatka.mp4",
     "Zdjęcie sprzed lat. Ołówkiem.\n\n"
     "Szkic wybaczy sporo — stare, ziarniste, lekko poruszone zdjęcie po "
     "przerobieniu wygląda jak celowy zabieg, a nie wada.\n\n"
     "Masz takie w albumie? 👉 pixelpedzel.pl\n\n"
     "#szkic #obraznaplotnie #pamiatka #prezentdlarodzicow"),
    ("video", "assets/video/reel-cyberpunk.mp4",
     "Ze zdjęcia z plaży do neonowego miasta.\n\n"
     "Najmocniejszy kontrast w całej ofercie i zdecydowanie najczęstszy wybór "
     "przy prezentach dla nastolatków i fanów sci-fi.\n\n"
     "👉 pixelpedzel.pl\n\n#cyberpunk #obraznaplotnie #prezent #sciencefiction"),

    # === SERIA reel-* DRUGA PARTIA (obiekcje, poradniki, okazje) ============
    ("video", "assets/video/reel-a-jak-sie-nie-spodoba.mp4",
     "„A jak mi się nie spodoba?” — pytacie o to najczęściej, więc odpowiadam raz a dobrze.\n\n"
     "Wysyłasz zdjęcie → przygotowuję projekt → pokazuję Ci go.\n"
     "Nie spodoba się? Nie płacisz i się rozchodzimy.\n\n"
     "Całe ryzyko jest po mojej stronie 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #bezryzyka #personalizowanyprezent #prezent"),
    ("video", "assets/video/reel-jakie-zdjecie.mp4",
     "Zanim wyślesz zdjęcie — trzy rzeczy, które decydują o efekcie:\n\n"
     "1. Ostrość (rozmyte nie da się uratować)\n"
     "2. Światło — dzienne bije każde inne\n"
     "3. Twarze dobrze widoczne, nie pod światło\n\n"
     "Reszta to moja robota 👉 pixelpedzel.pl\n\n"
     "#poradnik #obraznaplotnie #jakiezdjecie #personalizowanyprezent"),
    ("video", "assets/video/reel-stare-zdjecie.mp4",
     "Zdjęcia z albumu zostają w albumie. Szkoda.\n\n"
     "Stare, ziarniste, lekko poruszone — akurat takie świetnie wychodzą "
     "w szkicu ołówkiem. To, co w zdjęciu jest wadą, tam wygląda na zamysł.\n\n"
     "Zajrzyj do szuflady 👉 pixelpedzel.pl\n\n"
     "#pamiatkarodzinna #szkic #prezentdlarodzicow #obraznaplotnie"),
    ("video", "assets/video/reel-plakat-vs-obraz.mp4",
     "Plakat z sieciówki wisi u trzech Twoich znajomych.\n\n"
     "Obraz z Waszego zdjęcia nie wisi u nikogo — bo takiego zdjęcia "
     "nie ma nikt inny.\n\n"
     "Który styl wybieracie 👉 pixelpedzel.pl\n\n"
     "#dekoracjawnetrz #obraznaplotnie #wystrojwnetrz #homedecor"),
    ("video", "assets/video/reel-do-jakiego-wnetrza.mp4",
     "Ściągawka: jaki styl do jakiego wnętrza?\n\n"
     "Salon → olej albo Van Gogh (ciepłe, klasyczne)\n"
     "Biuro → wektor (czysty, graficzny)\n"
     "Pokój nastolatka → cyberpunk\n"
     "Sypialnia → akwarela, pastel\n\n"
     "Nie wiesz? Opisz ścianę w komentarzu, podpowiem 👉 pixelpedzel.pl\n\n"
     "#dekoracjawnetrz #obrazdosalonu #wystrojwnetrz #homedecor"),
    ("video", "assets/video/reel-proces.mp4",
     "Co się dzieje po wysłaniu zdjęcia?\n\n"
     "Siadam do niego sam — dobieram styl, poprawiam kadr, dopracowuję twarze. "
     "Potem pokazuję Ci projekt i dopiero po Twojej akceptacji idzie do druku.\n\n"
     "Bez automatu i bez niespodzianek 👉 pixelpedzel.pl\n\n"
     "#zakulisami #obraznaplotnie #rekodzielo #personalizowanyprezent"),
    ("video", "assets/video/reel-urodziny.mp4",
     "Urodziny za tydzień. Znowu perfumy? 🎁\n\n"
     "Obraz z ich własnego zdjęcia kosztuje tyle co porządny prezent, "
     "a zostaje na ścianie, a nie na półce w łazience.\n\n"
     "Zdążę, jak napiszesz dziś 👉 pixelpedzel.pl\n\n"
     "#urodziny #pomyslnaprezent #prezent #obraznaplotnie"),
    ("video", "assets/video/reel-ile-kosztuje.mp4",
     "„Pewnie kosztuje majątek.” — najczęstsze założenie, więc mówię wprost:\n\n"
     "30×40 — 129 zł · 40×50 — 169 zł · 50×70 — 229 zł · 60×90 — 299 zł\n\n"
     "Tyle, co kolacja we dwoje. Tylko że zostaje na lata.\n"
     "Projekt i podgląd gratis 👉 pixelpedzel.pl\n\n"
     "#cennik #obraznaplotnie #prezent #personalizowanyprezent"),

    # === SERIA bold-* (szybkie ciecia, napisy slowo po slowie) =============
    # Inny charakter niz reel-*: krotsze, ostrzejsze, bez eleganckiego serifu.
    ("video", "assets/video/bold-ile-lat.mp4",
     "Ile lat jesteście razem? I ile Waszych wspólnych zdjęć wisi na ścianie?\n\n"
     "Właśnie. Wyślijcie mi jedno — zrobię z niego obraz na płótnie.\n"
     "Projekt pokazuję przed drukiem 👉 pixelpedzel.pl\n\n"
     "#rocznica #obraznaplotnie #prezentdlarodzicow #pamiatkarodzinna"),
    ("video", "assets/video/bold-telefon.mp4",
     "Masz w telefonie cztery tysiące zdjęć. Ile z nich jeszcze kiedyś obejrzysz?\n\n"
     "Wybierz jedno. Reszta to moja robota.\n"
     "👉 pixelpedzel.pl\n\n"
     "#obrazzezdjecia #wspomnienia #obraznaplotnie #personalizowanyprezent"),
    ("video", "assets/video/bold-prezent.mp4",
     "Perfumy się skończą. Świeca zgaśnie. Bon przepadnie.\n\n"
     "Obraz z Waszego zdjęcia zostaje na ścianie — na lata.\n"
     "👉 pixelpedzel.pl\n\n"
     "#pomyslnaprezent #prezent #obraznaplotnie #personalizowanyprezent"),
    ("video", "assets/video/bold-nie-placisz.mp4",
     "Wysyłasz zdjęcie. Robię projekt. Pokazuję Ci go.\n\n"
     "Nie spodoba się? Nie płacisz ani złotówki. Całe ryzyko po mojej stronie.\n"
     "👉 pixelpedzel.pl\n\n"
     "#bezryzyka #obraznaplotnie #prezent #personalizowanyprezent"),
    ("video", "assets/video/bold-ktory.mp4",
     "Jeden, dwa, trzy czy cztery? Napiszcie numer w komentarzu 👇\n\n"
     "To jedno i to samo zdjęcie w czterech stylach. Ciekawy, co wygra.\n\n"
     "#ktorywybierasz #obraznaplotnie #sztuka #ankieta"),
    ("video", "assets/video/bold-babcia.mp4",
     "Dziadkowie mają wszystko i niczego nie potrzebują. Poza jednym.\n\n"
     "Sobą — na ścianie. Ich wspólne zdjęcie jako obraz na płótnie.\n"
     "👉 pixelpedzel.pl\n\n"
     "#prezentdladziadkow #pamiatkarodzinna #obraznaplotnie #prezent"),

    # === PARTIA JESIENNA (tools/gen_posty_jesien.py) =======================
    # Kolejka nie mowila dotad czterech rzeczy, ktore decyduja o zamowieniu:
    # ktore zdjecie sie nada, kto to robi, co przychodzi kurierem i do kiedy
    # trzeba zamowic na swieta.
    ("image", "assets/social/post-ktore-zdjecie.png",
     "„Chyba mam za słabe zdjęcie.” — na tym najczęściej urywa się rozmowa. "
     "Więc mówię wprost, co się nadaje:\n\n"
     "• zwykłe, z telefonu — wystarczy\n"
     "• twarze wyraźne, nie z drugiego końca plaży\n"
     "• ostre — rozmazanego nie naprawię\n"
     "• im większy plik, tym lepiej\n\n"
     "Odpada właściwie tylko jedno: zrzut ekranu z Instagrama albo zdjęcie zdjęcia.\n\n"
     "Nie wiesz, czy Twoje się nada? Wyślij — sprawdzę i powiem szczerze, "
     "zanim cokolwiek zamówisz 👉 pixelpedzel.pl\n\n"
     "#obrazzezdjecia #obraznaplotnie #poradnik #personalizowanyprezent"),
    ("image", "assets/social/post-kto-to-robi.png",
     "Za PixelPędzlem nie stoi firma. Stoję ja. 🤍\n\n"
     "Jedna osoba, Pabianice. Sam odbieram wiadomości, sam robię projekt, "
     "sam pakuję paczkę.\n\n"
     "Dlatego odpisuję tego samego dnia — i dlatego nie przyjmuję stu zamówień naraz.\n"
     "Jak coś jest nie tak, piszecie do mnie, nie do infolinii 👉 pixelpedzel.pl\n\n"
     "#lokalnybiznes #pabianice #handmadepl #obraznaplotnie"),
    ("image", "assets/social/post-co-dostajesz.png",
     "Co właściwie przychodzi kurierem? Bo to nie jest plik do druku.\n\n"
     "• płótno naciągnięte na drewniany blejtram\n"
     "• boki zadrukowane — wygląda z każdej strony, nie tylko z przodu\n"
     "• zawieszka z tyłu, gotowa na gwóźdź\n"
     "• zapakowane tak, żeby przeżyło kuriera\n\n"
     "Wyjmujesz z kartonu i wieszasz. Nic nie trzeba dokupować 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #dekoracjawnetrz #prezent #personalizowanyprezent"),
    ("image", "assets/social/post-pies.png",
     "Psa też zrobię. Kota też. 🐶\n\n"
     "Olej, szkic, komiks, klocki — każdy styl działa tak samo jak na portrecie.\n\n"
     "I uczciwie: nie mam jeszcze ani jednego zwierzaka w portfolio. "
     "Dlatego pierwsze trzy robię za pół ceny — w zamian proszę o zdjęcie "
     "gotowego obrazu na Waszej ścianie.\n\n"
     "Napiszcie PIES albo KOT w komentarzu 👇\n\n"
     "#portretpsa #pies #kot #obraznaplotnie #prezentdlamilosnikazwierzat"),
    ("image", "assets/social/post-ile-trwa.png",
     "„Ile to trwa?” — od zdjęcia do ściany zwykle 3–7 dni roboczych:\n\n"
     "24 h — pokazuję projekt\n"
     "1–2 dni — poprawki, jeśli trzeba\n"
     "2–4 dni — druk i wysyłka\n\n"
     "Zegar rusza, gdy przyjdzie zdjęcie. Nie wcześniej 👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #prezent #personalizowanyprezent #szybkarealizacja"),
    ("image", "assets/social/post-dwa-obrazy.png",
     "Jeden duży obraz czy dwa mniejsze? Dwa mniejsze robią ze ściany galerię.\n\n"
     "Dwa razy 30×40 to 258 zł — i dostawa wtedy gratis (od 250 zł).\n"
     "Możecie dać jedno zdjęcie w dwóch stylach albo dwa różne zdjęcia obok siebie.\n\n"
     "Nie wiecie, co lepiej zagra na Waszej ścianie? Opiszcie ją w komentarzu, "
     "podpowiem 👉 pixelpedzel.pl\n\n"
     "#dekoracjawnetrz #galeriascian #obraznaplotnie #homedecor"),
    ("image", "assets/social/post-rocznica.png",
     "Zdjęcie ze ślubu leży w pudełku od dwudziestu lat. 🤍\n\n"
     "Zeskanujcie je telefonem i wyślijcie — odtworzę je jako obraz na płótnie. "
     "Tym razem na ścianie, nie w szafie.\n\n"
     "Stare, pożółkłe i podniszczone też przyjmuję — od tego są poprawki.\n"
     "Projekt pokazuję przed drukiem 👉 pixelpedzel.pl\n\n"
     "#rocznicaslubu #pamiatkarodzinna #prezentdlarodzicow #obraznaplotnie"),
    ("image", "assets/social/post-swieta-termin.png",
     "Święta: zamówienia przyjmuję do 12 grudnia. ⏳\n\n"
     "Później nie zdążę zrobić projektu, przyjąć poprawek i wydrukować przed Wigilią. "
     "Wolę powiedzieć to teraz, niż obiecać i nie dowieźć.\n\n"
     "Grudzień to jedyny miesiąc, w którym zamykam listę wcześniej.\n"
     "Napiszcie ŚWIĘTA w komentarzu albo w wiadomości 👉 pixelpedzel.pl\n\n"
     "#prezentnaswieta #swieta2026 #obraznaplotnie #personalizowanyprezent",
     ("2026-11-03", "2026-12-12")),

    # === KAMPANIA "PIERWSZY KLIENT" (tools/gen_posty_start.py) =============
    # Ida jako pierwsze w rotacji. Wszystkie trzy koncza sie jednym slowem do
    # napisania w komentarzu — latwiej odpowiedziec jednym slowem niz ulozyc
    # zdanie, a kazdy komentarz podbija zasieg postu.
    ("image", "assets/social/post-darmowy-projekt.png",
     "Wyślij mi zdjęcie rano — projekt zobaczysz jeszcze tego samego dnia. 🤍\n\n"
     "Za darmo. Bez zamówienia, bez zaliczki, bez zobowiązania.\n"
     "Spodoba się — drukuję na płótnie. Nie spodoba się — rozchodzimy się "
     "i nie płacisz ani złotówki.\n\n"
     "Napiszcie PROJEKT w komentarzu albo w wiadomości 👉 pixelpedzel.pl\n\n"
     "#obrazzezdjecia #obraznaplotnie #bezryzyka #personalizowanyprezent"),
    ("image", "assets/social/post-pabianice.png",
     "Jestem z Pabianic. Nie z hurtowni, nie z drugiego końca Polski. 📍\n\n"
     "Dla Was z okolicy to znaczy tyle:\n"
     "• odbiór osobisty, bez kuriera i czekania na paczkę\n"
     "• obraz oglądacie na żywo, zanim za niego zapłacicie\n"
     "• Łódź i okolice — dowiozę sam\n\n"
     "Prezent na ostatnią chwilę? Lokalnie da się zdążyć tam, gdzie kurier już nie.\n"
     "Piszcie 👉 pixelpedzel.pl\n\n"
     "#pabianice #łódź #lokalnie #obraznaplotnie #prezent"),
    ("image", "assets/social/post-pierwszy-klient.png",
     "Szczerze: nikt u mnie jeszcze nie zamówił.\n\n"
     "Ruszyłem niedawno i nie mam się czym pochwalić — poza tym, co zrobiłem sam. "
     "Nie będę udawał dorobku, którego nie mam.\n\n"
     "Więc proponuję układ: **pierwsze trzy obrazy robię za pół ceny.** "
     "W zamian proszę o zdjęcie gotowego obrazu na Waszej ścianie i szczerą opinię — "
     "także jeśli wyjdzie kiepsko.\n\n"
     "Ktoś musi być pierwszy. Napiszcie PIERWSZY 👇\n\n"
     "#nowafirma #handmadepl #obraznaplotnie #wspierampolskiemarki"),

    # === ZIMA I PRZEDWIOSNIE 2027 (tools/gen_posty_zima.py) ================
    # Kolejka konczyla sie 31 grudnia, a zaraz po swietach wypadaja dwie
    # najlepsze okazje w roku dla obrazu ze zdjecia: Dzien Babci i Dziadka
    # oraz Walentynki. Okno zaczyna sie DWA TYGODNIE przed data — przy
    # realizacji 3-7 dni roboczych plus wysylka ktos, kto zobaczy post
    # dwa dni wczesniej, juz nie zdazy.
    ("image", "assets/social/post-po-swietach.png",
     "Ile z tegorocznych prezentów jeszcze pamiętacie?\n\n"
     "Świeca się wypaliła, czekolada zniknęła, skarpetki poszły do szuflady.\n"
     "Obraz z Waszego zdjęcia wisiałby dalej.\n\n"
     "W styczniu nie ma kolejki — realizuję od ręki. Projekt pokazuję "
     "przed drukiem 👉 pixelpedzel.pl\n\n"
     "#poswietach #obraznaplotnie #prezent #personalizowanyprezent",
     ("2026-12-27", "2027-01-20")),
    ("image", "assets/social/post-nowy-rok.png",
     "Pusta ściana to nie minimalizm. To zwykle odkładanie na potem. 🤍\n\n"
     "Zdjęcie macie od dawna — leży w telefonie razem z czterema tysiącami innych. "
     "Brakuje tylko jednej decyzji.\n\n"
     "Wyślijcie jedno, resztę zrobię ja 👉 pixelpedzel.pl\n\n"
     "#nowyrok #postanowienia #dekoracjawnetrz #obraznaplotnie",
     ("2026-12-28", "2027-01-25")),
    ("image", "assets/social/post-dzien-babci.png",
     "Dzień Babci i Dziadka — 21 i 22 stycznia. 🤍\n\n"
     "Dziadkowie mają wszystko i niczego nie potrzebują. Poza jednym: sobą na ścianie.\n\n"
     "Stare zdjęcie ślubne, wakacje sprzed lat, Wy razem z nimi — zrobię z tego "
     "obraz na płótnie. Pożółkłe i podniszczone też przyjmuję.\n\n"
     "Zamówcie do 14 stycznia, żeby zdążyć 👉 pixelpedzel.pl\n\n"
     "#dzienbabci #dziendziadka #prezentdladziadkow #pamiatkarodzinna",
     ("2027-01-05", "2027-01-21")),
    ("image", "assets/social/post-zimowe-wieczory.png",
     "Ciemno o 16:00, a ściana pusta od lat.\n\n"
     "Jedno zdjęcie z telefonu wystarczy. Projekt pokazuję, zanim cokolwiek "
     "zapłacicie. Od zdjęcia do ściany 3–7 dni.\n\n"
     "Zimą i tak siedzicie w domu — niech będzie na co patrzeć 👉 pixelpedzel.pl\n\n"
     "#zima #dekoracjawnetrz #obraznaplotnie #homedecor",
     ("2027-01-01", "2027-01-31")),
    ("image", "assets/social/post-walentynki.png",
     "Walentynki: Wasze zdjęcie, nie kolejna maskotka. ❤️\n\n"
     "Jedno wspólne zdjęcie jako obraz na płótnie. Projekt pokazuję przed drukiem — "
     "nie spodoba się, nie płacicie.\n\n"
     "Zamówcie do 6 lutego, żeby zdążyć na czas 👉 pixelpedzel.pl\n\n"
     "#walentynki #prezentdlaniej #prezentdlaniego #obraznaplotnie",
     ("2027-01-28", "2027-02-13")),
    ("image", "assets/social/post-dzien-kobiet.png",
     "8 marca: kwiaty zwiędną do piątku. 🌷\n\n"
     "Obraz z Waszego wspólnego zdjęcia zostanie. Mama, żona, siostra, babcia — "
     "każda z nich ma zdjęcie, które zasługuje na ścianę, a nie na kartę pamięci.\n\n"
     "Zamówcie do 1 marca 👉 pixelpedzel.pl\n\n"
     "#dzienkobiet #8marca #prezentdlaniej #obraznaplotnie",
     ("2027-02-20", "2027-03-07")),

    # === REELSY: KAMPANIA I SEZONY (tools/gen_reels4.py) ===================
    # Wideo dowozi wyrazniej lepszy zasieg niz grafiki, wiec kolejka idzie
    # teraz jeden do jednego i trzeba czym ja wypelnic. Zaden z tych filmow
    # nie jest kolejnym "o stylach" — kazdy ma za soba obietnice albo date.
    ("video", "assets/video/bold-projekt-dzis.mp4",
     "Wyślij zdjęcie rano — projekt zobaczysz wieczorem. Za darmo, bez zaliczki.\n\n"
     "Nie spodoba się? Nie płacisz ani złotówki i się rozchodzimy.\n"
     "Napisz PROJEKT 👉 pixelpedzel.pl\n\n"
     "#obrazzezdjecia #bezryzyka #obraznaplotnie #personalizowanyprezent"),
    ("video", "assets/video/bold-pabianice.mp4",
     "Jestem z Pabianic. Nie z hurtowni.\n\n"
     "Odbiór osobisty, obraz oglądasz na żywo, zanim za niego zapłacisz. "
     "Łódź i okolice — dowiozę sam.\n"
     "👉 pixelpedzel.pl\n\n"
     "#pabianice #łódź #lokalnie #obraznaplotnie"),
    ("video", "assets/video/bold-pierwszy.mp4",
     "Nikt u mnie jeszcze nie zamówił i nie będę udawał, że jest inaczej.\n\n"
     "Pierwsze trzy obrazy robię za pół ceny — w zamian proszę o zdjęcie "
     "gotowego obrazu na ścianie i szczerą opinię.\n\n"
     "Ktoś musi być pierwszy. Napisz PIERWSZY 👇\n\n"
     "#nowafirma #handmadepl #obraznaplotnie #wspierampolskiemarki"),
    ("video", "assets/video/bold-swieta.mp4",
     "Do świąt zostało mniej, niż myślisz. ⏳\n\n"
     "Zamówienia przyjmuję do 12 grudnia — potem nie zdążę zrobić projektu, "
     "przyjąć poprawek i wydrukować przed Wigilią. Wolę powiedzieć to teraz.\n"
     "👉 pixelpedzel.pl\n\n"
     "#prezentnaswieta #swieta2026 #obraznaplotnie",
     ("2026-11-03", "2026-12-12")),
    ("video", "assets/video/bold-walentynki.mp4",
     "Znowu maskotka i pudełko czekoladek? ❤️\n\n"
     "Macie wspólne zdjęcie. Powieście je na ścianie — zrobię z niego obraz "
     "na płótnie. Projekt pokazuję przed drukiem.\n"
     "👉 pixelpedzel.pl\n\n"
     "#walentynki #prezentdlaniej #prezentdlaniego #obraznaplotnie",
     ("2027-01-28", "2027-02-13")),
    ("video", "assets/video/bold-dzien-babci.mp4",
     "Co kupić babci i dziadkowi, skoro mają już wszystko? 🤍\n\n"
     "Poza jednym: sobą na ścianie. Stare zdjęcie ślubne albo Wy razem z nimi — "
     "zrobię z tego obraz na płótnie.\n"
     "Zamów do 14 stycznia 👉 pixelpedzel.pl\n\n"
     "#dzienbabci #dziendziadka #prezentdladziadkow #pamiatkarodzinna",
     ("2027-01-05", "2027-01-21")),
]
