# **Error Suggestion**

### 📦 **Required Dependencies**
- `openai`
- `pandas`
- `numpy`
- `re`

---

## 🚀 **New: Graph-ChatGPT-Combined Error Suggestion Tool**
A tool that leverages graph algorithms and ChatGPT to diagnose and suggest fixes for command-line errors.

### **Steps to Run the Program**
1. **Navigate to the Project Directory:**
   ```bash
   cd gpt-graph-combined
   ```
2. **Execute the Main Program:**
   ```bash
   python ask-suggestion.py ../input_data/cleaned_data_02.csv ../input_data/error_suggestion.csv
   ```
3. **Locate the Output** in `../output_data/solutions.csv`.

### **Data preparation**
To run the program, input files could be prepared by programs in two jupyter notebooks in the `notebook` folder. `cleaned_data_02.csv` data is processed by `new_log_processor.ipynb` and `error_suggestion.csv` is processed by `new_error_graph.ipynb`.

---

## 🖥 **Original: Graph-Based Analysis**
### 🔍 **Repository Focus**
- **Version 1** of the repository is dedicated to error analysis via graph algorithms.
  Check out the original version [here](https://github.com/GuningShen/cyverse_error_analysis/tree/main).

### **Analysis Code**
- **[new_log_processor.ipynb](https://github.com/GuningShen/error-suggestion/blob/main/notebooks/new_log_processor.ipynb)**: Converts raw JSON logs into CSV or PKI format.
- **[new_error_graph.ipynb](https://github.com/GuningShen/error-suggestion/blob/main/notebooks/new_error_graph.ipynb)**: Applies graph algorithms to Bash shell error logs, simulating workflows leading to errors and subsequent commands.

## 🧮 **Graph Algorithm Explanation**
### **Node Attributes**
Each command is represented as a graph node with the following attributes:
- **Program**: The command name or script.
- **Type of Error**: The error encountered, if any.
- **Frequency**: The command's execution frequency.
- **Full Command Dictionary**: Details of the entire command.
- **Children Command Dictionary**: Commands that followed.

### **Graph Construction**
Two graphs can be constructed using this information:
1. **Graph 1**: Captures previous commands to predict errors.
2. **Graph 2**: Tracks subsequent commands to trace how users corrected their errors.

<p align="center">
  <img src="https://github.com/GuningShen/cyverse_error_analysis/assets/77816197/946d1f4f-7c17-48aa-aa10-65cbff4dcb1a" alt="error graph" width="300"/>
</p>

<p align="center">
  <img width="634" alt="Graph Analysis" src="https://github.com/GuningShen/cyverse_error_analysis/assets/77816197/48f2c937-74d3-4201-9ddc-f3c346d2c001">
</p>

## 🗃 **Data**
- **[output_data](https://github.com/GuningShen/error-suggestion/tree/main/output_data)**: Error logs in CSV or PKI format, processed by the Log Processor Guide.
