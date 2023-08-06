from busy.command.command import CollectionCommand


class ListCommand(CollectionCommand):
    """Show the descriptions with selection numbers, default to all"""

    name = 'list'
    # key = "l"
    default_criteria = ['1-']
    FORMATS = {
        'description': "{!s}",
        'plan_date': "{:%Y-%m-%d}",
        'done_date': "{:%Y-%m-%d}"
    }

    @CollectionCommand.wrap
    def execute(self):
        def format(item, index):
            result = f"{(index+1):>6}"
            for colname in self.collection.schema:
                format = self.FORMATS[colname]
                value = getattr(item, colname)
                result += f"  {format.format(value)}"
            return result
        return self.output_items(format, with_index=True)
