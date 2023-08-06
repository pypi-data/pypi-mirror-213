from Bio import Phylo

# can also consider ETE toolkit

def drawPhyloTree(tree_file, tree_format):
    
    tree = Phylo.read(tree_file, format=tree_format)
    phylo_tree = Phylo.draw_ascii(tree)

    return phylo_tree
    

if __name__ == "__main__":
    tree_input = input("tree_file and tree_format: ")
    d = drawPhyloTree(tree_input[0], tree_input[1])
    print(d)
