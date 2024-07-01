"""Save details of chunks to a text file and CSV file.
Usage:
------
    python src/analysis/get_chunk_stats.py --data_dir [data_dir] --chroma_path [chroma_path]
Arguments:
--------
    --data_dir : str
        The path to the directory containing the Markdown documents.
    --chroma_path : str
        The path to the directory containing the Chroma database.

Example:
--------
    python src/analysis/get_chunk_stats.py --chroma_path "chroma_db"

This command will load the Chroma database from the 'chroma_db' directory, reconstruct the chunks from the vector database, 
save the details of each chunk to a text file named 'chroma_db_chunks_details.txt' 
and save the id, the file name, the number of tokens and characters for each chunks to a CSV file named 'chroma_db_chunks_stats.csv'.
"""

# METADATA
__authors__ = ("Pierre Poulain", "Essmay Touami")
__contact__ = "pierre.poulain@u-paris.fr"
__copyright__ = "BSD-3 clause"
__date__ = "2024"
__version__ = "1.0.0"


# LIBRARY IMPORTS
import os
import sys
import argparse
from statistics import mean
from typing import List, Tuple

from loguru import logger
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

# MODULE IMPORTS
# Add the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from query_chatbot import load_database


# FUNCTIONS
def get_args() -> str:
    """Get the command line arguments.
    Returns
    -------
    chroma_path : str
        The path to the directory containing the Chroma database.
    """
    logger.info("Getting the command line arguments...")
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Save details of chunks to a text file and CSV file."
    )
    parser.add_argument(
        "--chroma_path",
        type=str,
        help="The path to the directory containing the Chroma database.",
    )
    # Parse the command line arguments
    args = parser.parse_args()

    # Check if the Chroma path is provided
    if args.chroma_path == None:
        logger.error(
            "Please specify the path to the directory containing the Chroma database."
        )
        sys.exit(1)

    # Check if the directories exist
    if not os.path.exists(args.chroma_path):
        logger.error(
            f"The directory '{args.chroma_path}' specified by --chroma_path does not exist."
        )
        sys.exit(1)  # Exit the program

    logger.success("Got the command line arguments successfully.\n")

    return args.chroma_path


def reconstruct_chunks(vector_db: Chroma) -> List[Document]:
    """Reconstruct the chunks from the vector database.
    Parameters
    ----------
    vector_db : Chroma
        The vector database to reconstruct the chunks.
    Returns
    -------
    chunks : list of Document
        List of text chunks reconstructed from the vector database.
        format : [{"page_content": str, "metadata": dict}, ...]
    """
    logger.info("Reconstructing the chunks from the vector database...")

    chunks = []
    vector_collections = vector_db.get()
    total_chunks = len(vector_collections["ids"])
    for i in range(total_chunks):
        chunk = {
            "page_content": vector_collections["documents"][i],
            "metadata": vector_collections["metadatas"][i],
        }
        # ** used to unpack a dictionary into keyword arguments.
        chunk = Document(**chunk)
        chunks.append(chunk)

    logger.success(
        f"Reconstructed {total_chunks} chunks from the vector database successfully.\n"
    )

    return chunks


