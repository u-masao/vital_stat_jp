import datetime

from vital_statistics_jp import __version__, read_prompt

CATEGORIES = {
    "english": {
        "deaths",
        "divorces",
        "foetal deaths",
        "live births",
        "marriages",
        "natural change",
    },
    "japanese": {"自然増減", "死産", "婚姻", "出生", "離婚", "死亡"},
}


def test_version():
    assert __version__ == "0.1.0"


def test_default():

    df = read_prompt()

    assert df.shape[0] >= 1236  # 2022/05/05
    assert df.shape[1] == 3
    assert set(df.category.value_counts().index) == CATEGORIES["english"]
    assert df.category.value_counts().std() == 0


def test_lang():

    df = read_prompt(lang="japanese")

    assert set(df.category.value_counts().index) == CATEGORIES["japanese"]


def test_year():
    year_from = 2010
    year_to = 2011
    df = read_prompt(
        year_from=year_from, year_to=year_to, month_to=12, verbose=True
    )

    assert len(df) == len(CATEGORIES["english"]) * 12 * (
        year_to - year_from + 1
    )
    assert df.ts.dt.year.min() == year_from
    assert df.ts.dt.year.max() == year_to


def test_month():
    year_from = 2010
    year_to = 2015
    for month_to in (1, 6, 12):
        df = read_prompt(
            year_from=year_from, year_to=year_to, month_to=month_to
        )
        assert len(df) == len(CATEGORIES["english"]) * (
            12 * (year_to - year_from) + month_to
        )
        assert df.ts.dt.year.min() == year_from
        assert df.ts.dt.year.max() == year_to


def test_ignore_error():
    year_from = 2019
    year_to = datetime.datetime.now().year + 1
    df = read_prompt(
        year_from=year_from,
        year_to=year_to,
        month_to=12,
        verbose=True,
        ignore_error=True,
    )
    assert len(df) == len(CATEGORIES["english"]) * 12 * 3
