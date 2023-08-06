# cpumodel

A Python library to parse and return various attributes from the CPU string

It has only been tested on relatively modern AMD and Intel CPUs that are likely to still be in use,
i.e. AMD Ryzen, AMD EPYC, Intel i-series, Intel Xeon E3/E5 and newer. Other CPUs may or may not produce
useful output.

If you want to request support for an unsupported CPU or if you see a bug in the output, see the
Contributing section.

## Installation

```terminal
pip install cpumodel
```

## Usage

### As a library

```py
from cpumodel imnport get_cpu_model

info = get_cpu_model()
```

### As a script

```terminal
$ cpumodel
{'cpuVendor': 'AMD', 'cpuString': 'AMD Ryzen 7 5700G', 'cpuModel': 'Ryzen 7 5700G', 'cpuFamily': 'Ryzen 7', 'cpuGeneration': '5', 'cpuLetter': 'G'}
```

## Output

This library returns up to 6 values (it is possible for values to be `None`)

* `cpuVendor`, the CPU vendor, e.g. `Intel`
* `cpuString`, the full model string of the CPU, e.g. `Intel Core i7-6700S`
* `cpuModel`, the shorter model name of the CPU, e.g. `Core i7-6700S`
* `cpuFamily`, the concise family name of the CPU, e.g. `Core i7`
* `cpuGeneration`, the numeric generation of the CPU, e.g. `6`
* `cpuLetter`, any trailing letter codes for this CPU, e.g. `S`

## Examples

The best explanation of the data returned is probably by giving various examples.

| `cpuVendor` | `cpuString`                    | `cpuModel`      | `cpuFamily` | `cpuGeneration` | `cpuLetter` |
|-------------|--------------------------------|-----------------|-------------|-----------------|-------------|
| `AMD`       | `AMD Ryzen 7 5700G`            | `Ryzen 7 5700G` | `Ryzen 7`   | `5`             | `G`         |
| `Intel`     | `12th Gen Intel Core i7-1265U` | `Core i7-1265U` | `Core i7`   | `12`            | `U`         |
| `Intel`     | `Intel Core i5-6300U`          | `Core i5-6300U` | `Core i5`   | `6`             | `U`         |

## Contribution

If this library doesn't work properly on your CPU, it's probably because I've never tested on a CPU of that type.

Please [open an issue](https://github.com/djjudas21/cpumodel/issues), and describe what you would expect the
output of this module to be, and include the output of this command:

```sh
grep 'model name' /proc/cpuinfo | sort -u
```
