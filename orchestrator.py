from agents.section1_intake import detect_file_type, check_data_quality
from agents.section2_sequence import read_sequences, find_motif
from agents.section3_stats import analyze_statistics, find_outliers
from agents.section5_reporting import write_report

def run_pipeline(filepath):
    file_type = detect_file_type(filepath)

    if file_type == "sequence":
        sequences = read_sequences(filepath)
        first_sequence = str(sequences[0]) if sequences else ""
        motifs = find_motif(first_sequence, "ATG")
        section_results = {
            "file_type": file_type,
            "sequences": sequences,
            "motif_positions": motifs
        }

    elif file_type == "tabular":
        quality_report = check_data_quality(filepath)
        stats = analyze_statistics(filepath, "value")
        outliers = find_outliers(filepath, "value")
        section_results = {
            "file_type": file_type,
            "quality": quality_report,
            "stats": stats,
            "outliers": outliers
        }

    else:
        return f"Sorry, I don't know how to analyze files of type: {file_type}"

    report = write_report(section_results)
    return report

if __name__ == "__main__":
    result = run_pipeline("sample_data.csv")
    result = run_pipeline("sample_sequences.fasta")
    print(result)