import sys

from py4j.java_gateway import JavaGateway


logfile = open("log.txt", "w")


class Graph:
    def __init__(self):
        self.nodes = []

    def find_or_create_concept_node(self, concept):
        for node in self.nodes:
            if node.has_concept(concept):
                return node

        node = Node()
        node.concepts.add(concept)
        self.nodes.append(node)
        return node


class Node:
    def __init__(self):
        self.concepts = set()
        self.succesors = set()  # (role, node)

    def add_or_create_concept(self, concept):
        if concept in self.concepts:
            return False

        self.concepts.add(concept)
        return True

    def add_or_find_successor(self, role, successor):
        for r, s in self.succesors:
            if (r, s) == (role, successor):
                return False

        self.succesors.add((role, successor))
        return True

    def has_concept(self, concept):
        return concept in self.concepts


class ELSolver:
    def __init__(self, ontology, gateway, elfactory):
        self.graph = Graph()
        self.gateway = gateway
        self.elfactory = elfactory
        self.formatter = gateway.getSimpleDLFormatter()
        self.input_concepts = ELSolver.extract_input_concepts(ontology)
        self.axioms = ontology.tbox().getAxioms()

    @staticmethod
    def extract_input_concepts(ontology):
        allConcepts = ontology.getSubConcepts()
        return set(concept for concept in allConcepts)

    def solve(self, lhs_concept, rhs_concept):
        lhs_node = self.populate_graph(lhs_concept)
        return rhs_concept in lhs_node.concepts

    def print_graph(self):
        logfile.writelines(["PRINTING GRAPH\n"])
        for node in self.graph.nodes:
            logfile.writelines(["Node:\n"])
            logfile.writelines(
                [self.formatter.format(concept) for concept in node.concepts]
            )
            logfile.writelines(["\n"])
            # print([self.formatter.format(concept) for concept in node.concepts])

    def populate_graph(self, init_concept):
        changed = True
        start_node = self.graph.find_or_create_concept_node(init_concept)

        while changed:
            changed = False

            for node in self.graph.nodes:
                changed = self.apply_rules(node) or changed

        return start_node

    def apply_rules(self, node):
        changed = False
        rules = [
            self.conj1rule,
            self.conj2rule,
            self.ex1rule,
            self.ex2rule,
            self.subrule,
        ]

        for rule in rules:
            changed = rule(node) or changed
            # print(rule, changed)

        self.print_graph()

        return changed

    def conj1rule(self, node):
        changed = False
        new_concepts = []

        for concept in node.concepts:
            conceptType = concept.getClass().getSimpleName()
            if conceptType != "ConceptConjunction":
                continue

            conjuncts = concept.getConjuncts()

            for conjunct in conjuncts:
                if conjunct not in self.input_concepts:
                    continue

                new_concepts.append(conjunct)

        for conjunct in new_concepts:
            changed = node.add_or_create_concept(conjunct) or changed

        return changed

    def conj2rule(self, node):
        # Can be optimized
        changed = False
        new_concepts = []
        for c1 in node.concepts:
            for c2 in node.concepts:
                if c1 == c2:
                    continue

                conj = self.elfactory.getConjunction(c1, c2)

                if conj in self.input_concepts:
                    new_concepts.append(conj)

        for conj in new_concepts:
            changed = node.add_or_create_concept(conj) or changed

        return changed

    def ex1rule(self, node):
        changed = False
        new_successors = []
        for concept in node.concepts:
            conceptType = concept.getClass().getSimpleName()
            if conceptType != "ExistentialRoleRestriction":
                continue

            role = concept.role()
            concept = concept.filler()

            if concept in self.input_concepts:
                succesor = self.graph.find_or_create_concept_node(concept)
                new_successors.append((role, succesor))

        for r, s in new_successors:
            changed = node.add_or_find_successor(r, s) or changed

        return changed

    def ex2rule(self, node):
        changed = False
        new_concepts = []

        for r, succ in node.succesors:
            for c2 in succ.concepts:
                ex = self.elfactory.getExistentialRoleRestriction(r, c2)
                if ex in self.input_concepts:
                    new_concepts.append(ex)

        for ex in new_concepts:
            changed = node.add_or_create_concept(ex) or changed

        return changed

    def subrule(self, node):
        changed = False
        new_concepts = []

        for concept in node.concepts:
            for axiom in self.axioms:
                if axiom.getClass().getSimpleName() != "GeneralConceptInclusion":
                    continue

                c1 = axiom.lhs()
                c2 = axiom.rhs()

                if c1 == concept:
                    new_concepts.append(c2)

        for c in new_concepts:
            changed = node.add_or_create_concept(c) or changed

        return changed