def save_to_txt(chunks: List[Document], chroma_path: str) -> None:
    """Save text chunks to a text file with metadata.
    Parameters
    ----------
    chunks : list of Document
        List of text chunks to save to a text file.
    chroma_path : str
        The path to the directory containing the Chroma database.
    """
    logger.info(f"Saving into text file...")

    txt_output_path = chroma_path + "_chunks_details.txt"  # add .txt extension

    # Get statistics of the tokens for all the chunks
    all_tokens = sum(chunk.metadata.get("nb_tokens", 0) for chunk in chunks)
    mean_tokens = mean(chunk.metadata.get("nb_tokens", 0) for chunk in chunks)
    min_tokens = min(chunk.metadata.get("nb_tokens", 0) for chunk in chunks)
    max_tokens = max(chunk.metadata.get("nb_tokens", 0) for chunk in chunks)

    # Save the details of the chunks to a text file
    with open(txt_output_path, "w") as f:
        f.write("Chunks Details :\n\n")
        # statistics of the tokens for all the chunks
        f.write("Statistics of the tokens for all the chunks:\n")
        f.write(f"- Count : {all_tokens}\n")
        f.write(f"- Mean : {round(mean_tokens, 3)}\n")
        f.write(f"- Min : {min_tokens}\n")
        f.write(f"- Max : {max_tokens}\n\n")

        f.write("Statistics of the characters for all the chunks:\n")
        f.write(f"- Count : {sum(len(chunk.page_content) for chunk in chunks)}\n")
        f.write(f"- Mean : {round(mean(len(chunk.page_content) for chunk in chunks), 3)}\n")
        f.write(f"- Min : {min(len(chunk.page_content) for chunk in chunks)}\n")
        f.write(f"- Max : {max(len(chunk.page_content) for chunk in chunks)}\n\n")

        # sort the chunks by the id
        chunks = sorted(chunks, key=lambda x: x.metadata["id"])

        for chunk in chunks:
            f.write(f"Chunk id: {chunk.metadata['id']}\n")
            f.write(f"Number of Characters: {len(chunk.page_content)}\n")
            f.write(f"Number of Tokens: {chunk.metadata['nb_tokens']}\n")
            f.write(f"Url: {chunk.metadata['url']}\n")
            f.write(f"File Name: {chunk.metadata['file_name']}\n")
            f.write(f"Chapter Name: {chunk.metadata['chapter_name']}\n")
            if "section_name" in chunk.metadata:
                f.write(f"Section Name: {chunk.metadata.get('section_name', '')}\n")
            if "subsection_name" in chunk.metadata:
                f.write(
                    f"Subsection Name: {chunk.metadata.get('subsection_name', '')}\n"
                )
            if "subsubsection_name" in chunk.metadata:
                f.write(
                    f"Subsubsection Name: {chunk.metadata.get('subsubsection_name', '')}\n"
                )
            f.write(f"Content:\n")
            f.write(f"{chunk.page_content}\n\n")

    logger.success(
        f"Saved the details of each chunks successfully to '{txt_output_path}'.\n"
    )


def save_to_csv(
    chunks: List[Document],
    chroma_path: str,
) -> None:
    """Save details of the chunks to a CSV file.

    Parameters
    ----------
    chunks : list of Document
        List of text chunks to save to a CSV file.
    chroma_path : str
        The path to the directory containing the Chroma database.
    """
    logger.info(f"Saving into CSV file...")
    csv_output_path = chroma_path + "_chunks_stats.csv"  # add .csv extension

    # order the chunks by the id
    chunks = sorted(chunks, key=lambda x: x.metadata["id"])

    with open(csv_output_path, "w") as f:
        f.write("chunk_id, file_name, nb_chars, nb_tokens\n")
        for chunk in chunks:
            f.write(
                f"{chunk.metadata['id']}, {chunk.metadata['file_name']}, {len(chunk.page_content)}, {chunk.metadata['nb_tokens']}\n"
            )

    logger.success(
        f"Saved the number of tokens and chunks for each files successfully to '{csv_output_path}'.\n"
    )


def main() -> None:
    """Main function to save details of chunks to a text file and CSV file."""
    # Get the command line arguments
    chroma_path = get_args()

    # load the Chroma database
    vector_db = load_database(chroma_path)[0]

    # get the chunks from the vector database
    chunks = reconstruct_chunks(vector_db)

    # save the details of each chunks to a text file
    save_to_txt(chunks, chroma_path)

    # save the number of tokens and chunks for each files to a CSV file
    save_to_csv(chunks, chroma_path)


# MAIN PROGRAM
if __name__ == "__main__":
    main()