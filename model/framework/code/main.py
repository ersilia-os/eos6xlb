# imports
import os
import csv
import sys
import yaml
import subprocess
import pandas as pd

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# my model
subprocess.run(["python", os.path.join(root, "gather_representation.py"),
	"--gpu", "cpu",
	"--output_filepath", output_file,
	"--smiles_filepath", input_file,
	"--smiles_colname", "smiles",
	"--chemid_colname", "smiles",
	"--representation", "gin_concat_R1000_E8000_lambda0.0001"], 
	stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Compare SMILES input and output
smiles_input = pd.read_csv(os.path.join(input_file), sep=',')['smiles'].tolist()
smiles_output = pd.read_csv(os.path.join(output_file), sep=',').iloc[:, 0].tolist()
assert smiles_input == smiles_output

# Change output format
output = pd.read_csv(os.path.join(output_file), sep=',')
output = output.iloc[:, 1:]
output.columns = [f"dim_{i:03d}" for i in range(len(output.columns))]
output.to_csv(output_file, sep=',', index=False)
