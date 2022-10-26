#!/usr/bin/env python3
import itertools, os, re, sys
from hashlib import sha1


CSSLIBS = ('solarized-highlight', 'uikit-2.27.4.min', 'webmention-0.2.0')
JSLIBS = (
    'html5shiv-3.7.2.min',
    'jquery-1.10.2.min',
    'jquery.sticky-kit-1.1.1',
    'uikit-2.27.4.min',
    'webmention-0.2.0.min',
)


def cat(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def sed(filepath, pattern, value):
    with open(filepath, 'r+') as f:
        data = f.read()
        f.seek(0)
        f.write(re.sub(pattern, value, data))
        f.truncate()

def sizeof_fmt(num, suffix="B"):
    # Recipe from: https://stackoverflow.com/a/1094933/636849
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024
    return f"{num:.1f}Yi{suffix}"


print('Generating CSS bundle')
css_short_hash = sha1(cat('static/main.css') + ''.join(CSSLIBS).encode()).hexdigest()[:7]
css_bundle_filepath = 'static/bundle-SHORTSHA1-{}.css'.format(css_short_hash)
files_created = not os.path.exists(css_bundle_filepath)
with open(css_bundle_filepath, 'wb') as bundle:
    for csslib in CSSLIBS:
        bundle.write(cat('static/csslibs/{}.css'.format(csslib)))
    bundle.write(cat('static/main.css'))
print(f'* {css_bundle_filepath} :', sizeof_fmt(os.stat(css_bundle_filepath).st_size), file=sys.stderr)

print('Generating JS bundles')
js_short_hash = sha1(cat('static/js/social.js') + cat('static/js/filter-tags.js') + ''.join(JSLIBS).encode()).hexdigest()[:7]
for SHARE, MG_FILTER_TAGS in itertools.product(range(2), repeat=2):
    js_bundle_filepath = 'static/bundle-SHARE-{}-MG_FILTER_TAGS-{}-SHORTSHA1-{}.js'.format(
            SHARE, MG_FILTER_TAGS, js_short_hash)
    files_created |= not os.path.exists(js_bundle_filepath)
    with open(js_bundle_filepath, 'wb') as bundle:
        for jslib in JSLIBS:
            bundle.write(cat('static/jslibs/{}.js'.format(jslib)))
        if SHARE:
            bundle.write(cat('static/js/social.js'))
        if MG_FILTER_TAGS:
            bundle.write(cat('static/js/filter-tags.js'))
    print(f'* {js_bundle_filepath} :', sizeof_fmt(os.stat(js_bundle_filepath).st_size), file=sys.stderr)

print('Updating HTML with the correct SHA1 hashes in the CSS/JS bundle paths')
sed('templates/base.html', '-SHORTSHA1-[a-z0-9]+.css', '-SHORTSHA1-{}.css'.format(css_short_hash))
sed('templates/base.html', '-SHORTSHA1-[a-z0-9]+.js', '-SHORTSHA1-{}.js'.format(js_short_hash))
print('* templates/base.html :', sizeof_fmt(os.stat('templates/base.html').st_size), file=sys.stderr)

if files_created:
    print('New bundle files were created', file=sys.stderr)
    sys.exit(1)
