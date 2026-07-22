import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_compare_video import frame, wall_scene, cta, grid_scene, build
U="assets/uploads"
# Film A: format SIATKA — 1 zdjecie, 4 style (mloda para)
build("tt-style-grid-plaza",
  [ frame(f"{U}/para3-przed.jpg","1 zdjęcie · 4 style","PRZED", hook="Jedno zdjęcie."),
    grid_scene([f"{U}/para3-olej-clean.png", f"{U}/para3-witraz-clean.png",
                f"{U}/para3-wektor-clean.png", f"{U}/para3-cyberpunk-clean.png"]),
    wall_scene(f"{U}/para3-cyberpunk-clean.png"),
    cta() ],
  [2.4, 3.6, 2.6, 3.0], ["fade","fade","fade"])
# Film B: reveal witraz -> wektor (mloda para) + na plotnie
build("tt-metamorfoza-witraz",
  [ frame(f"{U}/para3-przed.jpg","1 zdjęcie, różne style","PRZED", hook="Zwykłe zdjęcie?"),
    frame(f"{U}/para3-witraz-clean.png",None,"PO · WITRAŻ"),
    frame(f"{U}/para3-wektor-clean.png",None,"PO · WEKTOR"),
    wall_scene(f"{U}/para3-witraz-clean.png"),
    cta() ],
  [2.3,2.2,2.2,2.6,3.0], ["wipeleft","wipeleft","fade","fade"])
