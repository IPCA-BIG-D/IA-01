import ast
from constraint import Problem, AllDifferentConstraint
from dataclasses import dataclass
from enum import Enum
from itertools import combinations


@dataclass
class Room:
    id: int
    oxygen: bool
    telemetry: bool


@dataclass
class Bed:
    id: int
    room: Room

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
    oxygen: bool
    telemetry: bool


def find_patients(patients, id):
    for patient in patients:
        if patient.id == id:
            return patient
    return None


def get_bed_by_id(beds, bed_id) -> Bed:
    for bed in beds:
        if bed.id == bed_id:
            return bed
    return None


def patient_admission_scheduling():
    # Create a problem instance
    problem = Problem()

    rooms = [
        Room(1, True, False),
        Room(2, True, True),
        Room(3, True, False),
        Room(3, True, True),
    ]

    beds = [
        Bed(1, rooms[0]),
        Bed(2, rooms[0]),
        Bed(3, rooms[1]),
        Bed(4, rooms[1]),
        Bed(5, rooms[2]),
        Bed(6, rooms[2]),
        Bed(7, rooms[3]),
        Bed(8, rooms[3]),
    ]

    patients = [
        Patient(1, "Patient1", 98, Gender.MALE, 0, 0, False, False),
        Patient(2, "Patient2", 82, Gender.MALE, 0, 5, True, True),
        Patient(3, "Patient3", 43, Gender.MALE, 0, 1, False, False),
        Patient(4, "Patient4", 88, Gender.MALE, 0, 4, False, False),
        Patient(5, "Patient5", 20, Gender.FEMALE, 0, 3, False, True),
        Patient(6, "Patient6", 65, Gender.FEMALE, 0, 1, False, False),
        Patient(7, "Patient7", 33, Gender.FEMALE, 1, 7, True, False),
        Patient(8, "Patient8", 86, Gender.MALE, 2, 3, False, False),
        Patient(9, "Patient9", 22, Gender.FEMALE, 2, 5, False, True),
        Patient(10, "Patient10", 70, Gender.FEMALE, 3, 10, True, False),
        Patient(11, "Patient11", 42, Gender.MALE, 4, 10, True, True),
        Patient(12, "Patient12", 3, Gender.FEMALE, 5, 11, False, False),
        Patient(13, "Patient13", 14, Gender.FEMALE, 5, 12, False, True),
        Patient(14, "Patient14", 78, Gender.MALE, 7, 13, False, False),
        Patient(15, "Patient15", 29, Gender.FEMALE, 8, 9, True, False),
        Patient(16, "Patient16", 61, Gender.FEMALE, 9, 15, False, False),
        Patient(17, "Patient17", 56, Gender.FEMALE, 10, 17, False, True),
        Patient(18, "Patient18", 106, Gender.FEMALE, 10, 14, True, False),
        Patient(19, "Patient19", 4, Gender.MALE, 11, 17, True, False),
        Patient(20, "Patient20", 52, Gender.FEMALE, 12, 19, True, True),
    ]

    for patient in patients:
        days_for_patient = set(
            range(patient.admission_date, patient.discharge_date + 1)
        )
        domain = [f"bed_{bed}_days_{days_for_patient}" for bed in beds]
        problem.addVariable(f"patient_{patient.id}", domain)

    # Avalia para cada paciente se o numero de dias (set) interceta com outro paciente,
    # Se sim, a condição é falsa excepto se a cama for diferente
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

    # Adicionar constraint de oxigenio e telemetria
    for variable, domain in problem._variables.items():
        patient_id = int(variable.split("_")[1])
        patient = find_patients(patients, patient_id)

        if patient.oxygen == True:

            def test_oxygen(a):
                bed_id = int(a.split("_")[1])
                bed = get_bed_by_id(beds, bed_id)
                return bed.room.oxygen

            problem.addConstraint(test_oxygen, [variable])

        if patient.telemetry == True:

            def test_telemetry(a):
                bed_id = int(a.split("_")[1])
                bed = get_bed_by_id(beds, bed_id)
                return bed.room.telemetry

            problem.addConstraint(test_telemetry, [variable])

    # Resolve o problema
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
