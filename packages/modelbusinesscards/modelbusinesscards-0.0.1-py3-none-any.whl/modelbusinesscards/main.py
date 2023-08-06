import argparse
import os

from .parser import MBCPythonFilesParser
from .writer import MBCMarkdownWriter

default_dir_path = os.getcwd()
default_output_file = 'model_business_card.md'

# Calling via from/import
def mbc(dir_path: str = default_dir_path, output_file: str = default_output_file):
    """Generate a model business card markdown files from Python docstrings."""
    # Parse files for docstrings that have model business card yaml valid write-ups/data
    parser = MBCPythonFilesParser(dir_path)
    mbc_uses, mbc_prompts = parser.run()
    # Write out the mbc markdown file
    writer = MBCMarkdownWriter(output_file)
    writer.write(mbc_uses, mbc_prompts)


# Calling via command line (ex: python -m modelbusinesscards)
def cli():
    # setup args parsing
    parser = argparse.ArgumentParser(description='Generate a markdown file from Python docstrings.')
    parser.add_argument('-d', '--dir', type=str, help='The directory to search for Python files.', default=default_dir_path)
    parser.add_argument('-o', '--output', type=str, help='The name of the output markdown file.', default=default_output_file)
    args = parser.parse_args()
    # execute
    mbc(args.dir, args.output)
