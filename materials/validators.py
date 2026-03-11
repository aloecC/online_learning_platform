import re

from rest_framework.serializers import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)

        if tmp_val is None or tmp_val.strip() == "":
            return

        reg = re.compile(
            "^(https?://)?(www.)?(youtube.com/(watch?v=|embed/|v/|.+?v=)|youtu.be/)([a-zA-Z0-9_-]{11})$"
        )

        if not bool(reg.match(tmp_val)):
            raise ValidationError("Title os not ok")
