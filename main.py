"""
This module is the CLI tool for the data extractor.
"""
import argparse

from extractor.extractor import Extractor


def get_parser() -> argparse.ArgumentParser:
    """
    Create the CLI argument parser.

    Returns:
        The CLI argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Extracts the MNIST images from the binary files."
    )

    # region Parser arguments
    parser.add_argument(
        "save_location",
        help="The location to save the images."
    )
    parser.add_argument(
        "-f",
        help="Force missing parent folders in save_location to be created.",
        action="store_true"
    )
    parser.add_argument(
        "--image",
        required=True,
        help="The location of the image binary."
    )
    parser.add_argument(
        "--label",
        required=True,
        help="The location of the label binary."
    )
    # endregion Parser arguments

    return parser


def main() -> None:
    parser = get_parser()
    args = vars(parser.parse_args())

    extractor = Extractor(args["save_location"], create_parents=args["f"])
    extractor.extract(
        image_file_location=args["image"],
        label_file_location=args["label"]
    )


if __name__ == "__main__":
    main()
