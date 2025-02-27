from ase.build import bulk
from ase.calculators.emt import EMT
from phonopy.units import VaspToTHz
import unittest

from atomistics.calculators.ase_interface.calculator import evaluate_with_ase
from atomistics.workflows.phonons.workflow import PhonopyWorkflow


class TestPhonons(unittest.TestCase):
    def test_calc_phonons(self):
        calculator = PhonopyWorkflow(
            structure=bulk("Al", a=4.0, cubic=True),
            interaction_range=10,
            factor=VaspToTHz,
            displacement=0.01,
            dos_mesh=20,
            primitive_matrix=None,
            number_of_snapshots=None,
        )
        structure_dict = calculator.generate_structures()
        result_dict = evaluate_with_ase(task_dict=structure_dict, ase_calculator_class=EMT)
        mesh_dict, dos_dict = calculator.analyse_structures(output_dict=result_dict)
        self.assertEqual((324, 324), calculator.get_hesse_matrix().shape)
        self.assertTrue('qpoints' in mesh_dict.keys())
        self.assertTrue('weights' in mesh_dict.keys())
        self.assertTrue('frequencies' in mesh_dict.keys())
        self.assertTrue('eigenvectors' in mesh_dict.keys())
        self.assertTrue('group_velocities' in mesh_dict.keys())
        self.assertTrue('frequency_points' in dos_dict.keys())
        self.assertTrue('total_dos' in dos_dict.keys())
