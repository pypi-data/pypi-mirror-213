import re

from Bio import SeqIO

# we ignore the X marking as they are unknown amino acids
ATOM_TO_HYDROPHOBICITY = {
    'G': 'H',
    'A': 'H',
    'V': 'H',
    'L': 'H',
    'I': 'H',
    'P': 'H',
    'F': 'H',
    'M': 'H',
    'W': 'H',
    'S': 'P',
    'T': 'P',
    'C': 'P',
    'N': 'P',
    'Q': 'P',
    'Y': 'P',
    'X': 'P',
    'R': 'P',
    'H': 'P',
    'K': 'P',
    'D': 'P'
}

d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
         'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
         'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
         'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M',
         }


class InputHandler:
    @staticmethod
    def extract_hydropolar_sequence_from_pdb(file_name):
        """
                Extracts the hydropolar sequence of an amino acid chain from a PDB file.

                Args:
                    file_name (str): The path to the PDB file.

                Returns:
                    str: The hydropolar sequence of the amino acid chain.
                """
        amino_acid_sequence = ""
        previous_chain = ""
        with open(file_name) as f:
            for matched_line in re.findall('^SEQRES.*$', f.read(), re.MULTILINE):
                tokens = matched_line.split()
                chain = tokens[2]
                if previous_chain != "" and chain != previous_chain:
                    print(
                        "Warning: The model works only with single-chain proteins. "
                        "The input will be truncated to use the first chain. ")
                    break
                tokens = tokens[4:]
                amino_acid_sequence = ''.join([d3to1[t] if t in d3to1.keys() else '' for t in tokens])
                amino_acid_sequence = ''.join([ATOM_TO_HYDROPHOBICITY[t] for t in amino_acid_sequence])
                previous_chain = chain

        return amino_acid_sequence

    @staticmethod
    def extract_hydropolar_sequence_from_fasta(file_name):
        """
                Extracts the hydropolar sequence of an amino acid chain from a FASTA file.

                Args:
                    file_name (str): The path to the FASTA file.

                Returns:
                    str: The hydropolar sequence of the amino acid chain.
                """
        amino_acid_sequence = ""
        index = 0
        for seq_record in SeqIO.parse(file_name, "fasta"):
            if index > 0:
                print(
                    "Warning: The model works only with single-chain proteins. "
                    "The input will be truncated to use the first chain. ")
                break
            sequence = seq_record.seq
            amino_acid_sequence = ''.join([ATOM_TO_HYDROPHOBICITY[t] for t in sequence])
            index += 1

        return amino_acid_sequence

seq = InputHandler.extract_hydropolar_sequence_from_fasta('/Users/ancaioanamuscalagiu/Documents/licenta/ProteinFolding/known_proteins/fasta/rcsb_pdb_1A1P.fasta')

print(seq)