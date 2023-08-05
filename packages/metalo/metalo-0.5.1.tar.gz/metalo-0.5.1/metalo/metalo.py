"""Metabolic analysis of Logical models extracted from maps.

Copyright (C) 2023 Sahar.Aghakhani@inria.fr and Sylvain.Soliman@inria.fr

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# import argparse
import io
import logging
import sys
from contextlib import redirect_stdout
from typing import Final, List, Optional, Set

import casq.celldesigner2qual
import cobra
import pandas
import trappist

from . import version

# import wx


INTERMEDIATES: Final[Set[str]] = {
    "atp_c",
    "adp_c",
    "adn_c",
    "adp_m",
    "amp_c",
    "amp_m",
    "atp_m",
    "cdp_m",
    "cmp_c",
    "co_c",
    "co_e",
    "co2_c",
    "co2_e",
    "co2_m",
    "coa_c",
    "coa_m",
    "ctp_c",
    "fe2_c",
    "fe2_e",
    "fe2_m",
    "ficytC_c",
    "ficytC_e",
    "ficytC_m",
    "gdp_c",
    "gdp_m",
    "gtp_c",
    "gtp_m",
    "h_c",
    "h_e",
    "h_m",
    "h2o_c",
    "h2o_m",
    "h2o2_c",
    " h2o2_m",
    "hco3_c",
    "hco3_e",
    "hco3_m",
    "nad_c",
    "nad_e",
    "nad_m",
    "nadh_c",
    "nadh_e",
    "nadh_m",
    "nadp_c",
    "nadp_m",
    "nadph_c",
    "nadph_m",
    "no_c",
    "no_e",
    "o2_c",
    "o2_e",
    "o2_m",
    "o2s_m",
    "pheme_c",
    "pheme_m",
    "pi_c",
    "pi_e",
    "pi_m",
    "q10_m",
    "q10h2_m",
}


def generate_model(
    map_file: str, init_file: str, casq_args: Optional[str]
) -> pandas.DataFrame:
    """Generate the model from the map."""
    args = ["--names", "--csv", map_file]
    if init_file is not None:
        args.append(f"--fixed={init_file}")
    if casq_args is not None:
        args.extend(casq_args.split())
    casq.celldesigner2qual.main(args)


def generate_trapspaces(model_file: str, trapspaces_file: str):
    """Compute all minimal trap-spaces of given model."""
    with redirect_stdout(io.StringIO()) as f:
        list(trappist.compute_trap_spaces(model_file, display=True, method="sat"))

    trapspace_str = f.getvalue().replace(" ", ",")

    with open(trapspaces_file, "w") as g:
        g.write(trapspace_str)

    trapspaces_df = pandas.read_csv(trapspaces_file)
    return trapspaces_df


def normalize_columns(df: pandas.DataFrame):
    """Normalize names in columns of given DataFrame."""
    df.columns = (
        df.columns.str.replace("_complex", "")
        .str.replace("_Secreted_space_Molecules", "")
        .str.replace("_phosphorylated", "")
        .str.replace("_Cytoplasm", "")
        .str.replace("_Cytosol", "")
        .str.replace("_simple_molecule", "")
        .str.replace("_active", "")
        .str.replace("M_", "")
        .str.replace("_rna", "")
        .str.replace("_antisense", "")
        .str.replace("_Nucleus", "")
        .str.replace("_empty", "")
        .str.replace("_Extracellular_space_Space", "")
        .str.replace("_extracellular", "")
        .str.replace("_Secreted_compartment", "")
        .str.replace("_Secreted_space_Molecules", "")
        .str.replace("_space", "")
        .str.replace("_Mitochondrion_outter_mb", "")
    )


def round_interval(i: pandas.Interval) -> pandas.Interval:
    """Round the bounds of given interval."""
    return pandas.Interval(round(i.left, 4), round(i.right, 4), closed=i.closed)


def optimize_atp_production(Metabolism, file: str, fva: bool):
    """Run FBA using the given model, store results in given file."""
    solution = Metabolism.optimize()
    print(Metabolism.summary(solution, fva=(1.0 if fva else None)))
    pandas.DataFrame(solution.fluxes).to_csv(file)

    ATP_total = solution.objective_value
    if ATP_total == 0:
        rate = 0
        print("No ATP production at all!")
    else:
        if fva:
            fva_result = cobra.flux_analysis.flux_variability_analysis(
                Metabolism, ["PYK", "PGK"], fraction_of_optimum=1.0
            )
            fva_sum = fva_result.sum()
            ATP_glycolysis = pandas.Interval(
                fva_sum.min(), fva_sum.max(), closed="both"
            )
            rate = round_interval(ATP_glycolysis / ATP_total)
        else:
            ATP_glycolysis = solution.fluxes["PYK"] + solution.fluxes["PGK"]
            rate = round(ATP_glycolysis / ATP_total, 4)

    return solution, rate


def main():
    """Run the whole pipeline."""
    pandas.set_option("display.precision", 4)
    pandas.set_option("styler.format.precision", 4)
    if HAS_GUI:
        parser = GooeyParser(description=" ".join(__doc__.splitlines()[:3]) + " GPLv3")
    else:
        parser = ArgumentParser(
            description=" ".join(__doc__.splitlines()[:3]) + " GPLv3"
        )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s v{version}",
    )
    parser.add_argument(
        "-D", "--debug", action="store_true", help="display some debug information"
    )
    parser.add_argument(
        "-f", "--fva", action="store_true", help="run FVA to get interval of values"
    )
    init_args = {"help": "CSV file with forced initial values for the Logic model"}
    if HAS_GUI:
        init_args.update(  # type: ignore
            widget="FileChooser",
            gooey_options={
                "wildcard": "Comma separated file (*.csv)|*.csv",
            },
        )
    parser.add_argument("-i", "--init", **init_args)
    parser.add_argument(
        "-c",
        "--casq",
        help="Additional arguments for CaSQ like -u, -d or -r",
    )
    map_args = {
        "metavar": "MAP",
        "help": "CellDesigner file containing the mechanistic map",
    }
    if HAS_GUI:
        map_args.update(  # type: ignore
            widget="FileChooser",
            gooey_options={"wildcard": "CellDesigner SBML file (*.xml)|*.xml"},
        )
    parser.add_argument("map_file", **map_args)
    model_args = {"metavar": "METABOLISM", "help": "MitoCore style metabolic model"}
    if HAS_GUI:
        model_args.update(  # type: ignore
            widget="FileChooser",
            gooey_options={
                "wildcard": "Metabolic SBML file (*.xml)|*.xml",
            },
        )
    parser.add_argument("metabolic_model", **model_args)
    args = parser.parse_args()

    generate_model(args.map_file, args.init, args.casq)

    assert args.map_file.endswith(".xml"), "Map file must end with '.xml'"
    basename = args.map_file[:-4]
    model_file = basename + ".bnet"
    trapspaces_file = basename + "_trapspaces.csv"

    trapspaces_df = generate_trapspaces(model_file, trapspaces_file)
    normalize_columns(trapspaces_df)
    model_components = set(trapspaces_df.columns.values)
    if args.debug:
        print(trapspaces_df)

    cobra.io.sbml.LOGGER.setLevel(logging.ERROR)
    Metabolism = cobra.io.read_sbml_model(args.metabolic_model)

    Metabolism_Enzymes = [r.id for r in Metabolism.reactions]
    Metabolism_Metabolites = [m.id for m in Metabolism.metabolites]

    common_enzymes = list((model_components.intersection(Metabolism_Enzymes)))
    if args.debug:
        trapspaces_metabolic_enzymes = trapspaces_df[common_enzymes]
        trapspaces_metabolic_enzymes.to_csv(
            basename + "_trapspaces_metabolic_enzymes.csv"
        )
        print(trapspaces_metabolic_enzymes)

    common_metabolites = list(
        model_components.intersection(Metabolism_Metabolites) - INTERMEDIATES
    )
    if args.debug:
        trapspaces_metabolites = trapspaces_df[common_metabolites]
        trapspaces_metabolites.to_csv(basename + "_trapspaces_metabolites.csv")
        print(trapspaces_metabolites)

    Metabolism.objective = ["PYK", "PGK", "CV_MitoCore"]
    solution, rate = optimize_atp_production(
        Metabolism, basename + "_FBA_CTL_obj_ATP.csv", args.fva
    )
    print(
        f"The proportion of global ATP production through glycolysis in control conditions is {rate}.",
    )

    enzymes_to_zero = [e for e in common_enzymes if trapspaces_df[e].max().max() == 0]
    if args.debug:
        print("enzymes_to_zero:", enzymes_to_zero)

    for i in enzymes_to_zero:
        Metabolism.reactions.get_by_id(i).lower_bound = 0
        Metabolism.reactions.get_by_id(i).upper_bound = 0

    metabolites_to_zero = [
        m for m in common_metabolites if trapspaces_df[m].max().max() == 0
    ]
    if args.debug:
        print("metabolites_to_zero:", metabolites_to_zero)

    producing_reactions_metabolite_to_zero: List[str] = []

    for i in metabolites_to_zero:
        producing_reactions_metabolite_to_zero1 = (
            Metabolism.metabolites.get_by_id(i)
            .summary()
            .producing_flux.index.values.tolist()
        )
        producing_reactions_metabolite_to_zero = (
            producing_reactions_metabolite_to_zero
            + producing_reactions_metabolite_to_zero1
        )

    if args.debug:
        print(
            "producing_reactions_metabolite_to_zero: ",
            producing_reactions_metabolite_to_zero,
        )

    for i in producing_reactions_metabolite_to_zero:
        Metabolism.reactions.get_by_id(i).lower_bound = 0
        Metabolism.reactions.get_by_id(i).upper_bound = 0

    solution, rate = optimize_atp_production(
        Metabolism, basename + "_FBA_TRAP_obj_ATP.csv", args.fva
    )
    print(
        f"The proportion of global ATP production through glycolysis in the trap-spaces conditions is {rate}."
    )


if sys.argv[0].endswith("metalo") and (not sys.stdout.isatty() or len(sys.argv) < 2):
    # If we are not attached to a terminal, or have no arguments try to use Gooey

    try:
        from gooey import Gooey, GooeyParser
    except ImportError:
        HAS_GUI = False
        from argparse import ArgumentParser
    else:
        HAS_GUI = True

        # wx.SystemOptions.SetOption("osx.openfiledialog.always-show-types", 1)
        main = Gooey(
            menu=[
                {
                    "name": "File",
                    "items": [
                        {
                            "type": "AboutDialog",
                            "menuTitle": "About",
                            "description": __doc__.splitlines()[0],
                            "version": version,
                            "copyright": "2023",
                            "website": "https://gitlab.inria.fr/soliman/metalo/",
                            "developer": __doc__.splitlines()[2],
                            "license": "GPLv3",
                        },
                        {
                            "type": "Link",
                            "menuTitle": "Visit Our Site",
                            "url": "https://gitlab.inria.fr/soliman/metalo/",
                        },
                    ],
                },
                {
                    "name": "Help",
                    "items": [
                        {
                            "type": "Link",
                            "menuTitle": "Online documentation",
                            "url": "https://metalo.readthedocs.io/",
                        }
                    ],
                },
            ]
        )(main)
else:
    HAS_GUI = False
    from argparse import ArgumentParser


if __name__ == "__main__":
    main()
