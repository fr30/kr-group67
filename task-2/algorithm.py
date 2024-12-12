import sys
from py4j.java_gateway import JavaGateway
from time import process_time
import multiprocessing
from functools import partial



# El Completion Algorithm (Description Logics 3: slide 26/40 & 23/40)

# Remove this line and uncomment "if __name__ == main" when handing in !!!!
owl_ontology = "hamburger_restaurant.owx"  # Loading pizza.owl file for testing purposes

# Python to Java setup
gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()

# Ontology & Converting to binary conjunctions
ontology = parser.parseFile(owl_ontology)  # Pizza for testing algorithm
gateway.convertToBinaryConjunctions(ontology)  # Binary conjunctions

axioms = set(ontology.tbox().getAxioms())  # Set of axioms
concepts = set(ontology.getConceptNames())  # Set of concepts
subconcepts = ontology.getSubConcepts()
elFactory = gateway.getELFactory()


class Element:
    """
    Element class that holds the initial element, concepts related to element, and role successors
    """

    def __init__(self, init_element):
        self.init = init_element
        self.concepts = {init_element}
        self.succ = dict()


def replace_equivalence():
    """
    Removes all axioms in form of A ≡ B
    Adds axioms A ⊑ B, B ⊑ A
    """
    equivalences = [axiom for axiom in axioms if axiom.getClass().getSimpleName() == "EquivalenceAxiom"]
    for axiom in equivalences:
        ax_concepts = axiom.getConcepts()
        axioms.remove(axiom)  # Removing the EquivalenceAxiom
        gci_1 = elFactory.getGCI(ax_concepts[0], ax_concepts[1])  # Creating 2 General Concept Inclusions
        gci_2 = elFactory.getGCI(ax_concepts[1], ax_concepts[0])
        axioms.add(gci_1), axioms.add(gci_2)


def algorithm(sub):
    """"
    Finds all subsumer elements such that
    sub ⊑ subsumer
    Applies completion rules exhaustively on all elements in individuals[]
    """
    replace_equivalence()
    subsumee = elFactory.getConceptName(sub)  # Converting to java object
    d0 = Element(subsumee)  # Assigning subsumee to d0
    individuals = [d0]
    changed = True
    while changed:
        changed = False
        for d in individuals:
            changed = apply_rules(d, individuals)  # for every individual, we apply the rules
    for subsumer in d0.concepts:  # apply_rules returned false because no change was made
        if subsumer.getClass().getSimpleName() in ["ConceptName", "TopConcept$"]:  # Returns 1 less than the ELk reasoner in exemple.py
            print(subsumer)

def conceptconj(concept, individual):
    for x in concept.getConjuncts():
        if x in subconcepts:
            individual.concepts.add(x)

def conceptconj2(individual, concept, assigned_concepts):
    for concept_2 in assigned_concepts:
        if concept != concept_2:
            conj = elFactory.getConjunction(concept, concept_2)
            if conj in subconcepts:
                individual.concepts.add(conj)

def exist(individual, concept, individuals):
    role, filler = concept.role(), concept.filler()  # ∃role.filler
    exist_successor = False
    for e in individuals:
        if filler == e.init:  # check if there is element e with e.init == filler
            individual.succ[role] = e  # e is role-successor of individual
            exist_successor = True
            break
            # Unsure if we should brake here. Can an individual have more role successors that
            # have filler as init concept? see algorithm_1.py
    if not exist_successor:  # No element found
        successor = Element(filler)  # make new element, which is role successor of individual
        individual.succ[role] = successor
        individuals.append(successor)

# !!!
def gci(individual, concept, axiom):
    if axiom.getClass().getSimpleName() == "GeneralConceptInclusion" and axiom.lhs() == concept:
        if subconcepts.contains(axiom.rhs()):
            individual.concepts.add(axiom.rhs())  # we add the right side


def exist2(individual):
    for ROLE in individual.succ:  # check role successors of individual
        for conc in individual.succ[ROLE].concepts:
            fill = conc
            axiom = elFactory.getExistentialRoleRestriction(ROLE, fill)  # Create existential role restriction
            if axiom in subconcepts:
                individual.concepts.add(axiom)  # Add to d


def apply_rules(individual, individuals):
    """
    Applies all el completion rules
    returns True if concept_individual_counter is increased after applying rules
    otherwise False
    """
    concept_individual_counter = sum(len(x.concepts) for x in individuals) + len(individuals)

    # ⊤-RULE
    individual.concepts.add(elFactory.getTop())

    # Apply all rules for every concept in d
    assigned_concepts = individual.concepts.copy()

    for concept in assigned_concepts:
        name = concept.getClass().getSimpleName()

        # Conjunction Rule 1
        if name == "ConceptConjunction":
            #  individual.concepts.update(set(concept.getConjuncts()).intersection(subconcepts))
            conceptconj(concept, individual)

        # Conjunctin Rule 2
        conceptconj2(individual, concept, assigned_concepts)

        # ∃-RULE 1
        if name == "ExistentialRoleRestriction":
            exist(individual, concept, individuals)

        # GCI RULE
        # if name == 'ConceptName':  # Only concept name so looking for General Concept Inclusion rule
        axioms_list = list(axioms)
        pool = multiprocessing.Pool()
        func = partial(gci, individual, concept)
        pool.map(func, axioms_list)
        pool.close()
        pool.join()

    # ∃-RULE 2
    exist2(individual)
    return concept_individual_counter != (sum(len(x.concepts) for x in individuals) + len(individuals))

t = process_time()
algorithm("BigMacBurger")
print(process_time()- t)
# for x in ontology.tbox().getAxioms():
#     print(x)
# Uncomment this when handing in 
# if __name__ == "__main__":
#     owl_ontology = sys.argv[1]
#     subsumee = sys.argv[2]
#     algorithm(subsumee, owl_ontology)
#[MeatyBurger, Hamburger, CheesyBurger, Food, NamedBurger, TOP, BigMacBurger, Restaurant]