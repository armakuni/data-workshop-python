from typing import Generator

from polyfactory.factories.pydantic_factory import ModelFactory

from data_workshop.repositories.energy_data_record import EnergyDataRecord


class EnergyDataRecordFactory(ModelFactory[EnergyDataRecord]):
    __model__ = EnergyDataRecord


class EnergyDataRepository:
    def __init__(self) -> None:
        self.factory = EnergyDataRecordFactory()

    def list_all(self) -> Generator[EnergyDataRecord, None, None]:
        while True:
            yield self.factory.build()
