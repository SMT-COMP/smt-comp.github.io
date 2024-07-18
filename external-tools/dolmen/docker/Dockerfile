#ocaml/opam:debian-10-ocaml-4.14
FROM ocaml/opam@sha256:6691fa8fe29246f1932c4322f318241cae397cceba1d9d2156e719a71bd3eddb AS stage1

RUN mkdir dolmen

COPY dolmen/*.opam dolmen/

WORKDIR dolmen/

RUN opam-2.1 install . --deps-only --with-test --yes

COPY --chown=opam dolmen/ ./

RUN opam-2.1 exec -- dune --version

ENV DUNE_PROFILE=release

RUN opam-2.1 exec -- make
RUN opam-2.1 exec -- make test
RUN opam-2.1 exec -- dune install --destdir=destdir --prefix=/
RUN cp destdir/bin/dolmen /tmp

FROM scratch AS export-stage
COPY --from=stage1 /tmp/dolmen .
