""" Testing the full functionality of the marinaders toolkit

These tests focus on the availability and consistency of the database api
"""

import sys
import pytest
import pandas as pd

sys.path.append("..")

import marinvaders.main as ml  # noqa: E402
import marinvaders.readers as readers  # noqa: E402


def test_ecoregions():
    """
    test existence and fields of ecoregion
    """
    marine_ecoregions = ml.marine_ecoregions()
    assert len(marine_ecoregions) > 0
    assert [
        "ECO_CODE",
        "ECO_CODE_X",
        "ECOREGION",
        "PROVINCE",
        "REALM",
        "geometry",
    ] == list(marine_ecoregions.columns)


def test_get_obis_raise_error():
    """
    get_obis returns error when neither aphiaID or eco_code is specified
    """
    with pytest.raises(ValueError):
        ml._get_obis()

    with pytest.raises(NotImplementedError):
        ml._get_obis(eco_code=1, aphia_id=1)


def test_species_class():
    """
    test instance of Species object for random species which we assume
    is always present at obis

    We using Hypnea musciformis as an example here, which is alien in Hawaii
    """
    ds = ml.Species("urn:lsid:marinespecies.org:taxname:145634")
    assert ds.aphia_id == 145634
    assert len(ds._obis) > 0
    assert isinstance(ds._obis, pd.DataFrame)
    assert "Hawaii" in ds.reported_as_alien.ECOREGION.values
    assert len(ds.reported_as_alien) < len(ds.all_occurrences)
    assert len(set(ds.all_occurrences[
            ds.all_occurrences.establishmentMeans == "Alien"
        ].ECO_CODE).symmetric_difference(
        set(ds.reported_as_alien.ECO_CODE))) == 0


def test_marine_life_class():
    """
    test instance of MarineLife object for specific eco code
    """
    cocos_code = 20169
    cocos = ml.MarineLife(eco_code=cocos_code)
    # there should be alien species
    assert cocos.alien_species.iloc[0, :].species in cocos.all_species.species.values
    assert len(cocos.alien_species) < len(cocos.all_species)


def test_big_region_obis_api():
    """
    the obis API calls has issue with large regions.
    It needs special code and this test is to make
    sure all big regions will run properly.
    Here we use High Arctic Archipelago (code 25010)
    """
    arctic = ml.MarineLife(25010)
    assert arctic._obis.empty is False
    assert len(arctic.all_species) > 0


def test_readers():
    """
    test data readers for different stored datasets

    This does not test the reading of the IUCN GISD and Red-List data.
    These files can not be added to the data we re-distribute, tests
    are included in the manual integration_evaluation.py
    """
    ecomrgidlink = readers.eco_mrgid_link()
    assert isinstance(ecomrgidlink, pd.DataFrame)
    assert len(ecomrgidlink) > 0

    natcon = readers.read_natcon()
    assert isinstance(natcon, pd.DataFrame)
    assert len(natcon) > 0

    gisd_worms_link = readers.read_gisd_worms_link()
    assert isinstance(gisd_worms_link, pd.DataFrame)
    assert len(gisd_worms_link) > 0


def test_ecoregions_plot():
    """
    the plot calls should not cause any error
    """

    ml.plot(eco_code=20002, show=False)

    species = ml.Species(145634)
    species.plot(show=False)
