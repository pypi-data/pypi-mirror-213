from typing import List

from pydantic import BaseModel

from hmmer_tables.csv_iter import csv_iter
from hmmer_tables.path_like import PathLike

__all__ = ["TBLScore", "TBLRow", "TBLIndex", "TBLDom", "read_tbl"]


class TBLIndex(BaseModel):
    name: str
    accession: str


class TBLScore(BaseModel):
    e_value: str
    score: str
    bias: str


class TBLDom(BaseModel):
    exp: str
    reg: int
    clu: int
    ov: int
    env: int
    dom: int
    rep: int
    inc: int


class TBLRow(BaseModel):
    target: TBLIndex
    query: TBLIndex
    full_sequence: TBLScore
    best_1_domain: TBLScore
    domain_numbers: TBLDom
    description: str


def read_tbl(filename: PathLike) -> List[TBLRow]:
    """
    Read tbl file type.

    Parameters
    ----------
    file
        File path or file stream.
    """
    rows = []
    with open(filename, "r") as file:
        for x in csv_iter(file):
            row = TBLRow(
                target=TBLIndex(name=x[0], accession=x[1]),
                query=TBLIndex(name=x[2], accession=x[3]),
                full_sequence=TBLScore(e_value=x[4], score=x[5], bias=x[6]),
                best_1_domain=TBLScore(e_value=x[7], score=x[8], bias=x[9]),
                domain_numbers=TBLDom(
                    exp=x[10],
                    reg=int(x[11]),
                    clu=int(x[12]),
                    ov=int(x[13]),
                    env=int(x[14]),
                    dom=int(x[15]),
                    rep=int(x[16]),
                    inc=int(x[17]),
                ),
                description=" ".join(x[18:]),
            )
            rows.append(row)
    return rows
