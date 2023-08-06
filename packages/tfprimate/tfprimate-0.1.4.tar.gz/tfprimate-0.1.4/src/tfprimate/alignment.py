from pymsaviz import MsaViz

def detect_msa_format(msa_path):
    """Detects the format of a multipe sequence alignment (MSA) file.

    Args:
        msa_path (str): The file path of MSA file.

    Returns:
        str: The detected format of the MSA file. Possible values are 'fasta', 'clustal', 'emboss', 'phylip', or 'Unknown'.
    """

    with open(msa_path, 'r') as file:
        first_line = file.readline().strip()
        if first_line.startswith('>'):
            return 'fasta'
        elif first_line.startswith('CLUSTAL') or first_line.startswith('MUSCLE'):
            return 'clustal'
        elif first_line.startswith('#') and 'EMBOSS' in first_line.upper():
            return 'emboss'
        elif first_line.isdigit():
            second_line = file.readline().strip()
            if second_line.isdigit():
                return 'phylip'
        return 'Unknown'


def draw_msa(msa_path, msa_format):
    """Draws a visualization of the multiple sequence alignment (MSA).

    Args:
        msa_path (str): The path of MSA file.
        msa_format (str): The format of the MSA file.

    Returns:
        MsaViz: An instance of the MsaViz class representing the MSA visualization.
    """
    
    mv = MsaViz(
        msa_path,
        format=msa_format,
        wrap_length=100,
        show_consensus=True,
        show_count=True,
        consensus_color='#A3E4D7'
    )

    # extract MSA positions less than 50% consensus identity
    pos_ident_less_than_50 = []
    ident_list = mv._get_consensus_identity_list()
    for pos, ident in enumerate(ident_list, 1):
        if ident <= 50:
            pos_ident_less_than_50.append(pos)

    # add markers
    mv.add_markers(pos_ident_less_than_50, marker='x', color='red')
    
    # mv.plotfig()
    # mv.savefig("figure.png", dpi=200)

    return mv

if __name__=="__main__":
    
    msa_path = "../../data/NANOG.fa.aligned"
    msa_format = detect_msa_format(msa_path)
    mv = draw_msa(msa_path, msa_format)
    #mv.savefig("test.png", dpi=200)

