import argparse
import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Generalizes a column in a CSV file by replacing values with more general categories.")
    parser.add_argument("input_file", help="Path to the input CSV file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    parser.add_argument("column_name", help="Name of the column to generalize.")
    parser.add_argument("--lookup_file", help="Path to a CSV file containing the lookup table (value,generalized_value). Values not present in the lookup file are written to the output unchanged in the default mode.", required=False)
    parser.add_argument("--regex", help="Regular expression pattern and replacement string (pattern::replacement).", required=False)
    parser.add_argument("--strict-lookup", action="store_true", help="With --lookup_file, exit 1 and write no output when any value in the column is not covered by the lookup file.")

    return parser

def generalize_column(df, column_name, lookup_file=None, regex=None, strict_lookup=False):
    """
    Generalizes the specified column based on either a lookup table or a regular expression.

    Args:
        df (pd.DataFrame): The Pandas DataFrame to process.
        column_name (str): The name of the column to generalize.
        lookup_file (str, optional): Path to a CSV file for lookup generalization. Defaults to None.
        regex (str, optional): Regular expression and replacement string (pattern::replacement). Defaults to None.

    Returns:
        pd.DataFrame: The modified DataFrame with the generalized column.

    Raises:
        ValueError: If neither lookup_file nor regex is provided, or if both are provided.
        FileNotFoundError: If the lookup_file does not exist.
        Exception: For other unexpected errors during processing.
    """
    try:
        if lookup_file and regex:
            raise ValueError("Only one of --lookup_file or --regex can be specified.")
        elif not lookup_file and not regex:
            raise ValueError("Either --lookup_file or --regex must be specified.")

        if lookup_file:
            try:
                lookup_df = pd.read_csv(lookup_file)
                if lookup_df.shape[1] != 2:
                    raise ValueError(f"Lookup file {lookup_file} must have exactly two columns (value, generalized_value).  It has {lookup_df.shape[1]} columns.")
                lookup_dict = dict(zip(lookup_df.iloc[:, 0].astype(str), lookup_df.iloc[:, 1].astype(str))) # Ensure keys are strings.
                # Fill from the string form of the column, not the original
                # series: filling a string result with values of the original
                # dtype is the combination newer pandas warns about, and the
                # generalized column is text either way.
                original = df[column_name].astype(str)
                mapped = original.map(lookup_dict)
                miss_count = int(mapped.isna().sum())
                if miss_count:
                    logging.warning(f"Lookup warning: {miss_count} value(s) in column '{column_name}' are not covered by the lookup file and will pass through unchanged.")
                    if strict_lookup:
                        raise ValueError(f"Strict lookup failed: {miss_count} value(s) in column '{column_name}' are not covered by the lookup file.")
                df[column_name] = mapped.fillna(original)
            except FileNotFoundError:
                raise

        elif regex:
            # A missing "::" makes the unpack raise ValueError with a
            # message about value counts that tells the user nothing;
            # name the actual format problem and let main log it once.
            if "::" not in regex:
                raise ValueError("Invalid regex format. Use 'pattern::replacement'.")
            pattern, replacement = regex.split("::", 1)
            df[column_name] = df[column_name].astype(str).replace(pattern, replacement, regex=True)

        return df

    except (ValueError, FileNotFoundError):
        # No logging in this layer: every handler here and in main used
        # to log the same failure, so one bad argument printed the error
        # three times. main logs it once, with the exit code.
        raise


def main():
    """
    Main function to execute the data generalization process.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # Input validation: File extension check
        if not args.input_file.lower().endswith('.csv'):
            raise ValueError("Input file must be a CSV file.")

        if not args.output_file.lower().endswith('.csv'):
             raise ValueError("Output file must be a CSV file.")

        df = pd.read_csv(args.input_file)

        # Input validation: Column name check
        if args.column_name not in df.columns:
            raise ValueError(f"Column '{args.column_name}' not found in the input file.")


        generalized_df = generalize_column(df.copy(), args.column_name, args.lookup_file, args.regex, strict_lookup=args.strict_lookup)

        # Securely write to the output file (avoiding potential path traversal vulnerabilities)
        generalized_df.to_csv(args.output_file, index=False)
        logging.info(f"Generalized data saved to {args.output_file}")

    except FileNotFoundError as e:
        # The missing file can be the lookup file, not just the input;
        # the old message always named the input file, which sent the
        # user to check a file that exists. The exception knows which
        # path failed, so report that one.
        missing = getattr(e, "filename", None) or args.input_file
        logging.error(f"File not found: {missing}")
        sys.exit(1)  # Exit with an error code
    except ValueError as e:
        logging.error(e)
        sys.exit(1) # Exit with an error code.
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit with an error code



if __name__ == "__main__":
    main()

