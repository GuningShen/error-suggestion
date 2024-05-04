# Error Suggestion

## Part 1: Graph-ChatGPT-Combined error suggestion tool
A tool that provides suggestions to diagnose and fix command-line errors based on graph algorithm and chatGPT.

## How to Run the Program
1. Navigate to the project directory:
   ```bash
   cd gpt-graph-combined
   ```
2. Run the main program:
   ```bash
   python compared.py ../output_data/cleaned_data_02.csv ../output_data/error_suggestion.csv
   ```
3. Find the output in `../output_data/solutions.csv`.

## Part 2: Graph-based Analysis
**Note:** Version 1 of the repository focuses on error analysis by graph algorithm. You can check it out [here](https://github.com/GuningShen/cyverse_error_analysis/tree/main).

## Analysis Code
- **[Log_Processor_Guide.ipynb](https://github.com/GuningShen/cyverse_tutorial/blob/main/Log_Processor_Guide.ipynb)**: Code to convert raw JSON-format logs into CSV or PKI format.
- **[Error_Analyzer.ipynb](https://github.com/GuningShen/cyverse_tutorial/blob/main/Error_Analyzer.ipynb)**: A detailed, level-by-level breakdown analysis for shell logs.
- **[Error_Tree.ipynb](https://github.com/GuningShen/cyverse_tutorial/blob/main/Error_Tree.ipynb)**: Uses a graph algorithm to analyze Bash shell error logs, constructing a model that simulates workflows leading to errors and subsequent commands.

## Graph Algorithm Explanation
Each command is represented as a graph node with the following attributes:
- **Program**: The command name or script.
- **Type of Error**: The error encountered, if any.
- **Frequency**: How often the command was executed.
- **Full Command Dictionary**: Details of the entire command.
- **Children Command Dictionary**: Commands that followed.

<p align="center">
  <img src="https://github.com/GuningShen/cyverse_error_analysis/assets/77816197/946d1f4f-7c17-48aa-aa10-65cbff4dcb1a" alt="error graph" width="270"/>
</p>

Using this information, two graphs can be constructed:
1. **Graph 1**: Captures previous commands to predict errors.
2. **Graph 2**: Captures subsequent commands to trace how users corrected their errors.

<p align="center">
  <img width="634" alt="Graph Analysis" src="https://github.com/GuningShen/cyverse_error_analysis/assets/77816197/48f2c937-74d3-4201-9ddc-f3c346d2c001">
</p>

## Data
- **[raw_data](https://github.com/GuningShen/cyverse_tutorial/tree/main/raw_data)**: Raw Bash shell error logs in JSON format.
- **[output_data](https://github.com/GuningShen/cyverse_tutorial/tree/main/output_data)**: Error logs in CSV or PKI format processed by the Log Processor Guide.
- **[error_processed_data](https://github.com/GuningShen/cyverse_tutorial/tree/main/error_processed_data)**: Output data from Error_Analyzer.ipynb, serving as input for Error_Tree.ipynb.
