import logging
from typing import Any

import pytest

from polyconf.core import model


lib_logger = logging.getLogger("polyconf")
lib_logger.addHandler(logging.NullHandler())


# TODO: Now that I've split up model into modules, these unit tests should be split appropriately.


@pytest.fixture
def word(faker):
    return faker.word


class BaseMockPlugin(model.Plugin):
    def __init__(self, test_data: list[tuple[str, Any]] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = test_data

    def hydrate(self, context: model.Context) -> model.Context:
        if not self.test_data:
            return context

        for key, value in self.test_data:
            name = key.removeprefix(f"{context.app_prefix}_")
            self.add_result(name=name, value=value, context=context, source=key)
            # context.result.assimilate(name=name, data=value, source=key, parent=context.result)

        return context


class MockNestedPlugin(BaseMockPlugin):
    name = "mock_nested"
    is_flat = False


class MockFlatPlugin(BaseMockPlugin):
    name = "mock_flat"
    is_flat = True


# @pytest.fixture
# def mock_nested_plugin():
#     return MockNestedPlugin(logger=lib_logger)
#
#
# @pytest.fixture
# def mock_flat_plugin():
#     return MockFlatPlugin(logger=lib_logger)


# def test_something_flat(faker):
#     app_name = "acme"
#     app_prefix = app_name.upper()
#
#     word = faker.word
#     mock_flat_plugin = MockFlatPlugin(
#         test_data=[
#             (f"{app_prefix}_{word()}", word()),  # with prefix
#             (word(), word()),  # without prefix
#             # Explicit nesting of value:
#             (word(), {word(): word(), word(): word()}),
#             # Implicit nesting inside key:
#             (f"{word()}__{word()}", word()),
#             # Combined nesting:
#             (f"{word()}__{word()}", {word(): word(), word(): word()}),
#         ],
#         logger=lib_logger,
#     )
#
#     ctx = model.Context(
#         app_name=app_name,
#         app_prefix=app_prefix,
#         trim_prefix=True,
#         given={},
#     )
#     result = mock_flat_plugin.hydrate(ctx)
#
#     assert mock_flat_plugin.name == "mock_flat"
#     assert result.result == {
#         "action": model.Datum(name="action", value="ten", sources={"mock_flat://action"}),
#         "keep": model.Datum(name="keep", value="significant", sources={"mock_flat://ACME_keep"}),
#         "others__least": model.Datum(
#             name="others__least", value={"capital": "two", "color": "hour"}, sources={"mock_flat://others__least"}
#         ),
#         "that": model.Datum(name="that", value={"suggest": "fire", "top": "home"}, sources={"mock_flat://that"}),
#         "work__daughter": model.Datum(name="work__daughter", value="expect", sources={"mock_flat://work__daughter"}),
#     }


# @pytest.mark.skip
class TestNode:
    def test_identity_ne(self, word):
        left = model.Datum(word())
        right = model.Datum(word())
        assert left is not right
        assert left != right

    def test_identity_eq(self, word):
        same_word = word()
        left = model.Datum(same_word)
        right = model.Datum(same_word)
        assert left is not right
        assert left == right

    def test_identity_add_child_node(self):
        top = model.Datum("top")
        top.add_child(model.Datum("child"))
        assert top.children == {model.Datum("child")}
        assert top == model.Datum("top", children={model.Datum("child")})

    def test_identity_add_child_simple(self):
        top = model.Datum("top")
        top.put("child", "child-value")
        assert top.children == {model.Datum("child", "child-value")}  # TODO: Failing
        assert top == model.Datum("top", children={
            model.Datum("child", "child-value")})
        assert top["child"].value == "child-value"

    def test_identity_update_child_simple(self, word):
        top = model.Datum(word())
        child_name = word()
        init_value = word()
        new_value = word()

        top.put(child_name, init_value)
        assert top[child_name].value == init_value

        top.put(child_name, new_value)
        assert top[child_name].value == new_value

    def test_identity_update_child_simple_with_source(self, word):
        top = model.Datum(word())
        child_name = word()
        init_value = word()
        new_value = word()
        source_name = word()

        top.put(child_name, init_value)
        assert top[child_name].sources == set()

        top.put(child_name, new_value, source_name)
        assert top[child_name].sources == {
            source_name,
        }

    def test_get_child(self):
        child = model.Datum("child")
        top = model.Datum(
            "top",
            children={
                child,
            },
        )
        assert top["child"] == child
        assert top.get("child") == child

    def test_looks_like_str(self, word):
        top = model.Datum(name=word(), value="")
        assert top.looks_like() == str
        top = model.Datum(name=word(), value="word")
        assert top.looks_like() == str

    def test_looks_like_int(self, word):
        top = model.Datum(name=word(), value=0)
        assert top.looks_like() == int
        top = model.Datum(name=word(), value=123)
        assert top.looks_like() == int

    def test_looks_like_bool(self, word):
        top = model.Datum(name=word(), value=False)
        assert top.looks_like() == bool
        top = model.Datum(name=word(), value=True)
        assert top.looks_like() == bool

    def test_looks_like_list(self, word):
        top = model.Datum(
            name=word(),
            children={
                model.Datum(name=0, value=word()),
            },
        )
        assert top.looks_like() == list

    def test_looks_like_dict(self, word):
        top = model.Datum(
            name=word(),
            children={
                model.Datum(name=word(), value=word()),
            },
        )
        assert top.looks_like() == dict

    def test_from_dict(self, faker):
        data = {
            (scalar_str := faker.word()): (scalar_str_value := faker.word()),
            (scalar_int := faker.word()): (scalar_int_value := faker.random_number()),
            (list_collection := faker.word()): [
                (lc_scalar_1 := faker.word()),
                (lc_scalar_2 := faker.word()),
                # [
                #     (lc_nested_list_scalar_1 := faker.word()),
                #     (lc_nested_list_scalar_2 := faker.word()),
                # ],
            ],
            (dict_collection := faker.word()): {
                (dc_scalar_str := faker.word()): (dc_scalar_str_value := faker.word()),
                # (dc_nested_dict := faker.word()): [],
                (dc_nested_dict := faker.word()): {
                    (dc_deep_key_1 := faker.word()): (dc_deep_value_1 := faker.word()),
                    (dc_deep_key_2 := faker.word()): (dc_deep_value_2 := faker.word()),
                },
            },
        }
        top = model.Datum.from_dict(data)
        assert top[scalar_str].name == scalar_str
        assert top[scalar_str].value == scalar_str_value
        assert top[scalar_int].value == scalar_int_value
        assert set(top[list_collection].as_native_value) == {lc_scalar_1, lc_scalar_2}
        assert top[dict_collection][dc_scalar_str].value == dc_scalar_str_value
        assert top[dict_collection][dc_nested_dict][dc_deep_key_1].value == dc_deep_value_1
        assert top[dict_collection][dc_nested_dict][dc_deep_key_2].value == dc_deep_value_2


# @pytest.mark.skip
class TestValueTypes:
    def test_value_is_str(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), word()),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        # assert result.result == {
        #     "significant": model.Datum(name="significant", value="action", sources={"mock_flat://significant"}),
        # }
        assert result.result.children == {
            model.Datum(name="significant", value="action", sources={"mock_flat://significant"}),
        }

    def test_value_is_int(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), faker.random_number()),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(name="significant", value=4, sources={"mock_flat://significant"}),
        }

    def test_value_is_bool(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), True),
                (word(), False),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(name="action", value=False, sources={"mock_flat://action"}),
            model.Datum(name="significant", value=True, sources={"mock_flat://significant"}),
        }

    def test_value_is_datum(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        fake_datum_key = word()
        fake_datum_value = word()
        fake_datum = model.Datum(
            name=fake_datum_key,
            value=fake_datum_value,
            children=set(),
            sources={f"mock_flat://{fake_datum_key}"},
        )
        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), fake_datum),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            fake_datum,
        }

    def test_value_is_list_simple(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), [word(), word(), word()]),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        # assert result.result.children == {
        #     model.Datum(name="significant", value="action", sources={"mock_flat://significant"}),
        #     model.Datum(name="significant", value="ten", sources={"mock_flat://significant"}),
        #     model.Datum(name="significant", value="that", sources={"mock_flat://significant"}),
        # }
        assert result.result.children == {
            model.Datum(
                name="significant",
                children={
                    model.Datum(name=0, value="action", sources={"mock_flat://significant"}),
                    model.Datum(name=1, value="ten", sources={"mock_flat://significant"}),
                    model.Datum(name=2, value="that", sources={"mock_flat://significant"}),
                },
                sources={"mock_flat://significant"},
            ),
        }

    def test_value_is_list_needing_recursion(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (
                    word(),
                    [
                        word(),
                        [word(), word()],
                    ],
                ),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(
                name="significant",
                children={
                    model.Datum(name=0, value="action", sources={"mock_flat://significant"}),
                    model.Datum(
                        name=1,
                        children={
                            model.Datum(name=0, value="ten", sources={"mock_flat://significant"}),
                            model.Datum(name=1, value="that", sources={"mock_flat://significant"}),
                        },
                        sources={"mock_flat://significant"},
                    ),
                },
                sources={"mock_flat://significant"},
            ),
        }

    def test_value_is_dict_simple(self, faker):
        word = faker.word
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        test_data = [
            (
                word(),
                {
                    word(): word(),
                    word(): word(),
                },
            ),
        ]
        mock_flat_plugin = MockFlatPlugin(test_data=test_data, logger=lib_logger)
        result = mock_flat_plugin.hydrate(ctx)

        assert test_data == [
            (
                "significant",
                {
                    "action": "ten",
                    "that": "suggest",
                },
            ),
        ]
        assert result.result.children == {
            model.Datum(
                name="significant",
                children={
                    model.Datum(name="action", value="ten", sources={"mock_flat://significant"}),
                    model.Datum(name="that", value="suggest", sources={"mock_flat://significant"}),
                },
                sources={"mock_flat://significant"},
            )
        }


