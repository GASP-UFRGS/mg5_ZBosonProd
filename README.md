# Bozon Z production at the SppS Collider conditions with MG5

This repo contains a MG5 (MadGraph v5) script for generating proton-antiproton events for the production of Z bosons and a python code for plotting the data.

## Instructions

### Running the MadGraph script
For using the MG5 script, use the following command inside the MG5 folder:

`./bin/mg5_aMC path/mg5_ZBosonProd/script.txt`

3 options are available: 

* ppee_LO.txt
* ppee_NLO_QCD.txt
* ppzee_LO.txt

After running the simulations, don't forget to store the cross-section calculated for each one of the processes.

### Analyzing the data

1) Each script will generate a folder with the same name as the script file. Inside the "Events" folder you will find a *.lhe.gz file which you need to unzip using the `gzip` command. In case the package is not found, install it with `$ apt install gunzip` (for Ubuntu). 

2) Modify the "plot_data.py" to work with your data: put the cross-sections calculated from the simulation in the `xsec` list, the `PDF` list corresponds to the name of the processes, the `FILES` list store the path for the data that you unziped and the `Nevents` variable indicates the number of events simulated. Note that the list must contain the information from the processes all in the same order. For instance, the first element of the xsec list must be the cross section related to the first element of the INPUT list and so on.

3) It is possible to change the Kinematical ranges in the `#KINEMATICAL CUTS`. These cuts are activated with the `cuts flag`.

4) Run the script `plot_script.sh` to generate the plots. You can add to the command line the following tags to modificate the plots:
* `--scale`: scale with the number of events.
* `--scale_yield`: scale with the number of events and the integrated luminosity.
* `--cuts`: enable kinematical cuts.
* `--setLog`: apply a logarithmic scale.
* `--filled`: fill the histogram bins.
* `--stacked`: stack the different histograms.
* `--data`: add data (summ of all histograms).

