# Guarded

Guarded is the interpreter of Dijkstra's guarded command language,
written in python with ANTLR4 generator.

Example of program in this language:
```
a := 45;
b := 15;

do a != b ->
    if a > b -> a := a - b
    |  a < b -> b := b - a
    fi
od
```

## Quick start:
To start using interpreter, follow these steps:

* Install gclang:
```console
  $ pip install gclang
```

* Launch program of your choice with:
```console
  $ gclang ./examples/euqclid.gua run
  $ gclang ./examples/euqclid.gua derive
```
