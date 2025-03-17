#!/bin/bash

# USAGE: ./run.sh ( install | install_dev | test_ludochaordic )

set -o pipefail -o errexit -o nounset -o xtrace

install () {
    ./gen_statics_bundles.py || true
}

install_dev () {
    npm install -g eslint htmlhint stylelint
    npm install -D eslint eslint-plugin-unicorn @eslint/js @eslint/eslintrc stylelint-config-standard
    pip install html5lib html5validator pre-commit
    pre-commit install
}

test_ludochaordic () {
    cd ..
    if ! [ -d pelican-plugins ]; then
        git clone https://github.com/getpelican/pelican-plugins.git
        cd pelican-plugins
        git submodule update --init ctags_generator deadlinks image_process representative_image tag_cloud
        cd ..
    fi
    [ -d ludochaordic ] || git clone https://github.com/Lucas-C/ludochaordic.git
    cd ludochaordic
    pip install -r requirements.txt

    ../pelican-mg/gen_imgs_from_mds.py content/*.md
    sed -i '/PLUGINS +=/d' publishconf.py
    invoke publish -- -D
    git checkout HEAD publishconf.py

    # Too many missing img alt attributes in thoses:
    rm output/street-art-and-hedonogeolostism-in-london.html output/variante-2-joueurs-pour-bang-le-jeu-de-des.html

    html5validator --root output/ --ignore-re='.*(Element "eof" not allowed as child of element "p" in this context.|Element "style" not allowed as child of element.*|Text not allowed in element "iframe" in this context.|Attribute "allow" not allowed on element "iframe" at this point.|No "p" element in scope but a "p" end tag seen.|End tag "p" implied, but there were open elements.|Unclosed element "a".|End tag "div" seen, but there were open elements.)' # issue with pelican renderer: <p> contains legally only inline-/inline-block-elements

    cp ../pelican-mg/.htmlhintrc output/
    htmlhint output/
}

eval "$1"
