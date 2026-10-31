![Banner](banner.png)

# dat-Generalize-Column
Replaces values in a column with a more general category (e.g., replacing specific ages with age ranges).  Uses a simple lookup table or regex for generalization. - Focused on Offers tools to automatically anonymize sensitive data within structured datasets (CSV, JSON).  Includes functionalities to replace real data with realistic but fake data, scramble data, and remove identifying information. Utilizes Faker to generate realistic but anonymized names, addresses, and other personal details. Pandas enables easy data manipulation.

## Install
`git clone https://github.com/ShadowGuardAI/dat-generalize-column`

## Usage
`./dat-generalize-column [params]`

## Parameters
- `-h`: Show help message and exit
- `--lookup_file`: Path to a CSV file containing the lookup table (value,generalized_value). Values not present in the lookup file are written to the output unchanged in the default mode. When any value is not covered, the run logs a warning naming how many values missed.
- `--regex`: Regular expression pattern and replacement string (pattern::replacement).
- `--strict-lookup`: With `--lookup_file`, exit 1 and write no output when any value in the column is not covered by the lookup file. Without this flag, uncovered values pass through unchanged and the run still succeeds, with the warning described above.

## License
Copyright (c) ShadowGuardAI
