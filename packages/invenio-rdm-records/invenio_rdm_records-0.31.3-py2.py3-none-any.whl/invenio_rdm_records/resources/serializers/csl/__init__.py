# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CSL JSON and  citation string serializers for Invenio RDM Records."""

import re

from citeproc import Citation, CitationItem, CitationStylesBibliography, \
    CitationStylesStyle, formatter
from citeproc.source.json import CiteProcJSON
from citeproc_styles import get_style_filepath
from citeproc_styles.errors import StyleNotFoundError
from flask import abort, request
from flask_resources.serializers import MarshmallowJSONSerializer
from webargs import fields
from webargs.flaskparser import FlaskParser

from .schema import CSLJSONSchema


class CSLJSONSerializer(MarshmallowJSONSerializer):
    """Marshmallow based CSL JSON serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(schema_cls=CSLJSONSchema, **options)


def get_citation_string(json, id, style, locale):
    """Get the citation string from Citeproc."""

    def _clean_result(text):
        """Remove double spaces, punctuation and escapes apostrophes."""
        text = re.sub(r"\s\s+", " ", text)
        text = re.sub(r"\.\.+", ".", text)
        text = text.replace("'", "\\'")
        return text

    source = CiteProcJSON([json])
    citation_style = CitationStylesStyle(
        validate=False, style=style, locale=locale
    )
    bib = CitationStylesBibliography(citation_style, source, formatter.plain)
    citation = Citation([CitationItem(id)])
    bib.register(citation)

    return _clean_result(str(bib.bibliography()[0]))


class StringCitationSerializer(MarshmallowJSONSerializer):
    """CSL Citation Formatter serializer for records.

    In order to produce a formatted citation of a record through citeproc-py,
    we need a CSL-JSON serialized version of it.
    """

    _default_style = "harvard1"
    """The `citeproc-py` library supports by default the 'harvard1' style."""

    _default_locale = "en-US"
    """The `citeproc-py` library supports by default the 'harvard1' style."""

    _user_args = {
        "style": fields.Str(missing=_default_style),
        "locale": fields.Str(missing=_default_locale),
    }
    """Arguments for the webargs parser."""

    _valid_formats = ("csl", "bibtex")
    """Supported formats by citeproc-py."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(schema_cls=CSLJSONSchema, **options)

    @classmethod
    def _get_args(cls, **kwargs):
        """Parse style and locale.

        Argument location precedence: kwargs > view_args > query
        """
        csl_args = {"style": cls._default_style, "locale": cls._default_locale}
        parser = FlaskParser(locations=("view_args", "query"))
        csl_args.update(parser.parse(cls._user_args, request))

        csl_args.update(
            {k: kwargs[k] for k in ("style", "locale") if k in kwargs}
        )

        try:
            csl_args["style"] = get_style_filepath(csl_args["style"].lower())
        except StyleNotFoundError:
            abort(
                400,
                description=f"Style {csl_args['style']} could not be found.",
            )

        return csl_args

    def serialize_object(self, record, **kwargs):
        """Serialize a single record.

        :param record: Record instance.
        """
        return get_citation_string(
            self.dump_one(record), record["id"], **self._get_args(**kwargs)
        )

    def serialize_object_list(self, records, **kwargs):
        """Serialize a list of records.

        :param records: List of records instance.
        """
        return "\n".join(
            [
                self.serialize_object(rec, **kwargs)
                for rec in records["hits"]["hits"]
            ]
        )
