Still building the workspace index, response may be less accurate.

# ELSolver README

## Overview

ELSolver is a reasoner that computes all subsumers for a given class name within an ontology. The reasoner can be executed from the command line and outputs all class names from the ontology that are subsumers of the specified class.

## Usage

### dl4python server
Before running anything make sure dl4python server is running with the command

```sh
java -jar dl4python-0.1-jar-with-dependencies.jar
```

### Running ELSolver

To run the ELSolver, use the following command:

```sh
python main.py ONTOLOGY_FILE CLASS_NAME
```

- `ONTOLOGY_FILE`: Path to the ontology file in OWL format.
- `CLASS_NAME`: The name of the class for which you want to compute the subsumers.

The output will be a list of class names, one per line, that are subsumers of the specified class. The logs will be stored in `log.txt` file.

### Example

```sh
python main.py ontology/burgers_ontology_v1.rdf "Burger"
```

### Running the Testing Script

To test whether your reasoner fulfills the requirements, you can use the provided evaluation tool. Run the following command:

```sh
python evaluateReasonerStudents.py REASONER_FILE_NAME
```

- `REASONER_FILE_NAME`: Path to the reasoner script, typically 

main.py

.

### Example

```sh
python evaluateReasonerStudents.py main.py
```

If the reasoner is successful, the last line of the output should say "True".
