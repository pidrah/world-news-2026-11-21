# make.fun news-image-20261121 entry: writes the day's image to /output/entry.png.
# The image is held in this repository and copied unchanged; no network is used, and
# two runs write the same bytes.
import shutil, os

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"), os.path.join(out_dir, "entry.png"))
