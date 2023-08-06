from ottrlib.model import Iri
from ottrlib.Ottr import Ottr


def tryit():
    stottr_input = """
    ax:SubClassOf [ ?sub, ?super ] :: {
        ottr:Triple(?sub, rdfs:subClassOf, ?super)
    } .

    pz:Pizza [ ?identifier, ?label ] :: {
        ottr:Triple(?identifier, rdf:type, owl:Class),
        ax:SubClassOf(?identifier, p:Pizza),
        ottr:Triple(?identifier, rdfs:label, ?label)
    } .

    pz:Pizza(p:Margherita, "Margherita") .
    pz:Pizza(p:Hawaii, "Hawaii") .
    pz:Pizza(p:Grandiosa, "Grandiosa") .
    """

    pyottr = Ottr()
    for triple in pyottr.expand(stottr_input):
        print(triple)

    print()
    for triple in pyottr.expand('pz:Pizza(p:Pepperoni, "Pepperoni") .'):
        print(triple)

    print()
    data = [
        (Iri("p:Capricciosa"), "Capricciosa"),
        (Iri("p:Marinara"), "Marinara"),
        (Iri("p:Crudo"), "Crudo"),
    ]
    for triple in pyottr.apply("pz:Pizza").to(data):
        print(triple)
