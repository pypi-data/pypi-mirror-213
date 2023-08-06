from __future__ import annotations

from collections.abc import Iterable
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np

from . import feature as fea
from ..misc import iterable as itb


class Product:
    def __init__(
        self,
        key: Any,
        data: Dict[str, Any],
    ) -> None:
        self.key = key
        self.data = data

    def get_embedding(
        self,
        feature_set: fea.FeatureSet,
    ) -> np.ndarray:
        return feature_set.get_row_embedding(self.data)


class ProductList:
    def __init__(
        self,
        products: List[Product],
    ) -> None:
        self.products: Dict[Any, Product] = {}
        self.add_products(products)

    def __len__(self) -> int:
        return len(self.products)

    def __getitem__(self, key: Any) -> Product:
        return self.get_product(key)

    def __iter__(self) -> Iterable[Product]:
        return iter(self.products.values())

    def chunks(self, batch_size: int) -> Iterable[ProductList]:
        for chunk in itb.chunks(self.products.values(), batch_size):
            yield ProductList(products=chunk)

    def clear_products(
        self,
    ) -> None:
        self.products = {}

    def add_products(
        self,
        products: List[Product],
    ) -> None:
        self.products.update({product.key: product for product in products})

    def set_products(
        self,
        products: List[Product],
    ) -> None:
        self.clear_products()
        self.add_products(products)

    def get_products(
        self,
    ) -> List[Product]:
        return list(self.products.values())

    def add_product(
        self,
        product: Product,
    ) -> None:
        self.products[product.key] = product

    def get_product(
        self,
        key: Any,
    ) -> Product:
        return self.products[key]

    def get_embeddings(
        self,
        feature_set: fea.FeatureSet,
    ) -> List[np.ndarray]:
        return [p.get_embedding(feature_set) for p in self.get_products()]


class Triplet:
    def __init__(
        self,
        anchor: Product,
        positive: Product,
        negative: Product,
    ) -> None:
        self.anchor = anchor
        self.positive = positive
        self.negative = negative


class TripletList:
    def __init__(
        self,
        triplets: List[Triplet],
    ) -> None:
        self.triplets = triplets

    def __len__(self) -> int:
        return len(self.triplets)

    def __iter__(self) -> Iterable[Triplet]:
        return iter(self.triplets)

    def chunks(self, batch_size: int) -> Iterable[TripletList]:
        for chunk in itb.chunks(self.triplets, batch_size):
            yield TripletList(triplets=chunk)

    def anchors(
        self,
    ) -> ProductList:
        return ProductList(products=[triplet.anchor for triplet in self.triplets])

    def positives(
        self,
    ) -> ProductList:
        return ProductList(products=[triplet.positive for triplet in self.triplets])

    def negatives(
        self,
    ) -> ProductList:
        return ProductList(products=[triplet.negative for triplet in self.triplets])
