def dict_strategy_merge(merger, path, base, other):
    """
    For keys that do not exist, use them directly.
    If the key exists  in both dictionaries, attempt a value merge.
    """
    for k, v in other.items():
        if k not in base:
            base[k] = v
        else:
            base[k] = merger.value_strategy(path + [k], base[k], v)
    return base


strategy_map = {
    list: lambda _merger, _path, base, other: base + other,  # (list append)
    dict: dict_strategy_merge,
    set: lambda _merger, _path, base, other: base | other,  # (set union)
}


class Merger:

    def merge(self, base, other):
        return self.value_strategy(path=[], base=base, other=other)

    def value_strategy(self, path, base, other):
        # Mismatch types -- other overrides base
        if not (isinstance(base, type(other)) or isinstance(other, type(base))):
            return other

        # Execute strategy
        if strategy := strategy_map.get(type(other)):
            return strategy(self, path, base, other)

        # Fall back to other
        return other


deep = Merger()
