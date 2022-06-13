import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import os

def get_related_property_sets(ifc_instance):
    """
    Renvoie une liste de IfcPropertySets pour une instance ifc donnée
    argument: ifc_instance
    return: liste de property sets
    """
    properties_list = []
    for x in ifc_instance.IsDefinedBy:
        if x.is_a("IfcRelDefinesByProperties"):
            if x.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                properties_list.append(x.RelatingPropertyDefinition)
    return properties_list

def totemification(ifc_file):
    file = ifcopenshell.open(ifc_file)
    products = [product for product in file.by_type("IfcProduct")]
    for product in products:
        if ifcopenshell.util.element.get_psets(product):
            for pset in get_related_property_sets(product):
                if pset.Name == "Pset_TOTEM":
                    for propriete in pset.HasProperties:
                        if propriete.Name == "Type_TOTEM":
                            product.Name = propriete.NominalValue.wrappedValue
    new_ifc_file = file
    #.write(os.path.basename(ifc_file)[0]+'TOTEMIZE'+os.path.basename(ifc_file)[1])
    return new_ifc_file
