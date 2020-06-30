from wtforms import ValidationError

from alegrosz.dbs.dbs import get_db


class BelongsToOtherFieldOption:
    def __init__(self, table, belongs_to, foreign_key=None, message=None):
        if not table:
            raise AttributeError("BelongsToOtherFieldOption validator needs the table parameter")

        if not belongs_to:
            raise AttributeError("BelongsToOtherFieldOption validator needs the belongs_to parameter")

        self.table = table
        self.belongs_to = belongs_to

        if not foreign_key:
            foreign_key = belongs_to + "_id"

        if not message:
            message = "Chosen option is not valid"

        self.foreign_key = foreign_key
        self.message = message

    def __call__(self, form, field):
        c = get_db().cursor()

        try:
            c.execute(f"""SELECT COUNT(*) FROM {self.table}
                WHERE id = ? AND {self.foreign_key} = ?""", (
                field.data, getattr(form, self.belongs_to).data
            ))
        except Exception as e:
            raise AttributeError(f"Passed parameters are not correct. {e}")

        exists = c.fetchone()[0]
        print(exists)
        if not exists:
            raise ValidationError(self.message)
