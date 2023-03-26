# MNIST data extractor

This repo provides a script to extract the MNIST images and labels given by the binary files [here](http://yann.lecun.com/exdb/mnist/). The images will be extracted to a given folder. The folder structure will be as follows:

```
mnist/
├── 0
│   ├── aaa.jpg
│   ├── ...
│   └── jjj.jpg
├── 1
│   ├── bbb.jpg
│   ├── ...
│   └── ppp.jpg
├── ...
│
└── 9
    ├── hhh.jpg
    ├── ...
    └── zzz.jpg
```

## 1. Setup

To set up the project:

If you are running a linux system:

1. Alter the values of `python` and `pip` of the makefile to suit your system.
2. Run `make .env`
3. Run `. .env/bin/activate`
4. Run `make install`

Otherwise:

1. Create and activate a python virtual environment, follow [link](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) for instructions
2. Install the packages using `pip install -r requirements.txt`
