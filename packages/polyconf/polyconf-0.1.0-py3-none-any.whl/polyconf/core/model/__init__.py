"""PolyConf core model.

Notes:
    - Although a lot of the dataclass magic is nullified, it's still used here for its excellent repr().
    - Tricky stuff to be aware of:
        - I'm not quite 100% settled on the type for "children".
            - It's currently a set, which has the benefit of order-agnostic comparison and feels somewhat natural.
            - I've been tempted to switch to a dict for the sake of explicit index keys.
        - Similarly, I'm not quite 100% settled on the type for "sources".
            - The first bullet for "children" also holds true here.
            - But the primary reasoning is that insertion order can carry implicit data for when the value was seen.
                - In this case, duplicates are actually desired, but it's not clear this is a _realistic_ scenario.
        - Serialization casts sets as lists.
            - "children" members get pre-sorted, which aids in comparison during testing.
                - When using a fake value generator (like faker), such that the actual value isn't readily known,
                  then be careful about ordering.  The serialized output is sorted but the INPUT might not be.

Definitions:
    - scalar -- I'm slightly loading this term to specifically mean, "primitive, non-collection, includes null".
        - Put another way, it's generic for "str | int | bool | None"
        - A motivation is ease of serialization (including JSON).
    - datum -- Is the blessed "augmented scalar".
        - Although it has an attribute that is a collection, a datum itself (class level) is not a collection.
        - Note the use of "scalar" is more restrictive and does not imply "datum".
    - collection -- Is specifically constrained to native collection types "set | list | dict".
        - In general, the members/values are "scalars" (as defined above) and/or "datums".
        - Specific to representing collections as datums,
          in the case of dict, the keys are explicit and the type implies the collection type.
            - int key implies a list
            - str key implies a dict
        - Note there currently isn't a case for collections of collections (perhaps called "2nd order collection"?).
            - This is because when composing data with "datums",
              collection are always represented with a datum and its "children" attribute.
    - serialization -- In general (outside of PolyConf), usually implies targeting outside the application,
      whether to disk or over the network, but PolyConf's usage is closer to "marshalling" (should I refactor?).
      The target is portability within the application, thus the "de/serialize()" methods produce native Python
      objects and not a (usually JSON) string.
        - A motivation (perhaps primary) is to ease deep merging between "datums",
          which is a complex topic/task.
        - I vendored a library ("deepmerge") that has exhaustive support for deep merging dictionaries.
          Therefore, the "merge" process serials each side to dictionaries, the deserializes the result.
        - Currently, the use cases are constrained within PolyConf, but it's easily conceivable that the
          application using PolyConf could use it, too (thus it's publicly exposed).

Maxims:
    - "value" and "children" are mutually exclusive.
    - "value" indicates a leaf node
    - "value" is always a scalar object
    - "children" is a collection
    - "children" members are always Datums
    - child datums:
        - The name attribute is basically the index of the collection.
        - if name is an int, the "children" collection is a list
        - if name is a str, the "children" collection is a dict

Todo:
    - General naming consistency.
        - Terms like "put", "assimilate", "from_dict", etc. are unclear -- reconsider naming.
    - Review test coverage.
    - Clean up early churn -- unused methods, properties, etc.
    - Consider logging usage.
    - Fill out types.
    - Clearly document public API and intended usage patterns.
    - Fill out docstrings.
"""

from __future__ import annotations

from polyconf.core.model.context import Context
from polyconf.core.model.datum import Datum
from polyconf.core.model.plugin import Plugin
from polyconf.core.model.status import Status


if __name__ == "__main__":
    ...
    # Ad hoc testing goes here.

    d = Datum.from_dict(
        data={
            # "foo": "bar",
            # "foo": {"bar": "baz"},
            "foo": {"bar": {"baz": "buz"}},
            # "foo": ["bar", "baz"],
        },
        source="foo",
    )
    print(d)
    print(d.get("foo"))
    print(d["foo"])
    foo: Datum = d["foo"] or Datum("")
    print(foo.as_native_value)

    # foo = Datum(
    #     name='foo',
    #     value=None,
    #     children={
    #         Datum(
    #             name='bar',
    #             value=None,
    #             children={
    #                 Datum(name='baz', value='buz', children=set(), sources={'foo'}),
    #             },
    #             sources={'foo'},
    #         ),
    #     },
    #     sources={'foo'},
    # )

    bar = Datum(
        name="bar",
        value=None,
        children={
            Datum(name="baz", value="buz", children=set(), sources={"foo"}),
        },
        sources={"foo"},
    )
    foo.remove_child(bar)
    print(foo.as_native_value)

    # # --------------------------------------------------------------------------
    # # Setup
    # from dataclasses import asdict, fields
    # from json import dumps
    # import logging
    #
    # from faker import Faker
    #
    # logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger("acme-logger")
    # faker = Faker()
    # w = faker.word
    #
    # def dprint(datum: Datum, heading: str):
    #     print("-" * 80)
    #     print(f"{heading.upper()}:")
    #     print(">>> str()")
    #     pprint(datum)
    #     print(">>> json.dumps()")
    #     print(dumps(datum.serialize(), indent=4))
    #     print(">>> serialize()")
    #     pprint(datum.serialize())
    #     print()

    # --------------------------------------------------------------------------
    # Tests

    # dprint(d1, "before")
    # dd1 = d1.serialize()
    # ddd1 = Datum.deserialize(dd1)
    # dprint(ddd1, "after")

    # dprint(d3, "before")
    # dd1 = d3.serialize()
    # ddd1 = Datum.deserialize(dd1)
    # dprint(ddd1, "after")

    # --------------------------------------------------------------------------

    # app_name = "acme"
    # app_prefix = app_name.upper()
    # ctx = Context(
    #     app_name=app_name,
    #     app_prefix=app_prefix,
    #     trim_prefix=True,
    #     given={},
    # )
    #
    # test_data = [
    #     (w(), w()), # value is plain scalar
    #     (f"{w()}__{w()}", w()), # single-level nesting
    #     (f"{w()}__{w()}__{w()}__{w()}__{w()}", w()),  # multi-level nesting
    #
    #     (w(), [w(), w(), w()]), # value is list
    #     (f"{w()}__{w()}", [w(), w(), w()]), # single-level nesting
    #     (f"{w()}__{w()}__{w()}", [w(), w(), w()]), # multi-level nesting
    #
    #     (w(), {w(): w()}), # value is dict
    #     (f"{w()}__{w()}", {w(): w()}), # single-level nesting
    #     (f"{w()}__{w()}__{w()}__{w()}__{w()}", {w(): w()}), # multi-level nesting
    # ]
    #
    # mock_flat_plugin = MockFlatPlugin(test_data=test_data, logger=logger)
    # result = mock_flat_plugin.hydrate(ctx)
    #
    # # pprint(result.result.children)
    # pprint(test_data)
    # print()
    # pprint(result.result.to_dict()["root"])
    # # print()
    # # pprint(result.result)
