# biopyassistant-sandbox

This is a sandbox repository for the BiopyAssistant project. It contains external data files and scripts that are used for testing, analysis and development purposes.


## Installation

To install BioPyAssistant-sanbox and its dependencies, run the following commands:

Clone the repository:

```bash
git clone https://github.com/pierrepo/biopyassistant-sandbox.git
cd biopyassistant-sandbox
```

Create a Conda environment:

```bash
conda env create -f environment.yml
```

Create a `.env` file with a valid OpenAI API key:

```text
OPENAI_API_KEY=<your-openai-api-key>
```

> Remark: The `.env` file is ignored by git.


## Usage

### Activate the Conda Environment

Activate the Conda environment by running:

```bash
conda activate biopyassistant-sandbox-env
```

### Process the Data

Process the data by running:

```bash
python src/parse_clean_markdown.py --in data/markdown_raw --out data/markdown_processed
```

This command will process Markdown files located in the `data/markdown_raw` directory and save the processed files to the `data/markdown_processed` directory.

### Create Chroma DB

Create the Chroma database by running:

```bash
python src/create_database.py --data_dir [data_dir] --chroma_out [chroma_output] --chunk_size [chunk_size] --chunk_overlap [chunk_overlap] 
```
Where :
- `[data_dir]` (optional): Directory containing processed Markdown files. Default: `data/markdown_processed`.
- `[chroma_output]` (optional): Output path to save ChromaDB database. Default: `chroma_db`.
- `[chunk_size]` (optional): Size of text chunks to create. Default: 600.
- `[chunk_overlap]` (optional): Overlap between text chunks. Default: 100.

Example:
  
```bash
python src/create_database.py --data_dir data/markdown_processed --chroma_out chroma_db --chunk_size 500 --chunk_overlap 50
```
This command will create a Chroma database from the processed Markdown files located in the `data/markdown_processed` directory. The text will be split into chunks of 500 characters with an overlap of 50 characters. And finally the Chroma database will be saved to the `chroma_db` directory.

> Remark: The vector database will be saved on the disk.

### Get Chunk Statistics

To save the details of each chunk to a text file and the number of tokens and chunks for each file to a CSV file, you can run:

```bash
python src/get_chunk_stats.py --data-path [data-path] --chroma-path [chroma-path] [--txt-output <txt-output>] [--csv-output <csv-output>]
```

Where:
- [data-path]: Path to the Markdown files.
- [chroma-path]: Path to the Chroma database.
- [--txt-output] (optional): Name of the output text file to save the chunks with metadata.
- [--csv-output] (optional): Name of the output CSV file to save the number of tokens and chunks for each Markdown file.

> **Note:** Make sure that the `data-path` matches the `data-path` used in the creation of the Chroma database. For more information, refer to [Create Chroma DB](#create-chroma-db).


Example:

```bash
python src/get_chunk_stats.py --data-path data/markdown_processed --chroma-path chroma_db
```

This command command will load the processed Markdown files from the `data/markdown_processed` directory and load the Chroma database from the `chroma_db` directory. 
And save the details of each chunk to a text file named `chroma_db_chunks_details.txt` and the number of tokens and chunks for each file to a CSV file named `chroma_db_stats.csv`.


### Analysis

#### Embeddings :

Run the Jupyter notebook `src/analysis_embeddings.ipynb` to visualize embeddings in a 2D and 3D.


#### Chunk size

Run the jupyter notebook `src/analysis_chunk_size.ipynb` to analyze the impact of the chunk size on the performance of the RAG model.

> Remark: The notebook requires the creation of Chroma databases with different chunk sizes (200, 400, 600, 800, 1000, 1500, 2000 and 3000). The databases should be saved in the `chroma_db_x` directory where `x` is the chunk size.

