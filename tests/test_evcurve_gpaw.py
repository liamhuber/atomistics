from ase.build import bulk
import numpy as np
import unittest

from atomistics.calculators.ase_interface.calculator import evaluate_with_ase
from atomistics.workflows.evcurve.workflow import EnergyVolumeCurveWorkflow


try:
    from gpaw import GPAW, PW

    skip_gpaw_test = False
except ImportError:
    skip_gpaw_test = True


@unittest.skipIf(
    skip_gpaw_test, "gpaw is not installed, so the gpaw tests are skipped."
)
class TestEvCurve(unittest.TestCase):
    def test_calc_evcurve(self):
        calculator = EnergyVolumeCurveWorkflow(
            structure=bulk("Al", a=4.05, cubic=True),
            num_points=11,
            fit_type='polynomial',
            fit_order=3,
            vol_range=0.05,
            axes=['x', 'y', 'z'],
            strains=None,
        )
        structure_dict = calculator.generate_structures()
        result_dict = evaluate_with_ase(
            task_dict=structure_dict,
            ase_calculator_class=GPAW,
            xc="PBE",
            mode=PW(300),
            kpts=(3, 3, 3)
        )
        fit_dict = calculator.analyse_structures(output_dict=result_dict)
        print(fit_dict)
        self.assertTrue(np.isclose(fit_dict['volume_eq'], 66.44252286131331, atol=1e-04))
        self.assertTrue(np.isclose(fit_dict['bulkmodul_eq'], 72.38919826652857, atol=1e-04))
        self.assertTrue(np.isclose(fit_dict['b_prime_eq'], 4.453836551712821, atol=1e-04))
