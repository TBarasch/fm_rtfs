# Preprocessing and saving Football Manager RTF's as CSV's:

This is an incoplete project, and intended to be used for preprocessing and saving RTF files extracted from football manager as csv's, for the purpose of personal and non-commercial use.

If you come across a bug, or want to request improvments to the functionality please open a [Issue](https://github.com/TBarasch/fm_rtfs/issues) by clicking the green *New Issue* button on the right.

### Useage:

in the folder `example_rtf`, you will find a sample `.rtf` file on which you can test the code to see if it works. to do so please move it into the same location as the `RTF_to_CSV.py` file, and run the python code.

#### Downloading
If you only intend to run the script and not contribute to the code, please only download the code (and do not clone), instructions on how to download a zipped folder can be found [here](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github/)
 
#### Useage
Download and unzip the folder to any location, for the purpose of only running the code and converting the files in your local computer, only the file `RTF_to_CSV.py` is needed.

- To start place the python file in the same directory (folder) as the RTF's you want to convert.


##### To run the code from terminal:

1. `cd` into the dir in which you placed the `RTF_to_CSV.py` and RTF files
2. run the line `python RTF_to_CSV.py`

##### To run from IDE:

1. Open your IDE of choice (PyCharm, VS Code, Other...)
2. Make sure the working directory is set to the folder in which you placed the `RTF_to_CSV.py` and RTF files
3. Open the  `RTF_to_CSV.py` file.
4. Run the script (typically by pressing on a play looking button on the top right).

The process can take a bit depending on the size and amount of RTF files.

When its done, a new folder named `Converted_CSV` will be created - if it doesnt already exist, in which the csv files will be saved.


### Preprocessing:

1. Hight and Weight: Remove the units (i.e 'cm'/'lb' etc') from the column values and appended to the column name
2. Salary: remove the currency symbol from column values and append to column name, then remove 
3. Transfer Value: Remove the currency denotion from values, split into two columns of `Transfer_Value_Lower` and `Transfer_Value_Upper`, added currency symbol to column name, removing thousends and millions trailing letter (i.e k in 10k and m in 10m) and replacing with appropriate number of zeros as well as deliminating comma/period



