from ase.build import bulk
from phonopy.units import VaspToTHz
import unittest

from atomistics.calculators.ase_interface.calculator import evaluate_with_ase
from atomistics.workflows.phonons.workflow import PhonopyWorkflow

try:
    from gpaw import GPAW, PW

    skip_gpaw_test = False
except ImportError:
    skip_gpaw_test = True


@unittest.skipIf(
    skip_gpaw_test, "gpaw is not installed, so the gpaw tests are skipped."
)
class TestPhonons(unittest.TestCase):
    def test_calc_phonons(self):
        calculator = PhonopyWorkflow(
            structure=bulk("Al", a=4.05, cubic=True),
            interaction_range=10,
            factor=VaspToTHz,
            displacement=0.01,
            dos_mesh=20,
            primitive_matrix=None,
            number_of_snapshots=None,
        )
        structure_dict = calculator.generate_structures()
        result_dict = evaluate_with_ase(
            task_dict=structure_dict,
            ase_calculator_class=GPAW,
            xc="PBE",
            mode=PW(300),
            kpts=(3, 3, 3)
        )
        mesh_dict, dos_dict = calculator.analyse_structures(output_dict=result_dict)
        self.assertEqual((324, 324), calculator.get_hesse_matrix().shape)
        self.assertTrue('qpoints' in mesh_dict.keys())
        self.assertTrue('weights' in mesh_dict.keys())
        self.assertTrue('frequencies' in mesh_dict.keys())
        self.assertTrue('eigenvectors' in mesh_dict.keys())
        self.assertTrue('group_velocities' in mesh_dict.keys())
        self.assertTrue('frequency_points' in dos_dict.keys())
        self.assertTrue('total_dos' in dos_dict.keys())
