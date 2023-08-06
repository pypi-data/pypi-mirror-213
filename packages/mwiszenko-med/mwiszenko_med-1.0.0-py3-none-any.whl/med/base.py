from __future__ import annotations

import copy
from collections import defaultdict

from tqdm import tqdm


class ItemSet:
    def __init__(self, items: list[str]):
        self.items: list[str] = items

    def __len__(self):
        return len(self.items)

    def __setitem__(self, item_number: int, data: str):
        self.items[item_number] = data

    def __getitem__(self, item_number: int):
        return self.items[item_number]

    def __delitem__(self, item_number: int):
        del self.items[item_number]

    def __str__(self):
        return "(" + " ".join(self.items) + ")"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key: str):
        return key in self.items

    def append(self, item: str):
        self.items.append(item)
        return self.items


class Sequence:
    def __init__(self, item_sets: list[ItemSet]):
        self.item_sets: list[ItemSet] = item_sets

    def __len__(self):
        return len(self.item_sets)

    def __setitem__(self, item_set_number: int, data: ItemSet):
        self.item_sets[item_set_number] = data

    def __getitem__(self, item_set_number: int):
        return self.item_sets[item_set_number]

    def __delitem__(self, item_set_number: int):
        del self.item_sets[item_set_number]

    def __str__(self):
        return "(" + "".join(str(i) for i in self.item_sets) + ")"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key: str):
        return any(key in its for its in self.item_sets)

    def append(self, item_set: ItemSet):
        self.item_sets.append(item_set)
        return self


class DataSet:
    def __init__(self, sequences: list[Sequence]):
        self.sequences: list[Sequence] = sequences

    def __len__(self):
        return len(self.sequences)

    def __setitem__(self, sequence_number: int, data: Sequence):
        self.sequences[sequence_number] = data

    def __getitem__(self, sequence_number: int):
        return self.sequences[sequence_number]

    def __delitem__(self, sequence_number: int):
        del self.sequences[sequence_number]

    def __str__(self):
        return "\n".join(
            str(idx + 1) + ": " + str(i) for idx, i in enumerate(self.sequences)
        )

    def remove_all(self, keys: set[str]):
        for s in self.sequences:
            for its in s.item_sets:
                for i in its.items:
                    if i in keys:
                        del i

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key: str):
        return any(key in seq for seq in self.sequences)

    def append(self, seq: Sequence):
        self.sequences.append(seq)
        return self

    def get_set(self):
        return set(
            [
                item
                for sublist in [
                    item.items for sublist in self.sequences for item in sublist
                ]
                for item in sublist
            ]
        )


def read_sequence_file(filename: str) -> DataSet:
    sequences: list[Sequence] = []

    try:
        with open(filename, "r", encoding="UTF-8") as file:
            while line := file.readline():
                item_sets: list[ItemSet] = []
                for its in line.strip().split(" -1 "):
                    if its != "-2":
                        item_sets.append(ItemSet(its.split(" ")))
                sequences.append(Sequence(item_sets))
    except FileNotFoundError:
        msg = filename + " does not exist."
        print(msg)
    return DataSet(sequences)


def prefix_span(
    ds: DataSet, min_sup: float, min_length: int, max_length: int
) -> dict[Sequence, int]:
    results: dict[Sequence, int] = {}
    initial_proj: dict[int, tuple[int, int]] = {}
    bar = tqdm()
    for i in range(len(ds)):
        initial_proj[i] = (0, 0)
    prefix_span_rec(
        ds, initial_proj, Sequence([]), min_sup, min_length, max_length, results, bar
    )
    return results


def prefix_span_rec(
    ds: DataSet,
    proj: dict[int, tuple[int, int]],
    seq_s: Sequence,
    min_sup: float,
    min_length: int,
    max_length: int,
    results: dict[Sequence, int],
    bar: tqdm,
) -> None:
    seq_to_sup: dict[Sequence, int] = get_sequences(ds, proj, seq_s)
    if len(seq_s) == 0:
        rare_items: set[str] = set()
        for seq_r, sup_r in seq_to_sup.items():
            if sup_r < min_sup:
                rare_items.add(seq_r.item_sets[0].items[0])
        if len(rare_items) > 0:
            ds.remove_all(rare_items)
        bar.total = len(ds.get_set())
    for seq_r, sup_r in seq_to_sup.items():
        if sup_r > min_sup:
            seq_length = sum(len(i) for i in seq_r.item_sets)
            if seq_length >= min_length:
                results[seq_r] = sup_r
            if seq_length < max_length:
                new_proj: dict[int, tuple[int, int]] = project(ds, proj, seq_r)
                prefix_span_rec(
                    ds, new_proj, seq_r, min_sup, min_length, max_length, results, bar
                )
        if len(seq_s) == 0:
            bar.update(1)


def project(
    ds: DataSet, proj: dict[int, tuple[int, int]], seq_r: Sequence
) -> dict[int, tuple[int, int]]:
    new_proj: dict[int, tuple[int, int]] = {}
    for idx, num in proj.items():
        new_num = get_place(seq_r, ds.sequences[idx])
        if new_num[0] != -1:
            new_proj[idx] = new_num
    return new_proj


def get_sequences(
    ds: DataSet, proj: dict[int, tuple[int, int]], seq: Sequence
) -> dict[Sequence, int]:
    seq_to_sup: dict[Sequence, int] = {}
    same_its: defaultdict[str, int] = defaultdict(int)
    next_its: defaultdict[str, int] = defaultdict(int)

    for idx, num in proj.items():
        if len(seq) > 0:
            characters = set(ds.sequences[idx].item_sets[num[0]].items[num[1] + 1 :])
            for i in ds.sequences[idx].item_sets[num[0] + 1 :]:
                new_num = get_place_its(seq.item_sets[-1], i)
                if new_num != -1:
                    characters.update(set(i.items[new_num + 1 :]))
            for c in characters:
                same_its[c] += 1

        characters = set()
        if len(seq) == 0:
            characters.update(
                set(
                    it
                    for lst in ds.sequences[idx].item_sets[num[0] :]
                    for it in lst.items
                )
            )
        else:
            characters.update(
                set(
                    it
                    for lst in ds.sequences[idx].item_sets[num[0] + 1 :]
                    for it in lst.items
                )
            )
        for c in characters:
            next_its[c] += 1

    for c, n in next_its.items():
        seq_to_sup[copy.deepcopy(seq).append(ItemSet([c]))] = n
    for c, n in same_its.items():
        new_seq = copy.deepcopy(seq)
        new_seq.item_sets[-1].append(c)
        seq_to_sup[new_seq] = n
    return seq_to_sup


def get_place(smaller_seq: Sequence, bigger_seq: Sequence) -> tuple[int, int]:
    ln, j = len(smaller_seq), 0
    for idx, its in enumerate(bigger_seq.item_sets):
        idx2 = get_place_its(smaller_seq[j], its)
        if idx2 != -1:
            j += 1
        if j == ln:
            return idx, idx2
    return -1, -1


def get_place_its(smaller_its: ItemSet, bigger_its: ItemSet) -> int:
    ln, j = len(smaller_its), 0
    for idx, its in enumerate(bigger_its.items):
        if its == smaller_its[j]:
            j += 1
        if j == ln:
            return idx
    return -1
