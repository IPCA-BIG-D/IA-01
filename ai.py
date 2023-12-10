import ast
from constraint import Problem, AllDifferentConstraint
from dataclasses import dataclass
from enum import Enum
from itertools import combinations


@dataclass
class Bed:
    id: int
    room_number: int

    def __repr__(self) -> str:
        return str(self.id)


class Gender(Enum):
    MALE = ("MALE",)
    FEMALE = ("FEMALE",)
    OTHER = "OTHER"


@dataclass
class Patient:
    id: int
    name: str
    age: int
    gender: Gender
    admission_date: int
    discharge_date: int


def find_combinations(nums):
    result = []
    for r in range(1, len(nums) + 1):
        result.extend(combinations(nums, r))
    return result


def get_vars_except_current_patient(variables, patient):
    vars_to_return = []
    for v in variables:
        if v.split("_")[3] != patient:
            vars_to_return.append(v)
    return vars_to_return


def get_vars_only_current_bed(variables, day):
    vars_to_return = []
    for v in variables:
        if v.split("_")[1] == day:
            vars_to_return.append(v)
    return vars_to_return


def find_patients(patients, id):
    for patient in patients:
        if patient.id == id:
            return patient
    return None


def patient_admission_scheduling():
    # Create a problem instance
    problem = Problem()

    beds = [
        Bed(1, 1),
        Bed(2, 1),
        Bed(3, 2),
        Bed(4, 2),
        Bed(5, 1),
        Bed(6, 1),
        Bed(7, 2),
        Bed(8, 2),
    ]

    patients = [
        Patient(1, "Patient1", 98, Gender.MALE, 0, 1),
        Patient(2, "Patient2", 82, Gender.MALE, 0, 0),
        Patient(3, "Patient3", 43, Gender.MALE, 1, 1),
        Patient(4, "Patient4", 88, Gender.MALE, 0, 0),
        Patient(5, "Patient5", 20, Gender.FEMALE, 0, 3),
        Patient(6, "Patient6", 65, Gender.FEMALE, 0, 1),
        Patient(7, "Patient7", 33, Gender.FEMALE, 1, 7),
        Patient(8, "Patient8", 86, Gender.MALE, 2, 3),
        Patient(9, "Patient9", 22, Gender.FEMALE, 2, 5),
        Patient(10, "Patient10", 70, Gender.FEMALE, 3, 10),
        Patient(11, "Patient11", 42, Gender.MALE, 4, 10),
        Patient(12, "Patient12", 3, Gender.FEMALE, 5, 11),
        Patient(13, "Patient13", 14, Gender.FEMALE, 5, 12),
        Patient(14, "Patient14", 78, Gender.MALE, 7, 13),
        Patient(15, "Patient15", 29, Gender.FEMALE, 8, 9),
        Patient(16, "Patient16", 61, Gender.FEMALE, 9, 15),
        Patient(17, "Patient17", 56, Gender.FEMALE, 10, 17),
        Patient(18, "Patient18", 106, Gender.FEMALE, 10, 14),
        Patient(19, "Patient19", 4, Gender.MALE, 11, 17),
        Patient(20, "Patient20", 52, Gender.FEMALE, 12, 19),
    ]

    for patient in patients:
        days_for_patient = set(
            range(patient.admission_date, patient.discharge_date + 1)
        )
        domain = [f"bed_{bed}_days_{days_for_patient}" for bed in beds]
        problem.addVariable(f"patient_{patient.id}", domain)

    for variable, domain in problem._variables.items():
        patient = variable.split("_")[1]
        patients_except_var = [p for p in problem._variables if p != variable]

        def test(a, b):
            bed_a = a.split("_")[1]
            bed_b = b.split("_")[1]
            set_a = ast.literal_eval(a.split("_")[3])
            set_b = ast.literal_eval(b.split("_")[3])
            return len(set_a & set_b) == 0 or bed_a != bed_b

        for patient in patients_except_var:
            problem.addConstraint(test, [variable, patient])

    # for variable, domain in problem._variables.items():
    #     patient_id = int(variable.split("_")[3])
    #     patient = find_patients(patients, patient_id)
    #     days_in_hospital = list(
    #         range(patient.admission_date, patient.discharge_date + 1)
    #     )

    #     def test(a):
    #         print(list(a) == days_in_hospital)
    #         return list(a) == days_in_hospital

    #     problem.addConstraint(test, [variable])

    # # Add patients cannot be in different beds constraint
    # for v, domain in problem._variables.items():
    #     bed_from_var = v.split("_")[1]
    #     all_vars_except_current_day = get_vars_except_current_bed(
    #         problem._variables, bed_from_var
    #     )

    #     def t(a, b):
    #         return b != a or (a == None and b == None)

    #     for except_days in all_vars_except_current_day:
    #         problem.addConstraint(t, [v, except_days])

    # # Solve the problem
    solutions = problem.getSolutions()

    # Print the solution(s)
    if solutions:
        for solution in solutions:
            print(solution)
        #    print("\nSolution:")
        #    for patient in patients:
        #        for night in nights:
        #            print(
        #                f"{patient}'s bed on night {night}: {solution[f'{patient}_night_{night}']}"
        #            )
        print(f"There are {len(solutions)} solutions")
    else:
        print("No solution found.")


if __name__ == "__main__":
    patient_admission_scheduling()
