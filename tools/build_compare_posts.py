import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_compare import make
U = "assets/uploads"
JOBS = [
 (f"{U}/para1-przed.jpg", f"{U}/para1-wektor-clean.png",
  "Wektor / minimalizm", "Twoje zdjęcie w nowoczesnym stylu.", "01", "post-po-wektor.png"),
 (f"{U}/para1-przed.jpg", f"{U}/para1-bajka3d-clean.png",
  "Bajkowy 3D", "Wasza historia jak z bajki.", "02", "post-po-bajka3d.png"),
 (f"{U}/para2-przed.jpg", f"{U}/para2-komiks-clean.png",
  "Pop-art / komiks", "Wasza miłość jak z komiksu.", "03", "post-po-komiks.png"),
 (f"{U}/para2-przed.jpg", f"{U}/para2-lego-clean.png",
  "Klockowy świat", "Zbudowani z miłości.", "04", "post-po-lego.png"),
]
for j in JOBS: make(*j)
