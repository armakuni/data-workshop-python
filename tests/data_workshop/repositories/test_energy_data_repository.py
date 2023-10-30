from data_workshop.repositories.energy_data_repository import EnergyDataRepository


def test_energy_data_repository() -> None:
    energy_data_repository = EnergyDataRepository()

    items = energy_data_repository.list_all()
    assert next(items) is not None
    assert next(items) is not None
    assert next(items) is not None
    assert next(items) is not None
    assert next(items) is not None
    assert next(items) is not None
    assert next(items) is not None
