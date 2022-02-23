#!/bin/bash
echo "--------------------------------------------"
echo "Name:         Conda Packages Installer"
echo "Author:       Jose L. Agraz, PhD"
echo "Description:  Installing Applications and Packages for Normalization scripts,"
echo "Note:         Verify Installation is in the appropriate                      "
echo "              environment (ex. conda activate Normalization_Libraries_2021)  "
echo "              In order to avoid library conflicts, use python 3.7.9          "
echo "              ex. conda create -n Normalization_Python_3.7.9 python=3.7.9    "
echo "              source activate Normalization_Python_3.7.9                     "  
echo "Date:         11/03/2021"
echo " Usage: ./CondaPackagesInstall"
echo "--------------------------------------------"
echo "Installing graphviz"
conda install -c conda-forge python-graphviz -y
echo "--------------------------------------------"
echo "Installing tk"
conda install -c anaconda tk                 -y
echo "--------------------------------------------"
echo "Installing Spams package"
conda install -c conda-forge python-spams    -y
echo "--------------------------------------------"
echo "Installing  future"
conda install -c conda-forge future          -y
echo "--------------------------------------------"
echo "Installing plotly package"
conda install -c plotly plotly               -y
echo "--------------------------------------------"
echo "Installing dask"
conda install -c conda-forge dask distributed -y
echo "--------------------------------------------"
echo "Installing Numpy"
conda install -c conda-forge numpy           -y
echo "--------------------------------------------"
echo "Installing Pandas package"
conda install -c conda-forge pandas          -y
echo "--------------------------------------------"
echo "Installing Scikit package"
conda install -c conda-forge scikit-image    -y
echo "--------------------------------------------"
echo "Installing tabulate"
conda install -c conda-forge tabulate        -y
echo "--------------------------------------------"
echo "Installing json"
conda install -c jmcmurray json              -y
echo "--------------------------------------------"
echo "Installing Opencv"
conda install -c conda-forge opencv          -y
echo "--------------------------------------------"
echo "Installing  pathlib package"
conda install -c conda-forge pathlib         -y
echo "--------------------------------------------"
echo "Installing  matplotlib package"
conda install -c conda-forge matplotlib      -y
echo "--------------------------------------------"
echo "Installing Pillow"
conda install -c conda-forge pillow          -y
echo "--------------------------------------------"
echo "Installing tqdm"
conda install -c conda-forge tqdm            -y
echo "--------------------------------------------"
echo "Installing glob2"
conda install -c conda-forge glob2           -y
echo "--------------------------------------------"
echo "Installing tifffile"
conda install -c conda-forge tifffile        -y
echo "--------------------------------------------"
echo "Installing pyvips"
#conda install -c conda-forge pyvips      -y
echo "--------------------------------------------"
echo "Installing Openslide"
conda install -c conda-forge openslide       -y
echo "--------------------------------------------"
echo "Installing bokeh"
conda install -c conda-forge bokeh           -y
echo "--------------------------------------------"
echo "Installing  dask"
conda install -c conda-forge dask            -y
echo "--------------------------------------------"
echo "Installing dask-image"
conda install -c conda-forge dask-image      -y
echo "--------------------------------------------"
echo "Installing dask-ml"
conda install -c conda-forge dask-ml         -y
echo "--------------------------------------------"
echo "Installing  dask-labextension"
conda install -c conda-forge dask-labextension -y
echo "--------------------------------------------"
echo "Installing jupyterlab"
conda install -c conda-forge jupyterlab      -y
echo "--------------------------------------------"
echo "Installing  nodejs"
conda install -c conda-forge nodejs          -y
echo "--------------------------------------------"
echo "Installing  notebook"
conda install -c conda-forge notebook        -y
echo "--------------------------------------------"
echo "Installing tornado"
conda install -c conda-forge tornado         -y
echo "--------------------------------------------"
echo "Installing  numba"
conda install -c conda-forge numba           -y
echo "--------------------------------------------"
echo "Installing  numpy"
conda install -c conda-forge numpy           -y
echo "--------------------------------------------"
echo "Installing  pip"
conda install -c conda-forge pip             -y
echo "--------------------------------------------"
echo "Installing seaborn"
conda install -c conda-forge seaborn         -y
echo "--------------------------------------------"
echo "Installing  scikit-learn"
conda install -c conda-forge scikit-learn    -y
echo "--------------------------------------------"
echo "Installing  nbserverproxy"
conda install -c conda-forge nbserverproxy   -y
echo "--------------------------------------------"
echo "Installing  nomkl"
conda install -c conda-forge nomkl           -y
echo "--------------------------------------------"
echo "Installing  h5py"
conda install -c conda-forge h5py            -y
echo "--------------------------------------------"
echo "Installing  xarray"
conda install -c conda-forge xarray          -y
echo "--------------------------------------------"
echo "Installing  bottleneck"
conda install -c conda-forge bottleneck      -y
echo "--------------------------------------------"
echo "Installing requests"
conda install -c conda-forge requests        -y
echo "--------------------------------------------"
echo "Installing py-xgboost"
conda install -c conda-forge py-xgboost      -y
echo "--------------------------------------------"
echo "Installing dask-xgboost"
conda install -c conda-forge dask-xgboost    -y
echo "--------------------------------------------"
echo "Installing mimesis"
conda install -c conda-forge mimesis         -y
echo "--------------------------------------------"
echo "Installing astropy"
conda install -c conda-forge astropy         -y
echo "--------------------------------------------"
echo "Installing dask-kubernetes"
conda install -c conda-forge dask-kubernetes -y
echo "--------------------------------------------"
echo "Installing yarn"
conda install -c conda-forge yarn            -y
echo "--------------------------------------------"
#conda install -c anaconda spyder
conda install -c conda-forge spyder          -y
echo "--------------------------------------------"
echo "Installing pyarrow"
#conda install fastparquet pyarrow -c conda-forge -y
#conda install -c conda-forge  pyarrow        -y
conda install -c conda-forge pyarrow fastparquet -y
echo "Done"



