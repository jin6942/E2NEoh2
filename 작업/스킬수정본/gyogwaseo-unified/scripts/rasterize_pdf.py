import argparse
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('pdf', type=Path)
parser.add_argument('out', type=Path)
parser.add_argument('--scale', type=float, default=1.5)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
document = pdfium.PdfDocument(str(args.pdf))
thumbnails = []
for index in range(len(document)):
    page = document[index]
    bitmap = page.render(scale=args.scale)
    image = bitmap.to_pil().convert('RGB')
    image.save(args.out / f'page-{index+1}.png')
    thumbnail = image.copy()
    thumbnail.thumbnail((300, 425))
    tile = Image.new('RGB', (320, 455), 'white')
    tile.paste(thumbnail, (10, 20))
    ImageDraw.Draw(tile).text((10, 4), str(index+1), fill='black')
    thumbnails.append(tile)
    bitmap.close()
    page.close()
for start in range(0, len(thumbnails), 12):
    batch = thumbnails[start:start+12]
    canvas = Image.new('RGB', (320*4, 455*((len(batch)+3)//4)), '#dddddd')
    for idx, tile in enumerate(batch):
        canvas.paste(tile, ((idx%4)*320, (idx//4)*455))
    canvas.save(args.out / f'contact-{start//12+1}.png')
print(f'Rendered {len(document)} pages to {args.out}')
document.close()
