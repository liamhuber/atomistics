import os
import unittest
import pyiron_lammps as pyr


class TestProjectData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.count_lst = [22, 22, 22, 21, 21]
        cls.element_lst = ["Fe", "Ni", "Cr", "Co", "Cu"]
        cls.potential = '2021--Deluigi-O-R--Fe-Ni-Cr-Co-Cu--LAMMPS--ipr1'
        cls.resource_path = os.path.join(os.path.dirname(__file__), "static")

    def test_example_elastic_constants_with_one_executable(self):
        # Generate SQS Structure
        structure = pyr.generate_sqs_structure(
            structure_template=pyr.get_ase_bulk("Al", cubic=True).repeat([3, 3, 3]),
            element_lst=self.element_lst,
            count_lst=self.count_lst
        )[0]
        self.assertEqual(len(structure), sum(self.count_lst))

        # Initialize Engine
        lmp = pyr.get_lammps_engine()

        # Select Potential
        df_pot = pyr.get_potential_dataframe(
            structure=structure,
            resource_path=self.resource_path
        )
        df_pot_selected = df_pot[df_pot.Name == self.potential].iloc[0]

        # Optimize Structure
        structure_opt = pyr.optimize_structure(
            lmp=lmp,
            structure=structure,
            potential_dataframe=df_pot_selected
        )
        self.assertEqual(len(structure_opt), sum(self.count_lst))

        # Calculate Elastic Constants
        elastic_matrix = pyr.calculate_elastic_constants(
            lmp=lmp,
            structure=structure_opt,
            potential_dataframe=df_pot_selected,
            num_of_point=5,
            eps_range=0.005,
            sqrt_eta=True,
            fit_order=2
        )
        self.assertTrue(elastic_matrix[0, 0] > 200)
        self.assertTrue(elastic_matrix[1, 1] > 200)
        self.assertTrue(elastic_matrix[2, 2] > 200)
        self.assertTrue(elastic_matrix[0, 1] > 135)
        self.assertTrue(elastic_matrix[0, 2] > 135)
        self.assertTrue(elastic_matrix[1, 2] > 135)
        self.assertTrue(elastic_matrix[3, 3] > 100)
        self.assertTrue(elastic_matrix[4, 4] > 100)
        self.assertTrue(elastic_matrix[5, 5] > 100)

        # Finalize
        lmp.close()

    def test_example_elastic_constants_with_separate_executable(self):
        # Generate SQS Structure
        structure = pyr.generate_sqs_structure(
            structure_template=pyr.get_ase_bulk("Al", cubic=True).repeat([3, 3, 3]),
            element_lst=self.element_lst,
            count_lst=self.count_lst
        )[0]
        self.assertEqual(len(structure), sum(self.count_lst))

        # Select Potential
        df_pot = pyr.get_potential_dataframe(
            structure=structure,
            resource_path=self.resource_path
        )
        df_pot_selected = df_pot[df_pot.Name == self.potential].iloc[0]

        # Optimize Structure
        structure_opt = pyr.optimize_structure(
            structure=structure,
            potential_dataframe=df_pot_selected
        )
        self.assertEqual(len(structure_opt), sum(self.count_lst))

        # Calculate Elastic Constants
        elastic_matrix = pyr.calculate_elastic_constants(
            structure=structure_opt,
            potential_dataframe=df_pot_selected,
            num_of_point=5,
            eps_range=0.005,
            sqrt_eta=True,
            fit_order=2
        )
        self.assertTrue(elastic_matrix[0, 0] > 200)
        self.assertTrue(elastic_matrix[1, 1] > 200)
        self.assertTrue(elastic_matrix[2, 2] > 200)
        self.assertTrue(elastic_matrix[0, 1] > 135)
        self.assertTrue(elastic_matrix[0, 2] > 135)
        self.assertTrue(elastic_matrix[1, 2] > 135)
        self.assertTrue(elastic_matrix[3, 3] > 100)
        self.assertTrue(elastic_matrix[4, 4] > 100)
        self.assertTrue(elastic_matrix[5, 5] > 100)

    def test_example_elastic_constants_with_statement(self):
        # Generate SQS Structure
        structure = pyr.generate_sqs_structure(
            structure_template=pyr.get_ase_bulk("Al", cubic=True).repeat([3, 3, 3]),
            element_lst=self.element_lst,
            count_lst=self.count_lst
        )[0]
        self.assertEqual(len(structure), sum(self.count_lst))

        with pyr.get_lammps_engine() as lmp:
            # Select Potential
            df_pot = pyr.get_potential_dataframe(
                structure=structure,
                resource_path=self.resource_path
            )
            df_pot_selected = df_pot[df_pot.Name == self.potential].iloc[0]

            # Optimize Structure
            structure_opt = pyr.optimize_structure(
                lmp=lmp,
                structure=structure,
                potential_dataframe=df_pot_selected
            )
            self.assertEqual(len(structure_opt), sum(self.count_lst))

            # Calculate Elastic Constants
            elastic_matrix = pyr.calculate_elastic_constants(
                lmp=lmp,
                structure=structure_opt,
                potential_dataframe=df_pot_selected,
                num_of_point=5,
                eps_range=0.005,
                sqrt_eta=True,
                fit_order=2
            )
            self.assertTrue(elastic_matrix[0, 0] > 200)
            self.assertTrue(elastic_matrix[1, 1] > 200)
            self.assertTrue(elastic_matrix[2, 2] > 200)
            self.assertTrue(elastic_matrix[0, 1] > 135)
            self.assertTrue(elastic_matrix[0, 2] > 135)
            self.assertTrue(elastic_matrix[1, 2] > 135)
            self.assertTrue(elastic_matrix[3, 3] > 100)
            self.assertTrue(elastic_matrix[4, 4] > 100)
            self.assertTrue(elastic_matrix[5, 5] > 100)
