from langgraph.graph import StateGraph, END

from typing import TypedDict, Optional

class PipelineState(TypedDict):
    filepath: str
    file_type: Optional[str]
    quality_report: Optional[dict]
    stats: Optional[dict]
    outliers: Optional[list]
    sequences: Optional[list]
    motifs: Optional[list]
    final_report: Optional[str]

from agents.section1_intake import detect_file_type, check_data_quality
from agents.section2_sequence import read_sequences, find_motif
from agents.section3_stats import analyze_statistics, find_outliers
from agents.section5_reporting import write_report

def detect_node(state: PipelineState) -> PipelineState:
    file_type = detect_file_type(state["filepath"])
    return {"file_type": file_type}

def tabular_node(state: PipelineState) -> PipelineState:
    quality = check_data_quality(state["filepath"])
    stats = analyze_statistics(state["filepath"], "value")
    outliers = find_outliers(state["filepath"], "value")
    return {"quality_report": quality, "stats": stats, "outliers": outliers}

def sequence_node(state: PipelineState) -> PipelineState:
    sequences = read_sequences(state["filepath"])
    first_sequence = str(sequences[0]) if sequences else ""
    motifs = find_motif(first_sequence, "ATG")
    return {"sequences": sequences, "motifs": motifs}

def report_node(state: PipelineState) -> PipelineState:
    relevant_data = {k: v for k, v in state.items() if k not in ["filepath", "final_report"]}
    report = write_report(relevant_data)
    return {"final_report": report}

def route_by_file_type(state: PipelineState) -> str:
    if state["file_type"] == "sequence":
        return "sequence_node"
    elif state["file_type"] == "tabular":
        return "tabular_node"
    else:
        return END
    
graph = StateGraph(PipelineState)
graph.add_node("detect_node", detect_node)
graph.add_node("tabular_node", tabular_node)
graph.add_node("sequence_node", sequence_node)
graph.add_node("report_node", report_node)

graph.set_entry_point("detect_node")
graph.add_conditional_edges("detect_node", route_by_file_type)
graph.add_edge("tabular_node", "report_node")
graph.add_edge("sequence_node", "report_node")
graph.add_edge("report_node", END)

app_graph = graph.compile()

def run_pipeline(filepath):
    result = app_graph.invoke({"filepath": filepath})
    return result.get("final_report", "No report generated.")

if __name__ == "__main__":
    result = run_pipeline("sample_data.csv")
    print(result)




