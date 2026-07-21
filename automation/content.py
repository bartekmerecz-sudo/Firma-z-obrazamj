"""Biblioteka tresci PixelPedzel — posty + przypisane pliki (zdjecia/wideo).
Z tego generujemy harmonogram (queue.json). Edytuj tu teksty, gdy chcesz zmienic.

Kazdy wpis: (typ, plik, tekst)
  typ:  "image" albo "video"
  plik: sciezka w repo (bedzie serwowana z SITE_BASE_URL, np. pixelpedzel.pl)
"""

# Kolejnosc = rotacja na kolejne dni. Mieszamy zdjecia (feed) i wideo (reels).
POSTS = [
    ("image", "assets/mockups/olej-klasyczny.png",
     "Zamien swoje zdjecie w obraz na plotnie! 🎨 Wybierasz styl (olej, Van Gogh, "
     "akwarela, szkic i wiecej), a projekt akceptujesz PRZED drukiem. Na start -20% "
     "kodem START20.\n👉 pixelpedzel.pl\n\n#obraznaplotnie #personalizowanyprezent "
     "#prezent #dekoracjawnetrz #handmadepl"),

    ("video", "assets/video/tt-recenzja-rocznica.mp4",
     "Prezent na rocznice, ktory trafia w serce mocniej niz perfumy ❤️ Wasze wspolne "
     "zdjecie jako obraz olejny na plotnie. Podglad przed drukiem.\n👉 pixelpedzel.pl\n\n"
     "#prezentnarocznice #obraznaplotnie #prezentdlapary #pomyslnaprezent"),

    ("image", "assets/mockups/van-gogh.png",
     "Ktory styl wybierasz? 👇 Olej klasyczny, Van Gogh czy akwarela? Napisz w "
     "komentarzu — pokaze, jak Twoje zdjecie mogloby wygladac!\n\n#sztuka #vangogh "
     "#obraznaplotnie #dekoracjawnetrz"),

    ("video", "assets/video/tt-recenzja-mama.mp4",
     "Pomysl na prezent dla Mamy, ktory ja wzruszy 🥹 Wasze wspolne zdjecie jako "
     "delikatna akwarela na plotnie. Zamow z wyprzedzeniem.\n👉 pixelpedzel.pl\n\n"
     "#prezentdlamamy #dzienmatki #prezent #obraznaplotnie"),

    ("image", "assets/mockups/duo-galeria.png",
     "Pusta sciana w salonie? 🖼️ Zamiast plakatu ze sklepu — obraz z WLASNEGO zdjecia. "
     "Nikt inny takiego nie ma.\n👉 pixelpedzel.pl\n\n#dekoracjawnetrz #obraznaplotnie "
     "#wystrojwnetrz #homedecor"),

    ("image", "assets/bon/bon-przyklad.png",
     "Nie wiesz, jakie zdjecie wybrac na prezent? Podaruj bon podarunkowy PixelPedzel — "
     "obdarowany sam wybierze zdjecie i styl. 🎁\n👉 pixelpedzel.pl\n\n#bonpodarunkowy "
     "#prezent #pomyslnaprezent"),

    ("video", "assets/video/tt-recenzja-zareczyny.mp4",
     "Zareczyny? Uwiecznij je inaczej niz wszyscy 💍 Jedno zdjecie zamieniam w obraz. "
     "Placisz, gdy Ci sie spodoba.\n👉 pixelpedzel.pl\n\n#zareczyny #slub2026 "
     "#prezentslubny #obraznaplotnie"),

    ("image", "assets/mockups/szkic-olowek.png",
     "Boisz sie, ze wyjdzie kicz? U mnie zobaczysz projekt PRZED drukiem i poprawiam "
     "do skutku. Placisz dopiero, gdy Ci sie spodoba. Zero ryzyka.\n👉 pixelpedzel.pl\n\n"
     "#obraznaplotnie #prezent #handmadepl"),

    ("image", "assets/mockups/akwarela.png",
     "Jak zamowic obraz? 1️⃣ Wyslij jedno zdjecie 2️⃣ Wybierz styl 3️⃣ Zaakceptuj projekt "
     "przed drukiem. Prosto i bez ryzyka.\n👉 pixelpedzel.pl\n\n#obraznaplotnie "
     "#personalizowanyprezent #jaktozrobic"),

    ("video", "assets/video/tt-recenzja-vangogh.mp4",
     "„Myslalem, ze AI zepsuje twarze” — a wyszlo lepiej niz na zdjeciu 🎨 Twoje zdjecie "
     "w stylu Van Gogha na plotnie.\n👉 pixelpedzel.pl\n\n#vangogh #sztuka "
     "#dekoracjawnetrz #obraznaplotnie"),

    ("image", "assets/mockups/cyberpunk.png",
     "Niektore chwile chce sie miec na scianie na zawsze. Przeslij jedno zdjecie — "
     "zamienie je w wyjatkowy obraz na plotnie.\n👉 pixelpedzel.pl\n\n#obraznaplotnie "
     "#pamiatka #prezent #cyberpunk"),

    ("image", "assets/mockups/komiks.png",
     "Masz u mnie obraz i jestes zadowolony/a? Polec znajomemu: on ma -15%, a Ty 25 zl "
     "za kazde polecenie. Wszyscy wygrywaja. 🤝\n👉 pixelpedzel.pl\n\n#programpolecen "
     "#obraznaplotnie #prezent"),
]
