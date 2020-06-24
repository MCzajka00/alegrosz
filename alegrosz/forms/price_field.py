from markupsafe import Markup
from wtforms.fields.html5 import DecimalField
from wtforms.widgets import Input


class PriceInput(Input):
    input_type = "number"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("step", "0.01")
        kwargs.setdefault("min", "0.00")

        if "value" not in kwargs:
            kwargs["value"] = field._value()

        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        return Markup("""
        <div class="input-group nb-3">
        <input %s>
            <div class="input-group-append">
                <span class="input-group-text">PLN</span>
            </div>
        </div>
        """ % self.html_params(name=field.name, **kwargs))


class PriceField(DecimalField):
    widget = PriceInput()
