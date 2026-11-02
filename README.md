![Introduction banner: the themed scene before any name is spoken](intro-banner.png)

# dat-generalize-column

Title block: the name above is set in Bowlby One in slate on a cloud cream plate, with the date ruled beneath it in monsoon jade and a small weather ship beside the first heading only, in the manner of a forecast entry.

![Logo](logo.png)

![Banner](banner.png)

![Animated scene](scene.svg)

![Major separator](sep-heavy.svg)


# dat-Generalize-Column
Replaces values in a column with a more general category (e.g., replacing specific ages with age ranges).  Uses a simple lookup table or regex for generalization. - Focused on Offers tools to automatically anonymize sensitive data within structured datasets (CSV, JSON).  Includes functionalities to replace real data with realistic but fake data, scramble data, and remove identifying information. Utilizes Faker to generate realistic but anonymized names, addresses, and other personal details. Pandas enables easy data manipulation.

![Major separator](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowGuardAI/dat-generalize-column`


> Station log note: broader words come from the caller alone. The program holds no categories of its own, makes no fake values, and uses no Faker library.

![Minor separator](sep-light.svg)

## Usage
`./dat-generalize-column [params]`

![Minor separator](sep-light.svg)

## Parameters
- `-h`: Show help message and exit
- `--lookup_file`: Path to a CSV file containing the lookup table (value,generalized_value). Values not present in the lookup file are written to the output unchanged in the default mode. When any value is not covered, the run logs a warning naming how many values missed.
- `--regex`: Regular expression pattern and replacement string (pattern::replacement).
- `--strict-lookup`: With `--lookup_file`, exit 1 and write no output when any value in the column is not covered by the lookup file. Without this flag, uncovered values pass through unchanged and the run still succeeds, with the warning described above.


> Station log note: misses pass through unchanged in the default mode. The output can hold a mix of broad categories and exact values under one column heading.

> Station log note: strict mode writes no new output. With the strict switch set, any miss stops the run before the write step, and the run exits 1.

> Station log note: the pattern replacement treats backslashes as live references. A replacement meant as plain text with a backslash in it does not come out literally.

![Minor separator](sep-light.svg)

## License
Copyright (c) ShadowGuardAI

![Major separator](sep-heavy.svg)

## Station log notes, gathered at the watch

The buttons of this re-skin read Generalise the Column, Use a Lookup File, Use a Pattern Pair, Refuse Uncovered Values, and Show the Station Log. Its headings read One Column, Two Methods, Broader Words Come From You, Misses Pass Through by Default, and Strict Means No Output. The working form is entered once more: python3 main.py first, then the input CSV path, the output CSV path, the column name, and exactly one method flag. The repository LICENSE file carries the MIT License, its holder line giving a pen name together with a single initial for the remaining name.
