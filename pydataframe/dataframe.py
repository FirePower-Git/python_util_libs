class DataFrame:

    def __init__(self, columns: list, col_names: list, dtypes: dict = None, title: str = ""):
        self.title = title

        col_names = [col_names[i] if col_names[i] not in ['', None] else ('col_' + str(i)) for i in range(len(col_names))]

        if len(columns) > len(col_names):
            pass
        elif len(columns) < len(col_names):
            pass
        else:
            self.columns = {col_names[i]: columns[i] for i in range(len(col_names))}

        self.shape = (len(col_names), max([len(columns[i]) for i in range(len(col_names))]))
