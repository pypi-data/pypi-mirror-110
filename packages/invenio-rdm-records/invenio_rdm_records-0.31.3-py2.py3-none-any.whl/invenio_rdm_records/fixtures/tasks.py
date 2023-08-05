# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks for fixtures."""
import arrow
from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_vocabularies.proxies import current_service as vocabulary_service

from ..proxies import current_rdm_records
from ..services.errors import EmbargoNotLiftedError


@shared_task
def create_vocabulary_record(data):
    """Create a vocabulary record."""
    vocabulary_service.create(system_identity, data)


@shared_task
def create_demo_record(data):
    """Create a demo record."""
    service = current_rdm_records.records_service
    draft = service.create(data=data, identity=system_identity)
    service.publish(id_=draft.id, identity=system_identity)


@shared_task(ignore_result=True)
def update_expired_embargos():
    """Release expired embargoes."""
    service = current_rdm_records.records_service
    embargoed_q = f"access.embargo.active:true AND access.embargo.until:" \
                  f"{{* TO {arrow.utcnow().datetime.strftime('%Y-%m-%d')}}}"
    # Retrieve overdue embargoed records
    restricted_records = service.scan(identity=system_identity, q=embargoed_q)
    for restricted_record in restricted_records.to_dict()["hits"]["hits"]:
        try:
            service.lift_embargo(
                _id=restricted_record['id'],
                identity=system_identity
            )
        except EmbargoNotLiftedError:
            current_app.logger.warning(f"Embargo from record with id"
                                       f" {restricted_record['id']} was not"
                                       f" lifted")
            continue
