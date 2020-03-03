import json
from unittest import skip  # noqa

from aleph.core import db
from aleph.authz import Authz
from aleph.tests.util import TestCase
from aleph.logic.xref import xref_collection
from aleph.index.xref import iter_matches
from aleph.queues import get_stage, OP_XREF


class XrefTestCase(TestCase):

    def setUp(self):
        super(XrefTestCase, self).setUp()
        self.user = self.create_user()
        self.coll_a = self.create_collection(creator=self.user, casefile=False)
        self.coll_b = self.create_collection(creator=self.user, casefile=False)
        self.coll_c = self.create_collection(creator=self.user, casefile=False)
        db.session.commit()
        self.stage = get_stage(self.coll_a, OP_XREF, job_id='unit_test')
        self.authz = Authz.from_role(self.user)

        _, headers = self.login(foreign_id=self.user.foreign_id)
        url = '/api/2/entities'

        entity = {
            'schema': 'Person',
            'collection_id': str(self.coll_a.id),
            'properties': {
                'name': 'Carlos Danger',
                'nationality': 'US'
            }
        }
        self.client.post(url, data=json.dumps(entity),
                         headers=headers,
                         content_type='application/json')
        entity = {
            'schema': 'Person',
            'collection_id': str(self.coll_b.id),
            'properties': {
                'name': 'Carlos Danger',
                'nationality': 'US'
            }
        }
        self.client.post(url, data=json.dumps(entity),
                         headers=headers,
                         content_type='application/json')
        entity = {
            'schema': 'LegalEntity',
            'collection_id': str(self.coll_b.id),
            'properties': {
                'name': 'Carlos Danger',
                'country': 'GB'
            }
        }
        self.client.post(url, data=json.dumps(entity),
                         headers=headers,
                         content_type='application/json')
        entity = {
            'schema': 'Person',
            'collection_id': str(self.coll_b.id),
            'properties': {
                'name': 'Pure Risk',
                'nationality': 'US'
            }
        }
        self.client.post(url, data=json.dumps(entity),
                         headers=headers,
                         content_type='application/json')

        entity = {
            'schema': 'LegalEntity',
            'collection_id': str(self.coll_c.id),
            'properties': {
                'name': 'Carlos Danger',
                'country': 'GB'
            }
        }
        self.client.post(url, data=json.dumps(entity),
                         headers=headers,
                         content_type='application/json')

    def test_xref(self):
        matches = list(iter_matches(self.coll_a, self.authz))
        assert 0 == len(matches), len(matches)
        xref_collection(self.stage, self.coll_a)
        matches = list(iter_matches(self.coll_a, self.authz))
        assert 3 == len(matches), len(matches)

    def test_xref_specific_collections(self):
        matches = list(iter_matches(self.coll_a, self.authz))
        assert 0 == len(matches), len(matches)
        xref_collection(self.stage, self.coll_a,
                        against_collection_ids=[self.coll_c.id])
        matches = list(iter_matches(self.coll_a, self.authz))
        assert 1 == len(matches), len(matches)
