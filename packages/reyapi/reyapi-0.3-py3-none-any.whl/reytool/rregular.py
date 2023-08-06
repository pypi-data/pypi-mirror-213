# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-11 23:25:36
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Regular methods.
"""


from typing import List, Tuple, Optional, Union, Literal, overload
from re import search as re_search, sub as re_sub, findall as re_findall

from .rdata import unique


def search(pattern: str, text: str) -> Optional[Union[str, Tuple[Optional[str], ...]]]:
    """
    Regular `matching` text.

    Parameters
    ----------
    pattern : Regular pattern.
    text : Match text.

    Returns
    -------
    Matching result.
        - When match to and not use `group`, then return string.
        - When match to and use `group`, then return tuple with value string or None.
            If tuple length is `1`, extract and return string.
        - When no match, then return None.
    """

    # Search.
    obj_re = re_search(pattern, text)

    # Return result.
    if obj_re is not None:
        result = obj_re.groups()
        if result == ():
            result = obj_re[0]
        elif len(result) == 1:
            result = obj_re[1]
        return result


@overload
def search_batch(text: str, *patterns: str, first: bool = True) -> Union[
    Optional[Union[str, Tuple[Optional[str], ...]]],
    List[Optional[Union[str, Tuple[Optional[str], ...]]]]
]: ...

@overload
def search_batch(first: Literal[True]) -> Optional[Union[str, Tuple[Optional[str], ...]]]: ...

@overload
def search_batch(first: Literal[False]) -> List[Optional[Union[str, Tuple[Optional[str], ...]]]]: ...

def search_batch(text: str, *patterns: str, first: bool = True) -> Union[
    Optional[Union[str, Tuple[Optional[str], ...]]],
    List[Optional[Union[str, Tuple[Optional[str], ...]]]]
]:
    """
    `Batch` regular `search` text.

    Parameters
    ----------
    text : Match text.
    pattern : Regular pattern.
    first : Whether return first successful match.

    Returns
    -------
    Matching result.
        - When match to and not use group, then return string.
        - When match to and use group, then return tuple with value string or None.
        - When no match, then return.
    """

    # Search.

    ## Return first result.
    if first:
        for pattern in patterns:
            result = search(pattern, text)
            if result is not None:
                return result

    ## Return all result.
    else:
        result = [search(pattern, text) for pattern in patterns]
        return result


def sub_batch(text: str, *patterns: Tuple[str, str]) -> str:
    """
    `Batch` regular `replace` text.

    Parameters
    ----------
    text : Match text.
    patterns : Regular pattern and replace text.

    Returns
    -------
    Replaced result.
    """

    # Replace.
    for pattern, replace in patterns:
        text = re_sub(pattern, replace, text)

    return text


def findall_batch(text: str, *patterns: str) -> str:
    """
    `Batch` regular `find all` text.

    Parameters
    ----------
    text : Match text.
    patterns : Regular pattern.

    Returns
    -------
    List of Find result.
    """

    # Find all.
    texts = [
        string
        for pattern in patterns
        for string in re_findall(pattern, text)
    ]

    # De duplicate.
    texts = unique(texts)

    return texts