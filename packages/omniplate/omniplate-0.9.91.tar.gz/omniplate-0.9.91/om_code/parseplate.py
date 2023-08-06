from pathlib import Path

import numpy as np
import pandas as pd
import om_code.omerrors as errors


def parseplate(
    platereaderfile, platereadertype, wdirpath=".", sheetnumber=0, export=False
):
    """
    Parse plate-reader output into a long dataframe.

    Note that the plate-reader file is assumed to be an Excel file
    and that time is converted into hours.

    Parameters
    ----------
    platereaderfile: str
        The name of the data file created by a platereader.
    platereadertype: str
        The type of plate reader, currently only "Tecan"
        for a Tecan M200 or Tecan F200.
    wdirpath: str, optional
        The path to the platereader_file.
    sheetnumber: integer, optional
        The sheet to read from an excel file.
    export: boolean, optional
        If True, write parsed data to tsv file.

    Example
    -------
    >>> from om_code.parseplate import parseplate
    >>> rdf= parseplate("ExampleData.xlsx", "Tecan", wdirpath="data")
    >>> print(rdf)

                time well      OD   GFP  AutoFL  mCherry
    0       0.000000   A1  0.2555  46.0    18.0     19.0
    1       0.232306   A1  0.2725  45.0    17.0     17.0

    """
    if isinstance(wdirpath, str):
        wdirpath = Path(wdirpath)
    # create a dict to store data
    rdict = {}
    rdict["time"] = []
    rdict["well"] = []

    if platereadertype == "tidy":
        print(
            "Columns must be labelled 'time', 'well', 'OD', etc., "
            "and time must be in units of hours."
        )
        try:
            if ".tsv" in platereaderfile:
                rdf = pd.read_csv(str(wdirpath / platereaderfile), sep="\t")
            else:
                rdf = pd.read_csv(str(wdirpath / platereaderfile))
        except FileNotFoundError:
            raise errors.FileNotFound(str(wdirpath / platereaderfile))
        if rdf.time.max() > 100:
            print("Warning: time does not appear to be in hours.")
        return rdf

    elif platereadertype == "Tecan":
        try:
            dfd = pd.read_excel(
                str(wdirpath / platereaderfile), sheet_name=sheetnumber
            )
        except FileNotFoundError:
            raise errors.FileNotFound(str(wdirpath / platereaderfile))
        # extract datatypes
        datatypes = (
            dfd[dfd.columns[0]]
            .iloc[
                np.nonzero(
                    dfd[dfd.columns[0]]
                    .str.startswith("Cycle Nr", na=False)
                    .to_numpy()
                )[0]
                - 1
            ]
            .to_numpy()
        )
        # if only OD data measured
        if not isinstance(datatypes[0], str):
            datatypes = ["OD"]
        # add datatypes to rdict
        for datatype in datatypes:
            rdict[datatype] = []
        # extract times of measurements
        t = (
            dfd.loc[
                dfd[dfd.columns[0]].str.startswith("Time [s]", na=False),
                dfd.columns[1] :,
            ]
            .dropna(axis="columns")
            .mean()
            .to_numpy()
            .astype("float")
            / 3600.0
        )
        # deal with overflows
        df = dfd.replace("OVER", np.nan)
        cols = df.columns
        # extract data and add to rdict
        df.index = df[cols[0]]
        for x in np.arange(1, 13):
            for y in "ABCDEFGH":
                well = y + str(x)
                if well in df.index:
                    data = df.loc[well, cols[1] :].to_numpy(dtype="float")
                    if data.ndim == 1:
                        data = data[None, :]
                    for i, tv in enumerate(t):
                        rdict["time"].append(tv)
                        rdict["well"].append(well)
                        for k, datatype in enumerate(datatypes):
                            rdict[datatype].append(data[k, i])
    else:
        raise ValueError(f"{platereadertype} not recognised.")
    # convert parsed dict to dataframe
    rdf = pd.DataFrame.from_dict(rdict)
    if export:
        outname = platereaderfile.split(".")[0] + ".tsv"
        print(f"exporting {outname}")
        rdf.to_csv(str(wdirpath / outname), sep="\t")
    return rdf
