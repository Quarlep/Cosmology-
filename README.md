# Cosmic

GUI based cosmology evolution calculator (similar to [ICosmos](http://www.icosmos.co.uk/index.html))

> It's tested for GNU/Linux, however it should also work in Windows and Mac. If you ever encounter with a problem, feel free to create an issue.

## Installation

Required packages are given in the `requirements.txt` and they can be installed via

    python3 -m pip install -r requirements.txt

## User Guide

You can run *Cosmic* via

    python3 cosmic.py

Later on you'll see a page in this form

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
