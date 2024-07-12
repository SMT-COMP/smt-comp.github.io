#!/bin/sh -eu

COMMIT=$1

REPO=docker/dolmen

if [ ! -d $REPO ]; then
    git clone git@github.com:SMT-COMP/dolmen.git $REPO
fi

git -C $REPO fetch

SHA=$(git -C "$REPO" rev-parse "$COMMIT")
echo "building $SHA"

git -C $REPO checkout --detach "$SHA"

docker buildx build --output type=local,dest=binaries/$SHA/ docker --progress plain
