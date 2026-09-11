from Bio import SeqIO

SECTION_2_AGENTS = [
    {"name": "Sequence Reader", "job": "parse DNA sequences and compute basic statistics"},
    {"name": "Pattern Finder", "job": "find motifs and patterns in DNA sequences"}
]

def read_sequences(filepath):
    sequences = []
    for record in SeqIO.parse(filepath, "fasta"):
        sequences.append({
            "id": record.id,
            "length": len(record.seq),
            "gc_content": round(
                (record.seq.count("G") + record.seq.count("C")) / len(record.seq) * 100, 2
            )
        })
    return sequences

def find_motif(sequence, motif):
    positions = []
    start = 0
    while True:
        index = sequence.find(motif, start)
        if index == -1:
            break
        positions.append(index)
        start = index + 1
    return positions


if __name__ == "__main__":
    sequences = read_sequences("sample_sequences.fasta")
    print(sequences)

    seq1_string = "ATCGGCTAATCGATCG"  # same as seq1 in your FASTA file
    print(find_motif(seq1_string, "ATC"))

