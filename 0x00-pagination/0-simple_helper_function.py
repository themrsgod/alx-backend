#!/usr/bin/env python3
"""Simpler helper function"""


def index_range(page, page_size):
    """
    Returns a tuple of size two containing a start index and
    end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)
