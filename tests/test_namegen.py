import pytest

from hyperborea3.namegen import (
    get_name_sql,
    process_gender,
    limit_repeating_chars,
    generate_epithet,
    generate_common_name,
    generate_amazon_name,
    generate_anglosaxon_name,
    generate_atlantean_name,
    generate_carolingian_frankish_name,
    generate_esquimaux_ixian_name,
    generate_esquimaux_name,
    generate_greek_name,
    generate_half_blood_pict_name,
    generate_hyperborean_name,
    generate_ixian_name,
    generate_keltic_name,
    generate_kimmerian_name,
    generate_kemmeri_kelt_name,
    generate_lapp_name,
    generate_lemurian_name,
    generate_moorish_name,
    generate_mu_name,
    generate_oon_name,
    generate_pictish_name,
    generate_roman_name,
    generate_tlingit_name,
    generate_viking_name,
    generate_yakut_name,
    generate_name,
)
from hyperborea3.valid_data import VALID_GENDERS, VALID_RACES_BY_ID


def test_get_name_sql():
    expected = """
            SELECT name
            FROM t150_common_name_elements
            WHERE id = ?
        """
    actual = get_name_sql("t150_common_name_elements")
    assert expected == actual


def test_get_name_sql_exc():
    table_name = "fake_table"
    with pytest.raises(NameError) as e:
        get_name_sql(table_name)
        assert str(e) == f"No table named '{table_name}' found in database."


def test_process_gender():
    assert process_gender("Female") == "Female"
    assert process_gender("Male") == "Male"
    assert process_gender("Non-Binary") in ["Female", "Male"]
    assert process_gender("random") in ["Female", "Male"]


def test_limit_repeating_characters():
    assert limit_repeating_chars("Donnnnnnnkey") == "Donnkey"
    assert limit_repeating_chars("AAAABBBBCCCCDDDD") == "AABBCCDD"


def test_generate_epithet():
    min_len = 7
    max_len = 16
    epithet = generate_epithet()
    assert isinstance(epithet, str)
    assert epithet.startswith("“")
    assert epithet.endswith("”")
    assert min_len + 2 <= len(epithet) <= max_len + 2


def test_generate_common_name():
    name = generate_common_name("random")
    assert isinstance(name, str)
    assert " " in name
    assert len(name) >= 7


def test_generate_amazon_name():
    name = generate_amazon_name("random")
    assert isinstance(name, str)
    assert " " in name
    assert len(name) >= 7


def test_generate_anglosaxon_name():
    name = generate_anglosaxon_name("random")
    assert isinstance(name, str)
    assert len(name) >= 5


def test_generate_atlantean_name():
    name = generate_atlantean_name("random")
    assert isinstance(name, str)
    assert " " in name
    assert len(name) >= 7


def test_generate_carolingian_frankish_name():
    name = generate_carolingian_frankish_name("random")
    assert isinstance(name, str)
    assert len(name) >= 5


def test_generate_esquimaux_ixian_name():
    name = generate_esquimaux_ixian_name("random")
    assert isinstance(name, str)
    assert len(name) >= 2


def test_generate_esquimaux_name():
    name = generate_esquimaux_name("random")
    assert isinstance(name, str)
    assert len(name) >= 3


def test_generate_greek_name():
    name = generate_greek_name("random")
    assert isinstance(name, str)
    assert " " in name
    assert len(name) >= 9


def test_generate_hyperborean_name():
    name = generate_hyperborean_name("random")
    assert isinstance(name, str)
    assert " " in name
    assert len(name) >= 12


def test_generate_ixian_name():
    female_name = generate_ixian_name("Female")
    assert isinstance(female_name, str)
    assert len(female_name.split()) == 3
    assert female_name.split()[1] in ["gunê", "thugatêr"]
    assert len(female_name) >= 13
    male_name = generate_ixian_name("Male")
    assert isinstance(male_name, str)
    assert len(male_name.split()) == 2
    assert len(male_name) >= 9


def test_generate_keltic_name():
    name = generate_keltic_name("random")
    assert isinstance(name, str)
    assert len(name) >= 3


def test_generate_kimmerian_name():
    name = generate_kimmerian_name("rnadom")
    assert isinstance(name, str)
    assert " " in name
    assert len(name) >= 12


def test_generate_kemmeri_kelt_name():
    name = generate_kemmeri_kelt_name("random")
    assert isinstance(name, str)
    assert len(name) >= 3


def test_generate_lapp_name():
    name = generate_lapp_name("random")
    assert isinstance(name, str)
    assert " of the " in name
    assert name.endswith(" Clan")
    assert len(name) >= 19


def test_generate_lemurian_name():
    name = generate_lemurian_name("random")
    assert isinstance(name, str)
    assert len(name) >= 2


def test_generate_moorish_name():
    male_name = generate_moorish_name("Male")
    assert isinstance(male_name, str)
    assert " ag-" in male_name
    assert len(male_name) >= 12
    female_name = generate_moorish_name("Female")
    assert isinstance(female_name, str)
    assert " ult-" in female_name
    assert len(female_name) >= 13


def test_generate_mu_name():
    name = generate_mu_name("random")
    assert isinstance(name, str)
    assert 4 <= len(name) <= 20


def test_generate_oon_name():
    name = generate_oon_name("random")
    assert isinstance(name, str)
    assert len(name) == 9
    assert 1 <= int(name) <= 999_999_999


def test_generate_pictish_name():
    female_name = generate_pictish_name("Female")
    assert isinstance(female_name, str)
    assert 3 <= len(female_name) <= 11
    male_name = generate_pictish_name("Male")
    assert isinstance(male_name, str)
    assert 6 <= len(male_name) <= 37


def test_generate_half_blood_pict_name():
    name = generate_half_blood_pict_name("random")
    assert isinstance(name, str)
    assert 3 <= len(name) <= 37


def test_generate_roman_name():
    female_name = generate_roman_name("Female")
    assert isinstance(female_name, str)
    assert 14 <= len(female_name) <= 28
    male_name = generate_roman_name("Male")
    assert isinstance(male_name, str)
    assert 16 <= len(male_name) <= 30


def test_generate_tlingit_name():
    name = generate_tlingit_name("random")
    assert isinstance(name, str)
    assert 8 <= len(name) <= 15


def test_generate_viking_name():
    female_name = generate_viking_name("Female")
    assert isinstance(female_name, str)
    assert 13 <= len(female_name) <= 29
    male_name = generate_viking_name("Male")
    assert isinstance(male_name, str)
    assert 12 <= len(male_name) <= 28


def test_generate_yakut_name():
    female_name = generate_yakut_name("Female")
    assert isinstance(female_name, str)
    assert 3 <= len(female_name) <= 10
    male_name = generate_yakut_name("Male")
    assert isinstance(male_name, str)
    assert 5 <= len(male_name) <= 9


def test_generate_name():
    for race_id in VALID_RACES_BY_ID.keys():
        for gender in VALID_GENDERS:
            name = generate_name(race_id, gender)
            assert isinstance(name, str)
            assert len(name) >= 2
