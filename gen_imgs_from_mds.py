#!/usr/bin/env python3
import html5lib, os, sys
from markdown import markdown

SMALLEST = {}
SMALLEST['gif'] = b'GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\n\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;'
SMALLEST['jpg'] = SMALLEST['jpeg'] = b'\xff\xd8\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xc9\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xcc\x00\x06\x00\x10\x10\x05\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xd2\xcf \xff\xd9'
SMALLEST['png'] = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00:~\x9bU\x00\x00\x00\nIDATx\x9cc\xfa\x0f\x00\x01\x05\x01\x02\xcf\xa0.\xcd\x00\x00\x00\x00IEND\xaeB`\x82'
SMALLEST['svg'] = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
SMALLEST['webp'] = b'RIFF\x1e\x00\x00\x00WEBPVP8L\x11\x00\x00\x00/\x00\x00\x00\x00\x07\xd0\xff\xfe\xf7\xbf\xff\x81\x88\xe8\x7f\x00\x00'

def gen_img(img_url):
    if img_url[0] == '/':
        img_url = img_url[1:]
    if os.path.exists(img_url):
        return
    os.makedirs(os.path.dirname(img_url), exist_ok=True)
    ext = img_url.split('.')[-1].lower()
    with open(img_url, 'wb') as img_file:
        img_file.write(SMALLEST[ext])

def enumerate_imgs(md_file_paths):
    for md_file_path in md_file_paths:
        with open(md_file_path) as md_file:
            md_content = md_file.read()
        html = markdown(md_content)
        doc_root = html5lib.parse(html)
        for img in doc_root.iter('{http://www.w3.org/1999/xhtml}img'):
            img_url = img.attrib['src']
            if img_url.startswith('http'):
                continue
            yield os.path.join('content', img_url)
        # Adding also images from "Image:" pelican metadata entries
        for line in md_content.splitlines()[:6]:
            if not line.startswith('Image: '):
                continue
            yield os.path.join('content', line.replace('Image: ', '').strip())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2 and sys.argv[1] == '--list':
            for img_path in enumerate_imgs(sys.argv[2:]):
                print(img_path)
        else:
            for img_path in enumerate_imgs(sys.argv[1:]):
                gen_img(img_path)
    else:
        print('Checking that pelican plugin image_process.scale works OK on those imgs')
        from PIL import Image
        sys.path.append('../pelican-plugins/image_process/')
        from image_process import scale
        for ext, content in sorted(SMALLEST.items()):
            print('- Testing {} img'.format(ext))
            small_img_filename = 'img.{}'.format(ext)
            with open(small_img_filename, 'wb') as small_img:
                small_img.write(content)
            scale(Image.open(small_img_filename), '300', '300', False, False)  # raise an exception if img.getbbox() returns None
