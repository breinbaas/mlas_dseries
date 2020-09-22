from mlas_dseries.dstability import DStability
from mlas.models.calculationmodel import CalculationModel

def test_dstability():
    calculationmodel = CalculationModel.parse("./testdata/crosssections/A145_2300.json")
    dstability = DStability(calculationmodel=calculationmodel)
    dstability.to_file(save_path="./testdata/output", save_name="crosssection_0")


if __name__=="__main__":
    test_dstability()