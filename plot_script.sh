#!/bin/bash

cp plot_data.py plot_data_copy.py;

printVar="Options chosen: "
while [ $# -gt 0 ]; do
	case $1 in
    --scale)
      sed -i 's/scale   = False;/scale   = True;/g' plot_data_copy.py;
      printVar+="scale, ";
      shift 1;;
    --scale_yield)
      sed -i 's/scale_yield = False;/scale_yield = True;/g' plot_data_copy.py;
      printVar+="scale_yield, ";
      shift 1;;
    --cuts)
      sed -i 's/cuts    = False;/cuts    = True;/g' plot_data_copy.py;
      printVar+="cuts, ";
      shift 1;;
    --setLog)
      sed -i 's/setLog  = False;/setLog  = True;/g' plot_data_copy.py;
      printVar+="setLog, ";
      shift 1;;
    --filled)
      sed -i 's/filled  = False;/filled  = True;/g' plot_data_copy.py;
      printVar+="filled, ";
      shift 1;;
    --stacked)
      sed -i 's/stacked = False;/stacked = True;/g' plot_data_copy.py;
      printVar+="stacked, ";
      shift 1;;
    --data)
      sed -i 's/data    = False;/data    = True;/g' plot_data_copy.py;
      printVar+="data, ";
      shift 1;
  esac
done

if [ ${#printVar} -eq 16 ]; then
  printVar+="none.";
  echo $printVar;
else 
  formatVar=${printVar:0:-2};
  formatVar+="."
  echo $formatVar;
fi

python plot_data_copy.py;
rm plot_data_copy.py;
