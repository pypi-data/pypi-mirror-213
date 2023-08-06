# 
#   AutoFunction
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from fxn import Acceleration, AccessMode, Predictor, PredictorType
from nbformat import write
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook
import openai
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict

def create (
    tag: str,
    description: str,
    type: PredictorType=None,
    access: AccessMode=None,
    acceleration: Acceleration=None,
    environment: Dict[str, str]=None,
    overwrite: bool=None,
    access_key: str=None
) -> Predictor:
    """
    Create a predictor from a description of what it should do.

    Parameters:
        tag (str); Predictor tag.
        description (str): Describe what you want the predictor to do. Be as detailed as possible.
        type (PredictorType): Predictor type. This defaults to `CLOUD`.
        access (AccessMode): Predictor access mode. This defaults to `PRIVATE`.
        acceleration (Acceleration): Cloud predictor acceleration. This defaults to `CPU`.
        environment (dict): Predictor environment variables.
        overwrite (bool): Overwrite any existing predictor with the same tag. Existing predictor will be deleted.
        access_key (str): Function access key.

    Returns:
        Predictor: Created predictor.
    """
    # Generate source code
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are an assistant that writes AI prediction functions, or "predictors" for short, given a description of what the function should do.
                
                Your response must contain one Python function called `predict` that conforms to what the user requests.

                The `predict` function must have type annotations for its input arguments.
                
                If your code requires Python dependencies, add an IPython magic line that uses `%pip install` to install Python dependencies.

                If your code requires system package dependencies, add an IPython system command line that uses `!apt-get install -y` to install Linux packages.

                For input images to the predictor, the function should use a Pillow `Image.Image` instance instead of an image path.

                For input tensors to the predictor, the function should use a numpy `ndarray` instance instead of a `torch.Tensor`.

                Always add a Google-style docstring to the predictor with a description of the function, its arguments, and what it returns.

                Finally, provide no explanations whatsoever. Only emit code.
                """
            },
            { "role": "user", "content": description }
        ],
        temperature=0
    )
    source: str = completion["choices"][0]["message"]["content"]
    source = source.replace("```python", "")
    source = source.replace("```py", "")
    source = source.replace("```", "")
    # Create notebook
    notebook = new_notebook()
    readme_cell = new_markdown_cell(
f"""Created by autofxn:
> {description}"""
    )
    source_cell = new_code_cell(source)
    notebook["cells"] = [readme_cell, source_cell]
    with NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False) as f:
        write(notebook, f)
    # Create predictor
    predicctor = Predictor.create(
        tag=tag,
        notebook=Path(f.name),
        type=type,
        access=access,
        description=None,
        media=None,
        acceleration=acceleration,
        environment=environment,
        license=None,
        overwrite=overwrite,
        access_key=access_key
    )
    # Return
    return predicctor