import logging
import sys
import traceback
from _ctypes import Array
from typing import Union, List

import numpy as np

from hardyweinberg_equilibrium.genetics.allele import Allele
from hardyweinberg_equilibrium.genetics.gene import Gene
from hardyweinberg_equilibrium.hardy_weinberg.hardy_weinberg import HardyWeinberg
from hardyweinberg_equilibrium.utils.generators.population_generator import generate_population
from hardyweinberg_equilibrium.utils.parsers.args_parser import parse_args

from hardyweinberg_equilibrium.config import get_logger

log = get_logger(__name__)


# --------------------------------------------------------------------------- #
def parse_genes_from_cli(genes: list):
    gene_list = []
    log.info(f"\nShape of genes: {np.shape(genes)}")
    if isinstance(genes, list):
        for gene in genes[0]:
            # log.debug(f"\nGene: {gene}")
            if isinstance(gene, dict):
                gene_list.append(Gene(mother=Allele(gene.get('mother').get('symbol')),
                                      father=Allele(gene.get('father').get('symbol')),
                                      description=gene.get('description')))
            elif isinstance(gene, Gene):
                gene_list.append(gene)
            else:
                log.error(f"\nGene: {gene} is not a valid gene.")
    elif isinstance(genes, Gene):
        gene_list.append(genes)
    else:
        log.error(f"\nGenes: {genes} is not a valid gene.")
    log.debug(f"\nParsed Gene List size: {len(gene_list)}")
    return gene_list


# --------------------------------------------------------------------------- #
def app(
        p: float = None,
        q: float = None,
        total_population: float = None,
        original_p_population: float = None,
        original_q_population: float = None,
        original_2pq_population: float = None,
        genes: Union[List[Gene], Array[Gene]] = None,
        **kwargs
):
    try:
        parser = parse_args()
        args = parser.parse_args()
        # log.debug(f"CLi Args: \n{args}")
        args.p = p if p is not None else args.p
        args.q = q if q is not None else args.q
        args.ppop = original_p_population if original_p_population is not None else args.ppop
        args.qpop = original_q_population if original_q_population is not None else args.qpop
        args.pq2pop = original_2pq_population if original_2pq_population is not None else args.pq2pop
        args.tpop = total_population if total_population is not None else args.tpop \
            if args.tpop is not None \
            else args.ppop + args.qpop + args.pq2pop \
            if args.ppop is not None and args.qpop is not None and args.pq2pop is not None \
            else None
        args.genes = genes \
            if genes is not None and isinstance(genes, list) \
            else parse_genes_from_cli(args.genes) \
            if args.genes is not None and isinstance(args.genes, list) and len(args.genes) > 0 \
            else None
        # _________________________________________________________________ #
        # print help message if no arguments are passed
        # log.info(f"Args: {sys.argv}")
        if len(sys.argv) <= 2:
            parser.print_help()
            sys.exit(1)

        # _________________________________________________________________ #
        # log.debug(f"\nInit Args: \n{args}")
        # _________________________________________________________________ #
        if args.debug:
            log.setLevel(logging.DEBUG)
        elif args.verbose:
            log.setLevel(logging.INFO)
        # _________________________________________________________________ #
        if args.samples is not None:
            args.genes = generate_population(args.samples)
        hardy_weinberg = HardyWeinberg(
            p=args.p,
            q=args.q,
            total_population=args.tpop,
            homozygous_dominant_population=args.ppop,
            homozygous_recessive_population=args.qpop,
            heterozygous_population=args.pq2pop,
            genes=args.genes,
            **kwargs
        )
        log.info(hardy_weinberg)
        return hardy_weinberg.to_json()
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
