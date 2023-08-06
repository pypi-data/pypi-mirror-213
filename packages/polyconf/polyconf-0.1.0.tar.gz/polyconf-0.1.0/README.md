# PolyConf

## Credit

The `polyconf.core.deepmerge` module is a heavy refactor of [gh://toumorokoshi/deepmerge](https://github.com/toumorokoshi/deepmerge).
(More specifically, I based it on the tip of `main` at the time, which was commit `33a078ac7a29b63dfb91fea806cc6b96ede3fd23`.)
I don't want this library to have 3rd party dependencies, so I basically stripped the dynamic configurability of `deepmerge`,
such that the behavior of `always_merge()` became the _only_ behavior.

The keyword arguments are quite self-explanatory, so to concisely define the behavior, consider this snippet:

```python
always_merger = Merger(
    type_strategies=[
        (list, "append"),
        (dict, "merge"),
        (set, "union"),
    ],
    fallback_strategies=["override"],
    type_conflict_strategies=["override"],
)
```

The refactor is _heavy_, indeed.  At the time of this writing, `cloc` calculates it at only `22` lines of code.
However, I still want to give credit where it's due because there are a couple lessons in recursion
and fallback behavior that would have been painful to work out myself.
It also serves as a reminder for future reference because if I ever reverse the moratorium on 3rd party libs,
I'll happily depend on `deepmerge` directly.
