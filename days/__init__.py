import os.path


def path_to_input(filename: str):
    inputs_directory = os.path.dirname(__file__)
    return os.path.join(inputs_directory, f'inputs/{filename}')


def path_to_output(filename: str):
    inputs_directory = os.path.dirname(__file__)
    return os.path.join(inputs_directory, f'outputs/{filename}')

