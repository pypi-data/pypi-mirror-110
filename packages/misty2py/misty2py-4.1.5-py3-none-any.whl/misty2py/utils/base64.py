"""base64 encoders and decoders"""
import base64
from typing import Union
from os import listdir
from os.path import isfile, join


def content_to_base64(
    input_str: str, is_path: bool = False, save_path: Union[str, bool] = False
) -> str:
    """Encodes content to base64.

    Args:
        input_str (str): the utf-8 string to encode or the path to the file
        to encode.
        is_path (bool, optional): True if input_str is the path to the file
        to encode, False if input_str is the content to encode. Defaults
        to False.
        save_path (Union[str,bool], optional): path to the file where
        the encoded content should be saved, False if the encoded content
        should be returned as utf-8 string. Defaults to False.

    Returns:
        str: either the encoded content if save_path is False, or the success
        message if save_path is True.
    """
    if is_path:
        try:
            data = open(input_str, "rb").read()
        except Exception as e:
            return "Error reading the file `%s`. Error message: `%s`" % (
                input_str,
                e
            )
    else:
        data = input_str.encode()
    encoded = base64.b64encode(data)
    if save_path:
        try:
            with open(save_path, "wb") as f:
                f.write(encoded)
            return "Successfully saved to `%s`" % save_path
        except Exception as e:
            return "Error saving to `%s`. Error message: `%s`" % (
                save_path,
                e
            )
    return encoded.decode("utf-8")


def base64_to_content(
    input_str: str, is_path: bool = False, save_path: Union[str, bool] = False
) -> str:
    """Decodes base64 to utf-8 string or other content type specified
    by the extension in save_path.

    Args:
        input_str (str): the utf-8 string to decode or the path to the file
        to decode.
        is_path (bool, optional): True if input_str is the path to the file
        to decode, False if input_str is the content to decode. Defaults
        to False.
        save_path (Union[str,bool], optional): path to the file where
        the decoded content should be saved, False if the decoded content
        should be returned as utf-8 string. Defaults to False.

    Returns:
        str: [description]
    """
    if is_path:
        try:
            data = open(input_str, "rb").read()
        except Exception as e:
            return "Error reading the file `%s`. Error message: `%s`" % (
                input_str,
                e
            )
    else:
        data = input_str.encode()
    decoded = base64.b64decode(data)
    if save_path:
        try:
            with open(save_path, "wb") as f:
                f.write(decoded)
            return "Successfully saved to `%s`" % save_path
        except Exception as e:
            return "Error saving to `%s`. Error message: `%s`" % (
                save_path,
                e
            )
    return decoded.decode("utf-8")
