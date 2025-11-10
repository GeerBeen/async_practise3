from Practise3.task1.utils import search_in_chunk, timed


@timed
def work_sync(arr, target):
    return search_in_chunk(arr, target)
