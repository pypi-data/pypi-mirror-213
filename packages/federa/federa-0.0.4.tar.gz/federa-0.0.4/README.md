# Federated Learning Framework
[![PyPI - Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/federa/)
[![Documentation Status](https://readthedocs.org/projects/federa/badge/?version=latest)](https://federa.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Ubuntu CI status](https://github.com/anupam-kliv/fl_framework_initial/actions/workflows/ubuntu.yml/badge.svg)](https://github.com/anupam-kliv/fl_framework_initial/actions/workflows/ubuntu.yml)
[![Windows CI status](https://github.com/anupam-kliv/fl_framework_initial/actions/workflows/windows.yml/badge.svg)](https://github.com/anupam-kliv/fl_framework_initial/actions/workflows/windows.yml)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7364/badge)](https://bestpractices.coreinfrastructure.org/projects/7364)
[![Downloads](https://static.pepy.tech/badge/federa)](https://pepy.tech/project/federa)

`FedERA` is a highly dynamic and customizable framework that can accommodate many use cases with flexibility by implementing several functionalities over different federated learning algorithms, and essentially creating a plug-and-play architecture to accommodate different use cases.

## Supported Devices

FedERA has been extensively tested on and works with the following devices:

* Intel CPUs
* Nvidia GPUs
* Nvidia Jetson
* Raspberry Pi
* Intel NUC

With `FedERA`, it is possible to operate the server and clients on **separate devices** or on a **single device** through various means, such as utilizing different terminals or implementing multiprocessing.

## Installation

- Install the stable version via PyPi:
```
$ pip install federa
```
For more installation options check out the [online documentation](https://federa.readthedocs.io/en/latest/installation.html).



## Documentation

Website documentation has been made availbale for `FedERA`. Please visit [FedERA Documentation](https://federa.readthedocs.io/en/latest/index.html) for more details.

1. [Overview](https://federa.readthedocs.io/en/latest/overview.html)
2. [Installation](https://federa.readthedocs.io/en/latest/installation.html)
3. [Tutorials](https://federa.readthedocs.io/en/latest/tutorials.html)
4. [Contribution](https://federa.readthedocs.io/en/latest/contribution.html)
5. [API Reference](https://federa.readthedocs.io/en/latest/api.html)



## Federated Learning Algorithms

Following federated learning algorithms are implemented in this framework:

| Method              | Paper                                                        | Publication                                     |
| ------------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| FedAvg              | [Communication-Efficient Learning of Deep Networks from Decentralized Data](http://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf) | AISTATS'2017 |                                                      
| FedDyn              | [Federated Learning Based on Dynamic Regularization](https://openreview.net/forum?id=B7v4QMR6Z9w) | ICLR' 2021   |          
| Scaffold           | [SCAFFOLD: Stochastic Controlled Averaging for Federated Learning]() | ICML'2020    |
| Personalized FedAvg | [Improving Federated Learning Personalization via Model Agnostic Meta Learning](https://arxiv.org/pdf/1909.12488.pdf) |    Pre-print      |                                                      
| FedAdagrad          | [Adaptive Federated Optimization](https://arxiv.org/pdf/2003.00295.pdf) | ICML'2020    |                                                       
| FedAdam       | [Adaptive Federated Optimization](https://arxiv.org/pdf/2003.00295.pdf) | ICML'2020    |                                                      
| FedYogi    | [Adaptive Federated Optimization](https://arxiv.org/pdf/2003.00295.pdf) | ICML'2020    |                                                      
| Mime       | [Mime: Mimicking Centralized Stochastic Algorithms in Federated Learning](https://arxiv.org/pdf/2008.03606.pdf) | ICML'2020    |                                                      
| Mimelite       | [Mime: Mimicking Centralized Stochastic Algorithms in Federated Learning](https://arxiv.org/pdf/2008.03606.pdf) | ICML'2020    |                                                      


### Datasets Supported

| Dataset                | Training samples         | Test samples       | Classes 
| ---------------------- | ------------------------ | ------------------ | ------------------ |
| MNIST                  | 60,000                   | 10,000             | 10                 |
| FashionMnist           | 60,000                   | 10,000             | 10                 |
| CIFAR-10               | 50,000                   | 10,000             | 10                 |
| CIFAR-100              | 50,000                   | 10,000             | 100                |

### Custom Dataset Support

We also provide a simple way to add your own dataset to the framework. Look into [docs](https://federa.readthedocs.io/en/latest/tutorials/dataset.html#adding-support-for-new-datasets) for more details.

## Models Supported

`FedERA` has support for the following Deep Learning models, which are loaded from `torchvision.models`:

* LeNet
* ResNet18
* ResNet50
* VGG16
* AlexNet

### Custom Model Support

We also provide a simple way to add your own models to the framework. Look into [docs](https://federa.readthedocs.io/en/latest/tutorials/dataset.html#adding-support-for-new-datasets) for more details.


 
<!-- ## References

<a id="1">[1]</a> Schmidt, V., Goyal, K., Joshi, A., Feld, B., Conell, L., Laskaris, N., Blank, D., Wilson, J., Friedler, S., & Luccioni, S. (2021). CodeCarbon: Estimate and Track Carbon Emissions from Machine Learning Computing. https://doi.org/10.5281/zenodo.4658424

<a id="2">[2]</a> -->

## Contact

<!-- Project Investigator: [Prof. ](https://scholar.google.com/citations?user=gF0H9nEAAAAJ&hl=ennjujbj) (abc@edu).

For technical issues related to __**FedERA**__ development, please contact our development team through Github issues or email:

- [Name Sirname](https://scholar.google.com/citations___): _____@gmail.com -->

For technical issues related to __**FedERA**__ development, please contact our development team through Github issues or email.



