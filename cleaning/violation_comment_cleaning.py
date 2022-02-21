#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import argparse
import os

from cleaning.data_wrangling import compile_datasets, clean_html, FileType, \
  output_to_csv, output_to_excel


def clean_violations(filenames: str, outfile_base: str,
                     out_type: FileType = FileType.CSV):
  """
  Given a list of filenames for address and violations records data,
  cleans the data, outputting two versions of the cleaned comments data.
  
  The first output file, <outfile_base>.<filetype> contains all the address
  and violation records data with the cleaned comment data.
  
  The second output file, <outfile_base>_comments.<filetype> contains only
  non-empty cleaned comment data.
  :param outfile_base: base output filename. The method will create files
    `<outfile_base>.<filetype>`
  :param out_type: Output filetype. Either EXCEL or CSV
  :param filenames: List of filenames for data to clean
  :return: None
  """
  
  # Create comments output filename
  base, ext = os.path.splitext(outfile_base)
  comments_outfile = base + "_comments"
  
  datasets = [pd.read_csv(filename) for filename in filenames]
  drop_set = ['STARTDTTM']
  
  fill_value = "NoData"
  compiled_data = compile_datasets(datasets, drop_set)
  compiled_data["ViolationComment"] = compiled_data["ViolationComment"].fillna(
    fill_value)
  
  # Clean the HTML in the comments data
  compiled_data["ViolationComment"] = compiled_data.apply(
    lambda x: clean_html(x["ViolationComment"]), axis=1
  )
  
  # Extract non-empty Comments
  compiled_comments = \
    compiled_data[compiled_data.ViolationComment != fill_value][
      "ViolationComment"]
  
  # Output file
  if out_type == FileType.EXCEL:
    # Output to excel
    output_to_excel(compiled_data, outfile_base)
    output_to_excel(compiled_comments, comments_outfile)
    pass
  
  else:
    # Output to csv
    output_to_csv(compiled_data, outfile_base)
    output_to_csv(compiled_comments, comments_outfile)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Clean HFD violation comments.")
  parser.add_argument("filenames",
                      help="Paths to all of the files to be cleaned.",
                      nargs='*', type=str,
                      default=[os.path.normpath(
                        "data/Address_&_Violation_Records_data 2020.csv"),
                        os.path.normpath(
                          r"data/Address_&_Violation_Records_data 2021.csv")])
  parser.add_argument("--out", nargs='?',
                      help="Name of output file. This file should be an excel "
                           "file.",
                      default="ViolationComment2020and2021.xlsx")
  excel_or_csv = parser.add_mutually_exclusive_group()
  
  # Decided to use "csv" as the default output filetype because exporting to
  # CSV is much quicker than creating an Excel spreadsheet. If using an Excel
  # spreadsheet is necessary, add "--outfile=excel" to the program invocation.
  excel_or_csv.add_argument("--outfile", choices=["excel", "csv"],
                            default="csv",
                            help="Choose the filetype for the cleaned data output file."
                                 "Choose either 'csv' or 'excel'")
  
  args = parser.parse_args()
  if args.outfile == "csv":
    clean_violations(args.filenames, args.out, out_type=FileType.CSV)
  else:
    clean_violations(args.filenames, args.out, out_type=FileType.EXCEL)
