
<a class="reference external image-reference" href="https://gitlab.com/benvial/pylatt/-/releases" target="_blank"><img alt="Release" src="https://img.shields.io/endpoint?url=https://gitlab.com/benvial/pylatt/-/jobs/artifacts/main/raw/logobadge.json?job=badge&labelColor=c9c9c9"></a> 
<a class="reference external image-reference" href="https://gitlab.com/benvial/pylatt/commits/main" target="_blank"><img alt="Release" src="https://img.shields.io/gitlab/pipeline/benvial/pylatt/main?logo=gitlab&labelColor=dedede&style=for-the-badge"></a> 
<a class="reference external image-reference" href="https://gitlab.com/benvial/pylatt/commits/main" target="_blank"><img alt="Release" src="https://img.shields.io/gitlab/coverage/benvial/pylatt/main?logo=python&logoColor=e9d672&style=for-the-badge"></a>
<a class="reference external image-reference" href="https://black.readthedocs.io/en/stable/" target="_blank"><img alt="Release" src="https://img.shields.io/badge/code%20style-black-dedede.svg?logo=python&logoColor=e9d672&style=for-the-badge"></a>
<a class="reference external image-reference" href="https://gitlab.com/benvial/pylatt/-/blob/main/LICENSE.txt" target="_blank"><img alt="Release" src="https://img.shields.io/badge/license-GPLv3-blue?color=aec2ff&logo=open-access&logoColor=aec2ff&style=for-the-badge"></a>


# PYLATT

**Numerical models of mechanical lattices (truss/frame structures)**

<!-- start elevator-pitch -->

- **Easy to use interface** --- define only the nodes and beams in the irreducible unit cell.
- **Calculation of phononic band diagrams** --- with utilities to define the path along the edges of the Brillouin zone.
- **Auto-diferentiable** --- allowing the optimization of discrete metamaterials.


<!-- end elevator-pitch -->


<!-- start installation -->

## Installation

### From Pypi

Simply run

```bash 
pip install pylatt
```
If you want more numerical backends (pytorch, autograd and jax), including 
auto-differentiation and GPU acceleration, install the full version:

```bash 
pip install pylatt[full]
```

### From source

Clone the repository

```bash 
git clone https://gitlab.com/benvial/pylatt.git
cd pylatt
```

Install the package locally

```bash 
pip install -e .
```

For the full version:

```bash 
pip install -e .[full]
```

### From gitlab

Basic:

```bash 
pip install -e git+https://gitlab.com/benvial/pylatt.git#egg=pylatt
```


Full:

```bash 
pip install -e git+https://gitlab.com/benvial/pylatt.git#egg=pylatt[full]
```

<!-- end installation -->