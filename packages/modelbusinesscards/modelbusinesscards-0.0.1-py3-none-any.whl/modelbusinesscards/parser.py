import ast
import os
import re
from typing import List
import yaml

from .entities import ModelBusinessDoc, ModelBusinessPromptDoc


class MBCPythonFilesParser:
    """Parses a directory of python files and returns a list of ModelBusinessDoc objects"""
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    # File Traversal - Directories
    def get_python_file_paths(self) -> List[str]:
        python_files = []
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files

    # Parsers - YAML
    def mbc_yaml_parse(self, mixed_string: str, parse_key: str) -> dict:
        yaml_content = re.findall(r'---(.*?)---', mixed_string, re.DOTALL)
        found_dict = None
        for yaml_string in yaml_content:
            yaml_string = yaml_string.strip()
            try:
                parsed_yaml = yaml.safe_load(yaml_string)
                if parsed_yaml is not None:
                    found_dict = parsed_yaml[parse_key] # if this property doesn't exist, we'll err and let it pass
                    break
            except yaml.YAMLError as err:
                pass
        return found_dict

    # Parsers - File Content
    def get_mbc_docs_from_python_file_path(self, file_path: str) -> tuple[List[ModelBusinessDoc], List[ModelBusinessPromptDoc]]:
        # 1. FILE CONTENT
        with open(file_path, 'r') as file:
            file_content = file.read()

        # 2. PARSE FUNCTIONS/CLASS DOCSTRINGS FOR ModelUse (using ast module)
        mbc_uses = []
        for node in ast.walk(ast.parse(file_content)):
            # ... for each class/function, grab the docstring)
            if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
                node_docstring = ast.get_docstring(node)
                if node_docstring != None:
                    # ... extract the YAML
                    mbc_use_data = self.mbc_yaml_parse(node_docstring, parse_key='ModelBusiness')
                    if mbc_use_data != None:
                        mbc_use = ModelBusinessDoc(
                            name=mbc_use_data.get('name') or node.name,
                            business_logic=mbc_use_data.get('business_logic'),
                            models=mbc_use_data.get('models'),
                            tags=mbc_use_data.get('tags'),
                            prompts=mbc_use_data.get('prompts'),
                        )
                        mbc_uses.append(mbc_use)

        # 3. PARSE FILE TEXT FOR ModelUsePrompt (using regex bc vars don't have docstrings)
        mbc_prompts = []
        model_use_prompt_text_blocks = re.findall(r'---\n\s*ModelBusinessPrompt:.*?---', file_content, re.DOTALL)
        for model_use_prompt_block in model_use_prompt_text_blocks:
            # ... extract the YAML
            mbc_prompt_data = self.mbc_yaml_parse(model_use_prompt_block, parse_key='ModelBusinessPrompt')
            mbc_prompt = ModelBusinessPromptDoc(
                name=mbc_prompt_data.get('name'),
                prompt=mbc_prompt_data.get('prompt'),
            )
            mbc_prompts.append(mbc_prompt)

        # 4. RETURN
        return mbc_uses, mbc_prompts

    def run(self) -> tuple[List[ModelBusinessDoc], List[ModelBusinessPromptDoc]]:
        mbc_uses = []
        mbc_prompts = []
        for file_path in self.get_python_file_paths():
            new_mbc_uses, new_mbc_prompts = self.get_mbc_docs_from_python_file_path(file_path)
            mbc_uses += new_mbc_uses
            mbc_prompts += new_mbc_prompts
        return mbc_uses, mbc_prompts
