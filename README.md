# Cosmos-GUI

GUI based cosmology evolution calculator (similar to [ICosmos](http://www.icosmos.co.uk/index.html))

It's tested for GNU/Linux but it should also work in Windows and Mac. If you encounter a problem, feel free to create an issue.

## Installation

Required packages are given in the `requirements.txt` and they can be installed via

    python3 -m pip install -r requirements.txt

## Getting Started

### 1. Run Cosmos-GUI via

    python3 cosmos_gui.py

### 2. Enter the Cosmological Parameters

![main_page](https://user-images.githubusercontent.com/45866787/189471183-167463a0-c1b2-4a4f-bc87-da400f8399e0.png)

After you click submit, the program will produce three plots;

#### a) Comoving Distance vs Redshift

![comoving_distance](https://user-images.githubusercontent.com/45866787/189471185-7432d037-3c1e-47bc-a4e0-c0c470cf538b.png)

#### b) Angular Diameter Distance vs Redshift

![angular_diameter_distance](https://user-images.githubusercontent.com/45866787/189471190-2db78722-2119-47e7-ad2b-c08789d04d23.png)

#### c) Luminosity Distance vs Redshift

![luminosity_distance](https://user-images.githubusercontent.com/45866787/189471196-166f8379-a91a-4dfb-b5ac-88a0d8a1ad14.png)

and finally, you'll see a page that prints the results.

![results](https://user-images.githubusercontent.com/45866787/189471198-26bed840-cbd4-41b1-81d7-845a849f10c0.png)
