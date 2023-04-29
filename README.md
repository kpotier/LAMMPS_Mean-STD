# LAMMPS_Mean-STD
LAMMPS_Mean-STD calculates the mean and the standard deviation of each column from the LAMMPS output file.

### Usage

1. ```python meanstd.py SECTIONS CONVERGEDLINE [DIRECTORY]``` or ```python meanstd.py SECTIONS CONVERGEDLINE DIRECTORY [SECTIONS CONVERGEDLINE DIRECTORY]...```
3. An output file will be created at the directory where ```log.lammps``` is located. Two other output files will be located at the directory where the command is executed.

```SECTIONS``` is the number of sections (the table will be divided in sections).

```CONVERGEDLINE``` is the line (BY COUNTING FROM THE BEGINNING OF THE TABLE) where the calculations will start.

```DIRECTORY``` is the directory of which the ```log.lammps``` file is located.

### Examples
1. ```python meanstd.py 4 0```
This command will inspect every folder and will process every log.lammps file it will find.
The table will be divided in 4 sections (independant to each other). An average of these 4 sections will be done at the end.

2. ```python meanstd.py 4 0 MyRun```
Same as above except that it will only look for a log.lammps in the MyRun folder.

3. ```python meanstd.py 4 0 MyRun 5 0 MySecondRun```
Same as above except that it will look for a log.lammps in the MyRun and MySecondRun folder.
The number of sections will be different for the log.lammps in the MySecondRun.

4. ```python meanstd.py 4 500```
Same as (1) except that this command won't include the first 500 lines of the table.