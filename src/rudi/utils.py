import ifcopenshell as ifc

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