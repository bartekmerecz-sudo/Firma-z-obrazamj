import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_compare import make
U="assets/uploads"
JOBS=[
 (f"{U}/para3-przed.jpg", f"{U}/para3-olej-clean.png",
  "Olejny klasyk", "Wasz zachód słońca — w oleju.", "05", "post-po-olej.png"),
 (f"{U}/para3-przed.jpg", f"{U}/para3-witraz-clean.png",
  "Mozaika witrażowa", "Miłość jak witraż.", "06", "post-po-witraz.png"),
 (f"{U}/para3-przed.jpg", f"{U}/para3-wektor-clean.png",
  "Nowoczesny wektor", "Wasz plakat retro.", "07", "post-po-wektor-plaza.png"),
 (f"{U}/para3-przed.jpg", f"{U}/para3-cyberpunk-clean.png",
  "Neon Cyberpunk", "Wasza miłość w roku 2099.", "08", "post-po-cyberpunk.png"),
 (f"{U}/para4-przed.jpg", f"{U}/para4-szkic-clean.png",
  "Szkic ołówkiem", "Tyle lat, jedna miłość.", "09", "post-po-szkic.png"),
 (f"{U}/para4-przed.jpg", f"{U}/para4-vangogh-clean.png",
  "Gwiaździsty Van Gogh", "Wasza miłość jak dzieło.", "10", "post-po-vangogh.png"),
]
for j in JOBS: make(*j)
