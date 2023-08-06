<div align="center">
  <img src="banner512x125.png" alt="Logo">
</div>

# Libprotein
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This module allows to analyze existing data to qualify a protein sequence in order to evaluate the sequence knowledge available in various databases.

**⚠️ All this tutorial is made for Ubuntu User for now!**

## Compile and Install the project
This guide provides compilation and installation instructions only for Ubuntu for now.

* First, start by installing github if it's not already installed
```sh
sudo apt install git

```
* Then, clone the repository to the destination you want.

(We will call this destination: <...>)

* Then install all dependencies:

⚠️ This step can take several minutes...
```sh
sudo apt-get install libcurl4-openssl-dev -y && sudo apt install make -y && sudo apt install libboost-all-dev -y && sudo apt install cmake -y && sudo apt install swig3.0 && sudo apt upgrade -y && sudo apt install -y
```
* Open your command prompt at <...>/libprotein/build

*If the build location doesn't exist, create it at <...>/libprotein with:*
```sh
mkdir build && cd build
```
* To compile and install Libprotein, use this command
```sh
cmake .. && make install
```
* To test if the project is working, you can run the command:

```sh
./src/mainlibprotein P08493
```
```sh
pfam file empty
--------------------------------------
           YOUR PROTEIN PTMs          
--------------------------------------
Pos      Name
21      4-carboxyglutamate
22      Phosphoserine
25      Phosphoserine
28      Phosphoserine
56      4-carboxyglutamate
60      4-carboxyglutamate
67      4-carboxyglutamate
71      4-carboxyglutamate
------------------------------------------
there are no PFAM domains for your protein
-------------------------------------------
there are no SCOP domains for your protein
```
* You can now test Librprotein for the Uniprot IDs you want using :
```sh
./src/mainlibprotein <your uniprot ID>
```

## Install Pymol from source

We will install Pymol from source to be able to use the latest version of Pymol because many Ubuntu distributions provide binary packages for open-source PyMOLbut hey often do not provide the latest version.

*⚠️ If you encounter any problems during the installation, you can refer to the official documentation: [Pymol Install on Ubuntu](https://pymolwiki.org/index.php/Linux_Install)*

* Start by installing all the dependencies needed for the installation of Pymol:
```sh
apt-get install git build-essential python3-dev libglew-dev \
  libpng-dev libfreetype6-dev libxml2-dev \
  libmsgpack-dev python3-pyqt5.qtopengl libglm-dev libnetcdf-dev
 ```

* Get the latest version of Pymol from the official repository:
```sh
git clone https://github.com/schrodinger/pymol-open-source.git
```
```sh
git clone https://github.com/rcsb/mmtf-cpp.git
```
```sh
mv mmtf-cpp/include/mmtf* pymol-open-source/include/
```
And go to the directory **/pymol-open-source**
```sh
cd pymol-open-source
```
* Now, we will compile and install Pymol:

*Here i use $HOME, but you can use the directory you want by replacing the prefix command*
```sh
prefix=$HOME/pymol-open-source-build
```
```sh
# Example for dependencies in non-standard places
# export PREFIX_PATH="$HOME/extra/glew-2.0.0:$HOME/extra/libpng-1.6.5:/opt/local"

python3 setup.py build install \
    --home=$prefix
```
* Finally, you can now run Pymol with the command:
```sh
$HOME/pymol-open-source-build/bin/pymol
```
