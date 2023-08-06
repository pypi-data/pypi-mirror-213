"""The module that defines the ``WebhookEnabledConfiguration`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class WebhookEnabledConfiguration:
    """Webhook upload type is enabled."""

    #: The tag for this data.
    tag: "t.Literal['enabled']"
    #: A url for a repository that determine the template for student
    #: submissions.
    template_url: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "tag",
                rqa.StringEnum("enabled"),
                doc="The tag for this data.",
            ),
            rqa.RequiredArgument(
                "template_url",
                rqa.Nullable(rqa.SimpleValue.str),
                doc=(
                    "A url for a repository that determine the template for"
                    " student submissions."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "tag": to_dict(self.tag),
            "template_url": to_dict(self.template_url),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["WebhookEnabledConfiguration"], d: t.Dict[str, t.Any]
    ) -> "WebhookEnabledConfiguration":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            tag=parsed.tag,
            template_url=parsed.template_url,
        )
        res.raw_data = d
        return res
