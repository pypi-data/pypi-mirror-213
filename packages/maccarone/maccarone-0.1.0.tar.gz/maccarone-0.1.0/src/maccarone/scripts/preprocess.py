import os
import glob
import logging

from argparse import Namespace

from maccarone.openai import CachedChatAPI
from maccarone.preprocessor import preprocess_maccarone

logger = logging.getLogger(__name__)

def preprocess(mn_path: str, print_: bool, write: bool, suffix: str) -> None:
    # produce Python source
    logger.info("preprocessing %s", mn_path)

    cache_path = mn_path.replace(suffix, ".mn.json")
    chat_api = CachedChatAPI(cache_path)

    with open(mn_path, "r") as f:
        mn_source = f.read()


    py_source = preprocess_maccarone(mn_source, chat_api)

    if write:
        import re
        py_path = re.sub(f"{suffix}$", ".py", mn_path)


        logger.info("writing %s", py_path)

        if py_path == mn_path:
            raise ValueError("won't overwrite input file", mn_path)

        with open(py_path, "w") as f:
            f.write(py_source)


    if print_:
        print(py_source)

def main(path: str, print_: bool, write: bool, suffix: str) -> None:
    """Preprocess files with Maccarone snippets."""

    if os.path.isdir(path):
        mn_files = glob.glob(
            os.path.join(path, f"**/*{suffix}"),
            recursive=True,
        )
    else:
        mn_files = [path]

    for mn_file in mn_files:
        preprocess(mn_file, print_, write, suffix)


def parse_args() -> Namespace:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file or directory containing Maccarone snippets")
    parser.add_argument("--print", dest="print_", action="store_true", help="Print the preprocessed Python source")
    parser.add_argument("--write", action="store_true", help="Write the preprocessed Python source to a file")
    parser.add_argument("--suffix", default=".mn.py", help="Suffix for files containing Maccarone snippets (default: .mn.py)")
    args = parser.parse_args()
    return args


def script_main():
    logging.basicConfig(level=logging.INFO)

    return main(**vars(parse_args()))

if __name__ == "__main__":
    script_main()

