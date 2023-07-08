from wiki.singleton import SectionTree


# Defining a function to return the section tree
def navbar_footer(request):
    # Creating an instance of SectionTree and getting the tree
    section_tree = SectionTree().tree
    # Returning the section tree
    return {"section_tree": section_tree}
