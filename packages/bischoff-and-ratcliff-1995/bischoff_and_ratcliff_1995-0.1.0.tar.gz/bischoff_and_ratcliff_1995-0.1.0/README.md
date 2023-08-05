# Generator of Instances for the Three-Dimensional Single Large Object Placement Problem (SLOPP)

Based on the paper E.E. Bischoff and M.S.W. Ratcliff, "Issues in the development of Approaches to Container Loading", OMEGA, vol.23, no.4, (1995) pp 377-390.

## Usage

```sh
$ pip install -e .
(...) pip install log stuff (...)
$ pytest
=== test session starts ===
(...) pytest logs (...)
=== X passed in Y.ZZ s ===
$ generate_all_instances
instances written into the directory 'data/'
```

## File Format

The [file format](https://github.com/lucasguesserts/packing-visualizer/tree/trunk/src/file_format/input) is based on the specifications in the [packing-visualizer project](https://github.com/lucasguesserts/packing-visualizer/).
