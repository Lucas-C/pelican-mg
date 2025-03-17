#!/bin/bash

# USAGE: ./run.sh ( install | install_dev | test_ludochaordic )

set -o pipefail -o errexit -o nounset -o xtrace

install () {
    ./gen_statics_bundles.py || true
}

install_dev () {
    npm install -g eslint htmlhint stylelint
    npm install -D eslint eslint-plugin-unicorn @eslint/js @eslint/eslintrc stylelint-config-standard
    pip install html5lib pre-commit
    pre-commit install
}

test_ludochaordic () {
    THEME_DIR=$PWD
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

    $THEME_DIR/gen_imgs_from_mds.py content/*.md
    sed -i '/PLUGINS +=/d' publishconf.py
    invoke publish -- -D
    git checkout HEAD publishconf.py

    # Too many missing img alt attributes in thoses:
    rm output/street-art-and-hedonogeolostism-in-london.html output/variante-2-joueurs-pour-bang-le-jeu-de-des.html

    cp $THEME_DIR/.htmlhintrc output/
    htmlhint output/

    if ! [ -d vnu-runtime-image ]; then
        curl -ROLs https://github.com/validator/validator/releases/download/latest/vnu.linux.zip \
        && unzip vnu.linux.zip \
        && rm vnu.linux.zip \
        && vnu-runtime-image/bin/vnu --version
    fi
    ./vnu-runtime-image/bin/vnu --Werror --filterfile .vnurc output/index.html
    ./vnu-runtime-image/bin/vnu --Werror --filterfile .vnurc output/quelques-sites-web-que-jai-concu.html
    ./vnu-runtime-image/bin/vnu --Werror --filterfile .vnurc output/a-review-of-html-linters.html
}

eval "$1"
