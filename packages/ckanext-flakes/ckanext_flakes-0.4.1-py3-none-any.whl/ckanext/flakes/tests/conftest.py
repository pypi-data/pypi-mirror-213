import factory
import pytest
from pytest_factoryboy import register

from ckan.tests import factories

from ..model import Flake


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    reset_db()
    migrate_db_for("flakes")


@register
class FlakeFactory(factories.CKANFactory):
    class Meta:
        model = Flake
        action = "flakes_flake_create"

    data = factory.Faker("pydict", value_types=(str, int))