# @pytest.mark.skip
class TestFlatShapes:
    def test_with_prefix(self, word):
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (f"{app_prefix}_{word()}", word()),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(name="significant", value="action", sources={"mock_flat://KEEP_significant"}),
        }

    def test_without_prefix(self, word):
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), word()),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(name="significant", value="action", sources={"mock_flat://significant"}),
        }

    def test_explicit_nesting(self, word):
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        mock_flat_plugin = MockFlatPlugin(
            test_data=[
                (word(), {word(): word(), word(): word()}),
            ],
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(
                name="significant",
                children={
                    model.Datum(name="action", value="ten", sources={"mock_flat://significant"}),
                    model.Datum(name="that", value="suggest", sources={"mock_flat://significant"}),
                },
                sources={"mock_flat://significant"},
            )
        }

    def test_implicit_nesting(self, word):
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        lvl1_k1 = word()
        lvl1_k2 = word()
        lvl2_k1 = word()
        lvl2_k2 = word()
        test_data = [
            (f"{lvl1_k1}__{lvl2_k1}", word()),
            (f"{lvl1_k2}__{lvl2_k2}", word()),
        ]
        mock_flat_plugin = MockFlatPlugin(
            test_data=test_data,
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        # Nominally:
        _ = {
            "significant": {
                "ten": "suggest",
                "that": "fire",
            },
            "action": {
                "ten": "top",
                "that": "home",
            },
        }
        assert test_data == [
            ("significant__ten", "suggest"),
            ("action__that", "fire"),
        ]

        assert len(result.result.children) == 2

        assert result.result.get("significant") is not None
        assert result.result.get("significant").children == {
            model.Datum(name="ten", value="suggest", sources={"mock_flat://significant__ten"}),
        }

        assert result.result.get("action") is not None
        assert result.result.get("action").children == {
            model.Datum(name="that", value="fire", sources={"mock_flat://action__that"}),
        }

    def test_implicit_nesting_with_merged_keys(self, word):
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
            given={},
        )

        lvl1_k1 = word()
        lvl1_k2 = word()
        lvl2_k1 = word()
        lvl2_k2 = word()
        test_data = [
            (f"{lvl1_k1}__{lvl2_k1}", lvl2_a_k1v1 := word()),
            (f"{lvl1_k1}__{lvl2_k2}", lvl2_a_k2v2 := word()),
            (f"{lvl1_k2}__{lvl2_k1}", lvl2_b_k1v1 := word()),
            (f"{lvl1_k2}__{lvl2_k2}", lvl2_b_k2v2 := word()),
        ]
        mock_flat_plugin = MockFlatPlugin(
            test_data=test_data,
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert test_data == [
            ("significant__ten", "suggest"),
            ("significant__that", "fire"),
            ("action__ten", "top"),
            ("action__that", "home"),
        ]
        assert result.result.children == {
            model.Datum(
                name=lvl1_k1,
                children={
                    model.Datum(name=lvl2_k1, value=lvl2_a_k1v1, sources={f"mock_flat://{lvl1_k1}__{lvl2_k1}"}),
                    model.Datum(name=lvl2_k2, value=lvl2_a_k2v2, sources={f"mock_flat://{lvl1_k1}__{lvl2_k2}"}),
                },
                sources={f'mock_flat://{lvl1_k1}__{lvl2_k1}', f'mock_flat://{lvl1_k1}__{lvl2_k2}'},
            ),
            model.Datum(
                name=lvl1_k2,
                children={
                    model.Datum(name=lvl2_k1, value=lvl2_b_k1v1, sources={f"mock_flat://{lvl1_k2}__{lvl2_k1}"}),
                    model.Datum(name=lvl2_k2, value=lvl2_b_k2v2, sources={f"mock_flat://{lvl1_k2}__{lvl2_k2}"}),
                },
                sources={f'mock_flat://{lvl1_k2}__{lvl2_k1}', f'mock_flat://{lvl1_k2}__{lvl2_k2}'},
            ),
        }

    def test_combined_explicit_and_implicit_nesting(self, word):
        app_name = word()
        app_prefix = app_name.upper()
        ctx = model.Context(
            app_name=app_name,
            app_prefix=app_prefix,
            trim_prefix=True,
        )

        w01 = word()  # 'significant'
        w02 = word()  # 'action'
        w03 = word()  # 'ten'
        w04 = word()  # 'that'
        w05 = word()  # 'suggest'
        w06 = word()  # 'fire'
        w07 = word()  # 'top'
        w08 = word()  # 'home'
        w09 = word()  # 'work'
        w10 = word()  # 'daughter'
        w11 = word()  # 'expect'
        w12 = word()  # 'others'

        test_data = [
            (f"{w01}__{w02}", {w03: w04, w05: w06}),
            (f"{w07}__{w08}", {w09: w10, w11: w12}),
        ]
        mock_flat_plugin = MockFlatPlugin(
            test_data=test_data,
            logger=lib_logger,
        )
        result = mock_flat_plugin.hydrate(ctx)

        assert result.result.children == {
            model.Datum(
                name=w01,
                children={
                    model.Datum(
                        name=w02,
                        children={
                            model.Datum(name=w03, value=w04, sources={f"mock_flat://{w01}__{w02}"}),
                            model.Datum(name=w05, value=w06, sources={f"mock_flat://{w01}__{w02}"}),
                        },
                        sources={f"mock_flat://{w01}__{w02}"},
                    )
                },
                sources={f"mock_flat://{w01}__{w02}"},
            ),
            model.Datum(
                name=w07,
                children={
                    model.Datum(
                        name=w08,
                        children={
                            model.Datum(name=w09, value=w10, sources={f"mock_flat://{w07}__{w08}"}),
                            model.Datum(name=w11, value=w12, sources={f"mock_flat://{w07}__{w08}"}),
                        },
                        sources={f"mock_flat://{w07}__{w08}"},
                    )
                },
                sources={f"mock_flat://{w07}__{w08}"},
            ),
        }
        assert result.result.serialize() == {
            "name": "root",
            "children": [
                {
                    "name": w01,
                    "children": [
                        {
                            "name": w02,
                            "children": [
                                # Note the order. This list forces manual sorting here.
                                {"name": w05, "value": w06, "sources": [f"mock_flat://{w01}__{w02}"]},
                                {"name": w03, "value": w04, "sources": [f"mock_flat://{w01}__{w02}"]},
                            ],
                            "sources": [f"mock_flat://{w01}__{w02}"],
                        }
                    ],
                    "sources": [f"mock_flat://{w01}__{w02}"],
                },
                {
                    "name": w07,
                    "children": [
                        {
                            "name": w08,
                            "children": [
                                # Note the order. This list forces manual sorting here.
                                {"name": w11, "value": w12, "sources": [f"mock_flat://{w07}__{w08}"]},
                                {"name": w09, "value": w10, "sources": [f"mock_flat://{w07}__{w08}"]},
                            ],
                            "sources": [f"mock_flat://{w07}__{w08}"],
                        }
                    ],
                    "sources": [f"mock_flat://{w07}__{w08}"],
                },
            ],
        }


def test_implicit_expansion(faker):
    word = faker.word
    lvl1_k = word()
    lvl2_k = word()
    lvl2_v = word()

    plugin = MockFlatPlugin(logger=lib_logger)
    result = plugin.expand_implicit_nesting(name=f"{lvl1_k}__{lvl2_k}", value=lvl2_v)

    assert result == (
        lvl1_k,
        {lvl2_k: lvl2_v},
    )
    assert result == (
        "keep",
        {"significant": "action"},
    )


class TestSerialization:
    def test_simple_value(self, word):
        datum = model.Datum(
            name=(name := word()),
            value=(value := word()),
            sources={f"mock_flat://{name}"},
        )
        assert datum.serialize() == {
            "name": name,
            "value": value,
            "sources": [f"mock_flat://{name}"],
        }

    def test_simple_collection_list(self, word):
        datum = model.Datum(
            name=(name := word()),
            children={
                model.Datum(name=0, value=(c_value_1 := word())),
                model.Datum(name=1, value=(c_value_2 := word())),
            },
            sources={f"mock_flat://{name}"},
        )
        assert datum.serialize() == {
            "name": name,
            "children": [
                {"name": 0, "value": c_value_1},
                {"name": 1, "value": c_value_2},
            ],
            "sources": [f"mock_flat://{name}"],
        }

    def test_simple_collection_dict(self, word):
        datum = model.Datum(
            name=(name := word()),
            children={
                model.Datum(name=(c_name_1 := word()), value=(c_value_1 := word())),
                model.Datum(name=(c_name_2 := word()), value=(c_value_2 := word())),
            },
            sources={f"mock_flat://{name}"},
        )
        assert datum.serialize() == {
            "name": name,
            "children": [
                {"name": c_name_1, "value": c_value_1},
                {"name": c_name_2, "value": c_value_2},
            ],
            "sources": [f"mock_flat://{name}"],
        }