def read_ontology(gateway, filepath):
    parser = gateway.getOWLParser()
    ontology = parser.parseFile(filepath)
    return ontology


def clean_ontology(gateway, elfactory, ontology):
    new_ontology = gateway.jvm.nl.vu.kai.dl4python.datatypes.Ontology()

    for axiom in ontology.tbox().getAxioms():
        axiomType = axiom.getClass().getSimpleName()

        match axiomType:
            case "GeneralConceptInclusion":
                new_ontology.tbox().add(axiom)
            case "EquivalenceAxiom":
                c1 = axiom.lhs()
                c2 = axiom.rhs()
                new_ontology.tbox().add(elfactory.getGCI(c1, c2))
                new_ontology.tbox().add(elfactory.getGCI(c2, c1))

    return new_ontology


def get_all_concept_names(ontology):
    allConcepts = ontology.getSubConcepts()
    res = []

    for concept in allConcepts:
        conceptType = concept.getClass().getSimpleName()
        if conceptType == "ConceptName":
            res.append(concept)

    return res


def create_mock_ontology(gateway, elfactory):
    cA = elfactory.getConceptName("A")
    cB = elfactory.getConceptName("B")
    cC = elfactory.getConceptName("C")
    cD = elfactory.getConceptName("D")
    cE = elfactory.getConceptName("E")
    cF = elfactory.getConceptName("F")
    cG = elfactory.getConceptName("G")

    r1 = elfactory.getRole("r")
    r2 = elfactory.getRole("s")

    cn1 = elfactory.getConjunction(cC, cG)

    ex1 = elfactory.getExistentialRoleRestriction(r1, cC)
    ex2 = elfactory.getExistentialRoleRestriction(r2, cE)
    ex3 = elfactory.getExistentialRoleRestriction(r2, cF)
    ex4 = elfactory.getExistentialRoleRestriction(r1, cn1)

    cn2 = elfactory.getConjunction(cD, ex2)

    gci1 = elfactory.getGCI(cA, ex1)
    gci2 = elfactory.getGCI(cC, cn2)
    gci3 = elfactory.getGCI(cE, cF)
    gci4 = elfactory.getGCI(ex3, cG)
    gci5 = elfactory.getGCI(ex4, cB)

    ontology = gateway.jvm.nl.vu.kai.dl4python.datatypes.Ontology()
    ontology.tbox().add(gci1)
    ontology.tbox().add(gci2)
    ontology.tbox().add(gci3)
    ontology.tbox().add(gci4)
    ontology.tbox().add(gci5)

    return ontology


def main():
    gateway = JavaGateway()
    elfactory = gateway.getELFactory()
    formatter = gateway.getSimpleDLFormatter()

    filepath = sys.argv[1]
    subsumee = elfactory.getConceptName(sys.argv[2])

    # ontology = create_mock_ontology(gateway, elfactory)
    ontology = read_ontology(gateway, filepath)
    ontology = clean_ontology(gateway, elfactory, ontology)
    print_ontology(logfile, formatter, ontology)

    for concept in get_all_concept_names(ontology):
        solver = ELSolver(ontology, gateway, elfactory)
        res = solver.solve(subsumee, concept)
        logfile.writelines(
            ["===============================================================\n"]
        )
        logfile.writelines(
            [
                f"Checking {formatter.format(concept)} subsumes {formatter.format(subsumee)} {res}\n"
            ]
        )
        if res:
            print(formatter.format(concept))

    logfile.close()


def print_ontology(logfile, formatter, ontology):
    for axiom in ontology.tbox().getAxioms():
        logfile.writelines([formatter.format(axiom), "\n"])


if __name__ == "__main__":
    main()
