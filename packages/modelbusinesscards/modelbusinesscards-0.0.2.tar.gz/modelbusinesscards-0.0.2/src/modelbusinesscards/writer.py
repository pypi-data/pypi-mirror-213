import os
from typing import List

from .entities import ModelBusinessDoc, ModelBusinessPromptDoc


class MBCMarkdownWriter:
    """Writes a list of ModelBusinessDoc objects to a markdown file"""
    def __init__(self, output_file: str):
        self.output_file = output_file

    def write(self, mbc_uses: List[ModelBusinessDoc], mbc_prompts: List[ModelBusinessPromptDoc]):
        with open(self.output_file, 'w') as file:
            # SETUP
            models_in_use = set()
            for mbc_use in mbc_uses:
                # --- Overview of Uses (ex: compile list of models in use/aliases)
                models_in_use = models_in_use.union(mbc_use.models)
                # --- Model Uses

            # WRITE
            # --- name
            name = os.path.basename(os.getcwd())
            file.write(f"# Model Business Card for {name} \n\n")

            # --- uses
            file.write(f"## Business Logic\n\n")
            for mbc_use in mbc_uses:
                file.write(f"### {mbc_use.name}\n")
                if mbc_use.business_logic:
                    file.write(f"\nDescription: {mbc_use.business_logic}")
                if isinstance(mbc_use.tags, list):
                    file.write(f"\n\nTags: {', '.join(mbc_use.tags)}\n")
                if mbc_use.prompts != None:
                    file.write('\nPrompts:\n')
                    for prompt in mbc_use.prompts:
                        file.write(f"- {prompt}\n")
                file.write('\n')

            # --- models
            file.write("\n---\n\n")
            file.write(f"## Models\n\n")
            for model in sorted(models_in_use):
                file.write(f"- {model}\n")

            # --- prompts
            file.write("\n---\n\n")
            file.write(f"## Prompts\n\n")
            for mbc_prompt in mbc_prompts:
                file.write(f"### {mbc_prompt.name}\n\n")
                file.write('```' + '\n' + mbc_prompt.prompt + '\n' + '```')
                file.write('\n\n')
