# temp hack as long as mlas and geolib are not distributed as packages
import sys
sys.path.append("/home/breinbaas/Programming/packages/mlas")
sys.path.append("/home/breinbaas/Programming/packages/mlas_dseries")
sys.path.append("/home/breinbaas/Programming/libraries/geolib")

from pydantic import BaseModel
from mlas.models.calculationmodel import CalculationModel
from pathlib import Path

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.soils import Soil, MohrCoulombParameters
from geolib.geometry import Point

class DStability(BaseModel):
    calculationmodel: CalculationModel

    def to_file(self, save_path: str, save_name: str):
        filename = Path(save_path) / f"{save_name}.stix"
        dstability_model = DStabilityModel(filename=filename)

        for soilname, parameters in self.calculationmodel.soilparameters.items():
            mohr_coulomb_parameters = MohrCoulombParameters(
                cohesion=parameters['cohesion'],
                friction_angle=parameters['friction_angle']
            )

            if not dstability_model.soils.has_soilcode(soilname):
                soil = Soil(name=soilname, code=soilname, mohr_coulomb_parameters=mohr_coulomb_parameters)
                _ = dstability_model.add_soil(soil)
            else:
                dstability_model.edit_soil(
                    code=soilname, 
                    cohesion=parameters['cohesion'], 
                    friction_angle=parameters['friction_angle']
                )          
            

        for soilpolygon in self.calculationmodel.soilpolygons:
            points = [Point(x=p.x, z=p.z) for p in soilpolygon.points]
            dstability_model.add_layer(points=points, soil_code=soilpolygon.soil_code)

        dstability_model.serialize(filename)


        # dstability_model.edit_soil(code=code, cohesion=2.0, friction_angle=35)

