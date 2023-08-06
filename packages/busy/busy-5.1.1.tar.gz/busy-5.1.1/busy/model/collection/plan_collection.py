from . import Collection


class PlanCollection(Collection):

    state = 'plan'
    schema = ['plan_date', 'description']
