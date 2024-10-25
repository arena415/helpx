# File: helpx/core.py

import inspect
import importlib
import os
import re
import base64

# Updated FUNCTION_CATEGORIES and CATEGORY_MODULE_MAP
FUNCTION_CATEGORIES = {
    "OpenCV": [
        "Canny", "getRotationMatrix2D", "cvtColor", "convertScaleAbs", "circle",
        "HoughCircles", "resize", "zeros_like", "calcHist", "threshold", "blur",
        "waitKey", "destroyAllWindows", "imshow", "imread", "warpAffine",
        "GaussianBlur", "split", "filter2D", "Laplacian"
    ],
    "Matplotlib": [
        "tight_layout", "figure", "set_title", "subplot", "title", "subplots",
        "axis", "set_xlim", "show", "plot"
    ],
    "Numpy": [
        "clip", "normal", "copy", "reshape", "print", "fit_transform", "find",
        "read", "defaultdict", "append", "array", "randint", "sub", "where",
        "len", "sort", "ones", "add_gaussian_noise", "items", "list",
        "argsort", "download", "ceil", "range", "float32", "strip", "dict",
        "astype", "compile", "open", "int", "lower", "log", "split",
        "enumerate", "set", "zeros"
    ],
    "NLP - nltk": [
        "PorterStemmer", "WordNetLemmatizer", "lemmatize", "stem"
    ],
    "NLP - sklearn.feature_extraction.text": [
        "TfidfVectorizer"
    ],
    "NLP - sklearn.metrics.pairwise": [
        "cosine_similarity"
    ],
    "NLP - gensim.models": [
        "Word2Vec"
    ],
    "Custom": [
        "calculate_idf", "calculate_tf", "clean_text", "lower_case",
        "match_sentences", "remove_accents", "remove_punctuations"
    ]
}

CATEGORY_MODULE_MAP = {
    "OpenCV": "cv2",
    "Matplotlib": "matplotlib.pyplot",
    "Numpy": "numpy",
    "NLP - nltk": "nltk",
    "NLP - sklearn.feature_extraction.text": "sklearn.feature_extraction.text",
    "NLP - sklearn.metrics.pairwise": "sklearn.metrics.pairwise",
    "NLP - gensim.models": "gensim.models",
    "Custom": "Custom"  # Pseudo-module name for custom/general functions
}

# Path to the Base64-encoded examples file
ENCODED_EXAMPLES_FILE = os.path.join(os.path.dirname(__file__), 'examples.b64')

def helpx(entity):
    """
    Provide help and code examples for a given function, class, or list functions in a module.

    Parameters:
    - entity: A function, class, or a module (e.g., cv2, your_custom_module)

    Usage:
    - helpx(cv2.Canny)
    - helpx(cv2)
    - helpx(calculate_tf)
    - helpx(custom)
    - helpx(TfidfVectorizer)
    """
    if inspect.isfunction(entity) or inspect.isbuiltin(entity) or inspect.isclass(entity):
        function_help(entity)
    elif inspect.ismodule(entity):
        module_help(entity)
    else:
        print("Unsupported type. Please provide a function, class, or a module.")

def function_help(entity):
    """
    Print the help information and a code example for a given function or class.
    """
    full_name = get_full_function_name(entity)
    print(f"Help for {full_name}:\n")

    # Get the docstring
    doc = inspect.getdoc(entity)
    if doc:
        print(doc)
    else:
        print("No documentation available.")

    print("\nCode Example:\n")

    # Retrieve the code example
    example_code = get_example(full_name)

    if example_code:
        print(example_code)
    else:
        print(f"No example available for {full_name}.")

def module_help(module):
    """
    List all functions and classes in the module that are categorized in FUNCTION_CATEGORIES.
    """
    print(f"Functions and Classes in module '{module.__name__}' available in helpx:\n")

    # Get the top-level module name
    module_name = module.__name__.split('.')[0]

    # Find all functions and classes from FUNCTION_CATEGORIES that belong to this module
    items_in_module = []
    for category, items in FUNCTION_CATEGORIES.items():
        mapped_module = CATEGORY_MODULE_MAP.get(category, "")
        if mapped_module == module.__name__ or mapped_module.startswith(module_name):
            for item_name in items:
                try:
                    attr = getattr(module, item_name)
                    if inspect.isfunction(attr) or inspect.isbuiltin(attr) or inspect.isclass(attr):
                        items_in_module.append(item_name)
                except AttributeError:
                    continue

    if items_in_module:
        for item in sorted(items_in_module):
            print(f"- {item}")
    else:
        print("No functions or classes from helpx found in this module.")

def get_example(key):
    """
    Retrieve the code example for a given key from the Base64-encoded examples.b64.

    Parameters:
    - key: A string in the format 'module.function' or 'module.Class'

    Returns:
    - The code example as a string, or None if not found.
    """
    if not os.path.exists(ENCODED_EXAMPLES_FILE):
        print("Examples file not found.")
        return None

    with open(ENCODED_EXAMPLES_FILE, 'rb') as file:
        encoded_content = file.read()

    # Decode the Base64 content
    try:
        decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    except Exception as e:
        print(f"Error decoding Base64 content: {e}")
        return None

    # Use regex to find the example section
    pattern = rf"===\s*{re.escape(key)}\s*===\n([\s\S]*?)(?====\s*\w+(\.\w+)*\s*===|$)"
    match = re.search(pattern, decoded_content)

    if match:
        return match.group(1).strip()
    else:
        print(f"No example found for '{key}'.")
        return None

def get_full_function_name(entity):
    """
    Retrieve the full function or class name in the format 'module.function'.
    Uses category mapping if the entity belongs to a known category.

    Parameters:
    - entity: The function or class object.

    Returns:
    - A string representing the full function or class name.
    """
    name = entity.__name__
    module_name = entity.__module__

    # Determine which category the entity belongs to
    category = None
    for cat, items in FUNCTION_CATEGORIES.items():
        if name in items:
            category = cat
            break

    if category:
        mapped_module = CATEGORY_MODULE_MAP.get(category, "unknown")
        # For custom functions, map to 'Custom.function_name'
        if category == "Custom":
            return f"Custom.{name}"
        else:
            return f"{mapped_module}.{name}"
    else:
        # Fallback to module.function or module.Class
        if module_name:
            return f"{module_name}.{name}"
        else:
            return f"unknown.{name}"

def fprint():
    """
    List all functions and classes available in helpx, categorized by their modules with full names.
    """
    print("Listing All Functions and Classes in helpx:\n")
    for category, items in FUNCTION_CATEGORIES.items():
        mapped_module = CATEGORY_MODULE_MAP.get(category, "unknown")
        print(f"--- {category} ({mapped_module}) ---")
        for item in sorted(items):
            full_item_name = f"{mapped_module}.{item}"
            print(f"- {full_item_name}")
        print("\n")

