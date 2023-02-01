# Cosmic

GUI-based cosmology evolution calculator (similar to [Ned Wright's](https://astro.ucla.edu/~wright/CosmoCalc.html) cosmology calculator).

> It's tested for GNU/Linux. However, it should also work in macOS. If you ever encounter a with a problem, feel free to create an issue.

## Installation

You can easily install Cosmic by cloning the repository

    git clone https://github.com/seVenVo1d/cosmic.git

## Requirements

Required packages are given in the `requirements.txt`, and they can be installed via

    python3 -m pip install -r requirements.txt

Additionally, `tkinter` support is required to run Cosmic, and it can be installed by running

in Fedora

    sudo dnf install python3-tkinter

in Ubuntu

    sudo apt install python3-tk

## User Guide

You can run Cosmic by simply typing

    python3 cosmic.py

in the terminal. After you start the program, you'll see a page in this form:

![main_page](https://user-images.githubusercontent.com/45866787/212608475-a6ee691c-c644-434e-b7e6-272e3b710b0f.png)

where you can enter the cosmological parameters. After you click submit, the program will produce three plots:

### Comoving Distance vs Redshift

![com_vs_z](https://user-images.githubusercontent.com/45866787/212608534-0d3d0b59-3241-4593-bbe4-40eee29ab09f.png)

### Angular Diameter Distance vs Redshift

![ad_vs_z](https://user-images.githubusercontent.com/45866787/212608544-3d817bd1-cdfe-4b9e-8459-7b94130a8927.png)

### Luminosity Distance vs Redshift

![ld_vs_z](https://user-images.githubusercontent.com/45866787/212608572-c23eda8c-8f6b-449d-9eb6-209115054d64.png)

and finally, you'll see a page that prints the results

![results](https://user-images.githubusercontent.com/45866787/212608596-1839a77d-57c3-42ce-b561-0fdfdc4dd2c3.png)
