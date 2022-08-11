#!/usr/bin/env python3
import itertools, os, re, sys
from hashlib import sha1


CSSLIBS = ('solarized-highlight', 'uikit-2.27.4.min', 'webmention-0.2.0')
JSLIBS = (
    'html5shiv-3.7.2.min',
    'jquery-1.10.2.min',
    'jquery.sticky-kit-1.1.1',
    'lazysizes-4.0.0-rc3.min',
    'lazysizes-4.0.0-rc3.noscript.min',
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


print('Generating CSS bundle')
short_hash = sha1(cat('static/main.css') + ''.join(CSSLIBS).encode()).hexdigest()[:7]
css_bundle_filepath = 'static/bundle-SHORTSHA1-{}.css'.format(short_hash)
files_created = not os.path.exists(css_bundle_filepath)
with open(css_bundle_filepath, 'wb') as bundle:
    for csslib in CSSLIBS:
        bundle.write(cat('static/csslibs/{}.css'.format(csslib)))
    bundle.write(cat('static/main.css'))
sed('templates/base.html', '-SHORTSHA1-[a-z0-9]+.css', '-SHORTSHA1-{}.css'.format(short_hash))

print('Generating JS bundle')
short_hash = sha1(cat('static/js/social.js') + cat('static/js/filter-tags.js') + ''.join(JSLIBS).encode()).hexdigest()[:7]
for SHARE, MG_FILTER_TAGS in itertools.product(range(2), repeat=2):
    js_bundle_filepath = 'static/bundle-SHARE-{}-MG_FILTER_TAGS-{}-SHORTSHA1-{}.js'.format(
            SHARE, MG_FILTER_TAGS, short_hash)
    files_created |= not os.path.exists(js_bundle_filepath)
    with open(js_bundle_filepath, 'wb') as bundle:
        for jslib in JSLIBS:
            bundle.write(cat('static/jslibs/{}.js'.format(jslib)))
        if SHARE:
            bundle.write(cat('static/js/social.js'))
        if MG_FILTER_TAGS:
            bundle.write(cat('static/js/filter-tags.js'))
sed('templates/base.html', '-SHORTSHA1-[a-z0-9]+.js', '-SHORTSHA1-{}.js'.format(short_hash))

if files_created:
    print('New bundle files were created', file=sys.stderr)
    sys.exit(1)
