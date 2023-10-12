import time

from data_workshop.actors.adding_actor import AddingActor
from data_workshop.actors.averaging_actor import AveragingActor
from data_workshop.actors.country_splitter_actor import CountrySplitterActor
from data_workshop.actors.energy_data_spout_actor import EnergyDataSpoutActor
from data_workshop.actors.get_renewables_consumption_actor import (
    GetRenewableConsumptionActor,
)
from data_workshop.repositories.energy_data_repository import EnergyDataRepository

if __name__ == "__main__":
    averaging_actor = AveragingActor.start()

    uk_renewables_consumption_actor = GetRenewableConsumptionActor.start(
        averaging_actor
    )
    usa_renewables_consumption_actor = GetRenewableConsumptionActor.start(
        averaging_actor
    )

    country_splitter_actor = CountrySplitterActor.start(
        uk_renewables_consumption_actor, usa_renewables_consumption_actor
    )
    repo = EnergyDataRepository()
    energy_spout_actor = EnergyDataSpoutActor.start(country_splitter_actor, repo)

    adding_actor = AddingActor.start()

    while True:
        time.sleep(100)
