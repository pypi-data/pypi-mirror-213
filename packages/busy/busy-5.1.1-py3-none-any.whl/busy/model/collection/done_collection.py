from . import Collection


class DoneCollection(Collection):

    state = 'done'
    schema = ['done_date', 'description']
