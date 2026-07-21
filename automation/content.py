"""Biblioteka tresci PixelPedzel — posty + przypisane pliki (zdjecia/wideo).
Z tego generujemy harmonogram (queue.json). Edytuj tu teksty, gdy chcesz zmienic.

Kazdy wpis: (typ, plik, tekst)
  typ:  "image" albo "video"
  plik: sciezka w repo (bedzie serwowana z SITE_BASE_URL, np. pixelpedzel.pl)

Zasada: sprzedajemy EMOCJE i MOMENT, nie produkt. Rotacja: grafika emocjonalna -> wideo.
"""

POSTS = [
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
