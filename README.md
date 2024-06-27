# biopyassistant-sandbox

This is a sandbox repository for the BiopyAssistant project. It contains external data files and scripts that are used for testing, analysis and development purposes.


## Installation

To install BioPyAssistant-sanbox and its dependencies, run the following commands:

Clone the repository:

```bash
git clone https://github.com/pierrepo/biopyassistant-sandbox.git
cd biopyassistant-sandbox
```


Install Conda:

To install Conda, follow the instructions provided in the official [Conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Create a Conda environment:

```bash
conda env create -f environment.yml
```


## Usage

### Step 1: Activate the Conda Environment

Activate the Conda environment by running:

```bash
conda activate biopyassistant-sandbox-env
```

### Step 2: Process the course content

Process the course content by running:

```bash
python src/parse_clean_markdown.py --in data/markdown_raw --out data/markdown_processed
```

This command will process Markdown files located in the `data/markdown_raw` directory and save the processed files to the `data/markdown_processed` directory.

### Step 3: Set up OpenAI API key

Create a `.env` file with a valid OpenAI API key:

```text
OPENAI_API_KEY=<your-openai-api-key>
```

> Remark: This `.env` file is ignored by git.

### Step 4: Create the Vector Database

Create the Vector database by running:

```bash
python src/create_database.py --data-path [data-path] --chroma-path [chroma-path] --chunk-size [chunk-size] --chunk-overlap [chunk-overlap] 
```
Where :
- `[data-path]` (mandatory): Directory containing processed Markdown files.
- `[chroma-path]` (mandatory): Output path to save the vectorial ChromaDB database.
- `[chunk-size]` (optional): Size of text chunks to create. Default: 1000.
- `[chunk-overlap]` (optional): Overlap between text chunks. Default: 200.

Example:
  
```bash
python src/create_database.py --data-path data/markdown_processed --chroma-path chroma_db
```
This command will create a vectorial Chroma database from the processed Markdown files located in the `data/markdown_processed` directory. The text will be split into chunks of 1000 characters with an overlap of 200 characters. And finally the vectorial Chroma database will be saved to the `chroma_db` directory.

> Remark: The vector database will be saved on the disk.


### Analysis

#### Get Chunk Statistics

To save the details of each chunk to a text file and the number of tokens and chunks for each file to a CSV file, you can run:

```bash
python src/get_chunk_stats.py --data-path [data-path] --chroma-path [chroma-path]
```

Where:
- [data-path]: Path to the Markdown files.
- [chroma-path]: Path to the Chroma database.

> **Note:** Make sure that the `data-path` matches the `data-path` used in the creation of the Chroma database. For more information, refer to [Create the vectorial DB](#step-4-create-the-vector-database).


Example:

```bash
python src/analysis/get_chunk_stats.py --data-path data/markdown_processed --chroma-path chroma_db
```

This command command will load the processed Markdown files from the `data/markdown_processed` directory and load the Chroma database from the `chroma_db` directory. 
It will then save the details of each chunk to a text file and the number of tokens and chunks for each file to a CSV file.


#### Embeddings :

Run the Jupyter notebook `src/analysis/analysis_embeddings.ipynb` to visualize embeddings in a 2D and 3D.


#### Chunk size

Run the jupyter notebook `src/analysis/analysis_chunk_size.ipynb` to analyze the impact of the chunk size on the performance of the RAG model.

> Remark: The notebook requires the creation of Chroma databases with different chunk sizes (200, 400, 600, 800, 1000, 1500, 2000 and 3000). The databases should be saved in the `chroma_db_x` directory where `x` is the chunk size.

