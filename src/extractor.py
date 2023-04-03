"""
This module contains the MNIST data extractor class.
"""
from io import BufferedReader
import pathlib
import struct

import numpy as np
from PIL import Image as img
from tqdm import tqdm


class Extractor:
    """
    MNIST image and label extractor.
    """

    num = 0

    @staticmethod
    def next_num() -> int:
        """
        Get the next number.

        Returns:
            The next number
        """
        Extractor.num += 1
        return Extractor.num

    def __init__(
        self,
        save_location: str,
        *,
        create_parents: bool = False
    ) -> None:
        """
        Extractor init.

        Args:
            save_location: The location to save the images
            create_parents: If true, allow parent folders to be created
                            if needed
        """
        self.save_location = pathlib.Path(save_location)
        if self.save_location.exists() and not self.save_location.is_dir():
            raise NotADirectoryError(
                "The provided save location is not a directory."
            )
        self.save_location.mkdir(parents=create_parents, exist_ok=True)
        for i in range(10):
            class_folder = self.save_location / str(i)
            class_folder.mkdir(exist_ok=True)

    # region Extract
    def _check_metadata(
        self,
        image_metadata: bytes,
        label_metadata: bytes
    ) -> tuple[int, int, int]:
        """
        Checks that the metadata is correct and the image and label files
        match.

        Args:
            image_metadata: The first 16 bytes of the image file
            label_metadata: The first 8 bytes of the label file

        Returns:
            The number of images, the number of rows and columns in an image.
        """
        # Check image file
        magic, num_images, num_rows, num_cols = struct.unpack(
            ">IIII", image_metadata
        )
        if magic != 2051:
            raise ValueError(
                "Image file magic number mismatch, expected 2051,"
                f" got {magic}."
            )
        if num_rows != 28 or num_cols != 28:
            raise ValueError(
                "Unexpected image dimensions, expected 28x28, got"
                f" {num_rows}x{num_cols}."
            )

        # Check label file
        magic, num_labels = struct.unpack(">II", label_metadata)
        if magic != 2049:
            raise ValueError(
                "Label file magic number mismatch, expected 2049,"
                f" got {magic}."
            )
        if num_images != num_labels:
            raise ValueError(
                f"Number of images ({num_images}) does not match"
                f" number of labels ({num_labels})."
            )
        return num_images, num_rows, num_cols

    def _extract_image(
        self,
        image_file: BufferedReader,
        label_file: BufferedReader,
        image_dimension: tuple[int, int]
    ) -> tuple[img.Image, int]:
        """
        Extracts the image and its class label.

        Args:
            image_file: The image file reader
            label_file: The label file reader
            image_dimension: The image dimensions

        Returns:
            The image as a PIL image and the image's class label.
        """
        label, *_ = struct.unpack('B', label_file.read(1))
        rows, cols = image_dimension
        image = img.fromarray(
            np.array([
                [
                    struct.unpack('B', image_file.read(1))[0]
                    for _ in range(cols)
                ]
                for _ in range(rows)
            ]).astype(np.uint8)
        )

        return image, label

    def _save_image(
        self,
        image: img.Image,
        label: int,
        *,
        format: str = "jpg"
    ) -> None:
        """
        Save the image under the correct class in the save location.

        Args:
            image: The PIL image to save
            label: The label of the image
            format: The format to save the image in
        """
        image.save(
            self.save_location /
            str(label) /
            f"{Extractor.next_num()}.{format}"
        )

    def extract(
        self,
        *,
        image_file_location: str,
        label_file_location: str
    ) -> None:
        """
        Extract the images from the image and label files and save them as
        an image in the save location under the class's folder.

        Args:
            image_file_location: The location of the image file
            label_file_location: The location of the label file
        """
        with (
            pathlib.Path(image_file_location).open("rb") as image_file,
            pathlib.Path(label_file_location).open("rb") as label_file
        ):
            num_images, num_rows, num_cols = self._check_metadata(
                image_file.read(16),
                label_file.read(8)
            )

            print(f"Saving images to {self.save_location}")
            for _ in tqdm(range(num_images)):
                image, label = self._extract_image(
                    image_file,
                    label_file,
                    (num_rows, num_cols)
                )
                self._save_image(image, label)
    # endregion Extract
