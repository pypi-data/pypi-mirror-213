from __future__ import annotations

import os
import shelve as she
from collections.abc import Iterable
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataiku as di
import numpy as np
import pandas as pd
import tensorflow_hub as hu

from ..fsio import dss as lio
from ..img import dss as lim
from ..img import helpers as ih
from ..misc import common as co
from ..misc import http as hh
from ..misc import iterable as it


##########
# Config #
##########


class FEATURE_MODULE_CONFIG:
    VERBOSE: bool = False
    CACHE_DIR: str = "."


#########
# Enums #
#########


class FeatureKind(Enum):
    """An enumeration of the kinds of features."""

    Embedding = "embedding"
    Metadata = "metadata"
    Output = "output"
    Ignored = "ignored"


class CaseConversion(Enum):
    """An enumeration of the kinds of case conversion."""

    NoChange = "no-change"
    LowerCase = "lower-case"
    UpperCase = "upper-case"


#################
# Base Features #
#################


class BaseFeature:
    def __init__(
        self,
        feature_name: str,
        feature_type: str,
        feature_kind: FeatureKind = FeatureKind.Embedding,
        is_key: bool = False,
        input_size: Optional[Union[int, Tuple[int, int]]] = None,
        output_size: Optional[int] = None,
    ) -> None:
        self.feature_name = feature_name
        self.feature_type = feature_type
        self.feature_kind = feature_kind
        self.is_key = is_key
        self.input_size = input_size
        self.output_size = output_size

    ###################
    # Private methods #
    ###################

    def _printout_self_state(self):
        print('type: "{0}"'.format(type(self)))
        print('feature_name: "{0}"'.format(self.feature_name))
        print('feature_kind: "{0}"'.format(self.feature_kind))
        print('feature_type: "{0}"'.format(self.feature_type))
        print('is_key: "{0}"'.format(self.is_key))
        print('input_size: "{0}"'.format(self.input_size))
        print('output_size: "{0}"'.format(self.output_size))

    ##################
    # Public methods #
    ##################

    def process(self, data: Any) -> Any:
        if FEATURE_MODULE_CONFIG.VERBOSE:
            print("----------")
            print(
                'class: "{0}", function: "process", data: "{1}"'.format(
                    self.__class__.__name__, data
                )
            )
            print("----------")
            print("")

        return self.process_data(data=self.preprocess_data(data=data))

    #####################################
    # Methods to override in subclasses #
    #####################################

    def get_config(self):
        return {
            "class_name": self.__class__.__name__,
            "feature_name": self.feature_name,
            "feature_type": self.feature_type,
            "feature_kind": self.feature_kind.value,
            "is_key": self.is_key,
            "input_size": self.input_size,
            "output_size": self.output_size,
        }

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            feature_type=config["feature_type"],
            feature_kind=FeatureKind(config["feature_kind"]),
            is_key=config["is_key"],
            input_size=config["input_size"],
            output_size=config["output_size"],
        )

    def sanity_check_data(self, data: Union[List[Dict], pd.DataFrame]) -> None:
        self.sanity_check()

        columns = None

        if isinstance(data, pd.DataFrame):
            columns = data.columns.tolist()
        elif isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):
                columns = list(data[0].keys())

        if columns is None:
            raise Exception('Data type "{0}" not supported'.format(type(data)))

        if self.feature_name not in columns:
            raise Exception('Feature "{0}" not in dataset'.format(self.feature_name))

    def sanity_check(self) -> None:
        if self.feature_kind == FeatureKind.Embedding:
            if self.dimension() is None:
                raise Exception(
                    'Dimension is not set for feature "{0}"'.format(self.feature_name)
                )

    def preprocess_data(self, data: Any) -> Any:
        return data

    def process_data(self, data: Any) -> Any:
        return data

    def dimension(self) -> Optional[int]:
        return self.output_size


class BaseHubFeature(BaseFeature):
    models: Dict[str, Any] = {}

    def __init__(
        self,
        feature_name: str,
        feature_type: str,
        model_url: str,
        is_key: bool = False,
        input_size: Optional[Union[int, Tuple[int, int]]] = None,
        output_size: Optional[int] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type=feature_type,
            feature_kind=FeatureKind.Embedding,
            is_key=is_key,
            input_size=input_size,
            output_size=output_size,
        )

        self.model_url = model_url
        self.model = BaseHubFeature._register_model(self.model_url)

        self._embeddings_cache = None
        self._load_cache()

    ###################
    # Private methods #
    ###################

    def _printout_self_state(self):
        super()._printout_self_state()
        print('model_url: "{0}"'.format(self.model_url))

    def __exit__(self, *exc_info):
        self._save_cache()

    def _load_cache(self):
        cache_path = self._get_cache_path()

        self._embeddings_cache = she.open(filename=cache_path)

    def _get_cache_path(self):
        cache_path = FEATURE_MODULE_CONFIG.CACHE_DIR

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        return os.path.join(cache_path, "CACHE__{0}".format(self.feature_type))

    def _save_cache(self):
        if self._embeddings_cache is not None:
            self._embeddings_cache.close()

    def _flush_cache(self):
        self._save_cache()
        self._load_cache()

    def _empty_embedding(self) -> np.ndarray:
        return np.array([0] * self.dimension(), np.float32)

    def _get_cache_key(self, key: Any) -> Tuple[Any, Any]:
        cache_key = None
        cache_key_exists = False

        if isinstance(key, float) and np.isnan(key):
            cache_key = None
        elif isinstance(key, str) and key == "":
            cache_key = None
        else:
            cache_key = str(key)

        if self._embeddings_cache is not None:
            if cache_key is not None:
                cache_key_exists = cache_key in self._embeddings_cache

        return cache_key, cache_key_exists

    ##################
    # Public methods #
    ##################

    def process(self, data: Any) -> Any:
        if FEATURE_MODULE_CONFIG.VERBOSE:
            print("----------")
            print(
                'class: "{0}", function: "process", data: "{1}"'.format(
                    self.__class__.__name__, data
                )
            )
            print("----------")
            print("")

        output = None

        try:
            cache_key, cache_key_exists = self._get_cache_key(key=data)

            if cache_key_exists:
                output = self._embeddings_cache[cache_key]
            else:
                output = super().process(data=data)

                if cache_key is not None:
                    self._embeddings_cache[cache_key] = output
        except Exception as e:
            if FEATURE_MODULE_CONFIG.VERBOSE:
                self._printout_self_state()
                print('data: "{0}" (type: "{1}")'.format(data, type(data)))
                print('output: "{0}"'.format(output))
                print('Exception: "{0}" (type: "{1}")'.format(e, type(e)))

        return output

    ####################
    # Static / Private #
    ####################

    @staticmethod
    def _register_model(model_url):
        if model_url not in BaseHubFeature.models:
            BaseHubFeature.models[model_url] = hu.load(model_url)

        return BaseHubFeature.models[model_url]

    #############
    # Overrides #
    #############

    def get_config(self):
        config = super().get_config()
        config.update({"model_url": self.model_url})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            feature_type=config["feature_type"],
            model_url=config["model_url"],
            is_key=config["is_key"],
            input_size=config["input_size"],
            output_size=config["output_size"],
        )

    def sanity_check(self) -> None:
        super().sanity_check()

        if self.model is None:
            raise Exception('Model not set for feature "{0}"'.format(self.feature_name))

        if self.input_size is None:
            raise Exception(
                'Input size not set for feature "{0}"'.format(self.feature_name)
            )

    def process_data(self, data: Any) -> Any:
        if FEATURE_MODULE_CONFIG.VERBOSE:
            print("----------")
            print(
                'class: "{0}", function: "process", data: "{1}"'.format(
                    self.__class__.__name__, data
                )
            )
            print("----------")
            print("")

        if data is None:
            return self._empty_embedding()
        else:
            return self.model(data)[0]

    def preprocess_data(self, data: Any) -> Any:
        raise NotImplementedError()


class BaseTextFeature(BaseHubFeature):
    def __init__(
        self,
        feature_name: str,
        feature_type: str,
        model_url: str,
        is_key: bool = False,
        input_size: Optional[Union[int, Tuple[int, int]]] = None,
        output_size: Optional[int] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type=feature_type,
            model_url=model_url,
            is_key=is_key,
            input_size=input_size,
            output_size=output_size,
        )

    #############
    # Overrides #
    #############

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            feature_type=config["feature_type"],
            model_url=config["model_url"],
            is_key=config["is_key"],
            input_size=config["input_size"],
            output_size=config["output_size"],
        )

    def preprocess_data(self, data: Any) -> Any:
        input = data
        if self.input_size is not None and len(data) > self.input_size:
            input = data[: self.input_size]

        return np.array([input])


class BaseImageFeature(BaseHubFeature):
    def __init__(
        self,
        feature_name: str,
        feature_type: str,
        model_url: str,
        is_key: bool = False,
        folder: Optional[Union[str, di.Folder]] = None,
        input_size: Optional[Union[int, Tuple[int, int]]] = None,
        output_size: Optional[int] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type=feature_type,
            model_url=model_url,
            is_key=is_key,
            input_size=input_size,
            output_size=output_size,
        )

        self._folder = None

        if folder is not None:
            self._folder = lio.get_folder(folder)

        self.folder = None

        if isinstance(folder, str):
            self.folder = folder
        elif isinstance(folder, di.Folder):
            self.folder = folder.path

    #############
    # Overrides #
    #############

    def get_config(self):
        config = super().get_config()
        config.update({"folder": self.folder})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            feature_type=config["feature_type"],
            model_url=config["model_url"],
            is_key=config["is_key"],
            folder=config["folder"],
            input_size=config["input_size"],
            output_size=config["output_size"],
        )

    def preprocess_data(self, data: Any) -> Any:
        if FEATURE_MODULE_CONFIG.VERBOSE:
            print("----------")
            print(
                'class: "{0}", function: "process", data: "{1}"'.format(
                    self.__class__.__name__, data
                )
            )
            print("----------")
            print("")

        if data is None:
            return None
        elif isinstance(data, float) and np.isnan(data):
            return None
        elif isinstance(data, str) and data == "":
            return None

        string_kind = co.get_string_kind(data)
        pil_image = None

        try:
            if string_kind == co.StringKind.Url:
                pil_image = hh.download_image(url=data)
            elif string_kind == co.StringKind.Path:
                if self._folder is None:
                    pil_image = ih.open_image(file_path=data)
                else:
                    pil_image = lim.open_valid_image(
                        folder=self._folder, file_path=data
                    )
        except Exception:
            pil_image = None

        if pil_image is not None:
            if pil_image.size != self.input_size:
                pil_image = ih.extract_square_portion(
                    image=pil_image,
                    horizontal_position="center",
                    vertical_position="middle",
                    output_size=self.input_size,
                )

            return ih.image_to_batch_array(pil_image=pil_image, rescaled=True)
        else:
            return None


class BaseMetadataFeature(BaseFeature):
    def __init__(self, feature_name: str, feature_type: str, is_key: bool = False):
        super().__init__(
            feature_name=feature_name,
            feature_type=feature_type,
            feature_kind=FeatureKind.Metadata,
            is_key=is_key,
            input_size=None,
            output_size=None,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            feature_type=config["feature_type"],
            is_key=config["is_key"],
        )


class BaseOutputFeature(BaseFeature):
    def __init__(self, feature_name: str, feature_type: str, is_key: bool = False):
        super().__init__(
            feature_name=feature_name,
            feature_type=feature_type,
            feature_kind=FeatureKind.Output,
            is_key=is_key,
            input_size=None,
            output_size=None,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            feature_type=config["feature_type"],
            is_key=config["is_key"],
        )


###################
# Usable Features #
###################


class CategoryFeature(BaseFeature):
    def __init__(
        self,
        feature_name: str,
        trim: bool = True,
        case_conversion: CaseConversion = CaseConversion.NoChange,
        is_key: bool = False,
        output_size: Optional[int] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type="category",
            feature_kind=FeatureKind.Embedding,
            is_key=is_key,
            input_size=None,
            output_size=output_size,
        )

        self.trim = trim
        self.case_conversion = case_conversion
        self.reset_categories()

    ###################
    # Private methods #
    ###################

    def _apply_conversion(
        self,
        value: str,
        trim: bool = True,
        case_conversion: CaseConversion = CaseConversion.NoChange,
    ) -> str:
        if value is not None:
            if trim:
                value = value.strip()

            if case_conversion == CaseConversion.LowerCase:
                value = value.lower()
            elif case_conversion == CaseConversion.UpperCase:
                value = value.upper()

        return value

    def _get_output_size(self) -> int:
        if self.output_size is None:
            return len(self.categories)
        else:
            return self.output_size

    def _empty_embedding(self) -> np.ndarray:
        return np.array([0] * self._get_output_size(), dtype=np.float32)

    #############
    # Overrides #
    #############

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "trim": self.trim,
                "case_conversion": self.case_conversion,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            trim=config["trim"],
            case_conversion=config["case_conversion"],
            is_key=config["is_key"],
            output_size=config["output_size"],
        )

    def process_data(self, data: Any) -> Any:
        vect = self._empty_embedding()

        if data is not None:
            if data in self.categories:
                vect[self.categories_revert[data]] = 1

        return vect

    def dimension(self) -> Optional[int]:
        return self._get_output_size()

    #############
    # Additions #
    #############

    def reset_categories(self) -> None:
        self.categories: List[str] = []
        self.categories_revert: Dict[str, int] = {}

    def load_categories(self, categories: List[str]) -> None:
        if categories is not None:
            for category in categories:
                self.register_category(category)

    def register_category(self, category: str):
        category = self._apply_conversion(
            value=category, trim=self.trim, case_conversion=self.case_conversion
        )

        if category not in self.categories:
            self.assert_capacity()
            self.categories.append(category)
            self.categories_revert[category] = self.categories.index(category)

    def assert_capacity(self):
        if self.output_size is not None and len(self.categories) >= self.output_size:
            raise Exception("Categories capacity full")


class CsvCategoryFeature(CategoryFeature):
    def __init__(
        self,
        feature_name: str,
        separator: str = ",",
        trim: bool = True,
        case_conversion: CaseConversion = CaseConversion.NoChange,
        is_key: bool = False,
        output_size: int = 128,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            trim=trim,
            case_conversion=case_conversion,
            is_key=is_key,
            output_size=output_size,
        )

        self.feature_type = "csv_categoy"
        self.separator = separator

    ###################
    # Private methods #
    ###################

    def _concatenate_csv_strings(
        self,
        csv_strings: List[str],
        separator: str = ",",
        trim: bool = True,
        case_conversion: CaseConversion = CaseConversion.NoChange,
    ) -> List[str]:
        result = []
        for csv_string in csv_strings:
            values = csv_string.split(separator)

            # Trim and change case for each value as specified
            for i, value in enumerate(values):
                values[i] = self._apply_conversion(value, trim, case_conversion)

            result.extend(values)
        return result

    #############
    # Overrides #
    #############

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "feature_type": self.feature_type,
                "separator": self.separator,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            separator=config["separator"],
            trim=config["trim"],
            case_conversion=config["case_conversion"],
            is_key=config["is_key"],
            output_size=config["output_size"],
        )

    def load_categories(self, categories):
        if categories is not None:
            for category in self._concatenate_csv_strings(
                csv_strings=categories,
                separator=self.separator,
                trim=self.trim,
                case_conversion=self.case_conversion,
            ):
                self.register_category(category)

    def register_category(self, category: str):
        for c in self._concatenate_csv_strings(
            csv_strings=[category],
            separator=self.separator,
            trim=self.trim,
            case_conversion=self.case_conversion,
        ):
            if c not in self.categories:
                self.assert_capacity()
                self.categories.append(c)
                self.categories_revert[c] = self.categories.index(c)


class BooleanFeature(BaseFeature):
    def __init__(
        self, feature_name: str, default_value: float = 0.5, is_key: bool = False
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type="boolean",
            feature_kind=FeatureKind.Embedding,
            is_key=is_key,
            input_size=None,
            output_size=1,
        )

        self.default_value = default_value

    #############
    # Overrides #
    #############

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "default_value": self.default_value,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            default_value=config["default_value"],
            is_key=config["is_key"],
        )

    def preprocess_data(self, data: Any) -> Any:
        value = self.default_value

        if data or data == 1:
            value = 1
        elif not data or data == 0:
            value = 0
        return value

    def process_data(self, data: Any) -> Any:
        return np.array(object=[data], dtype=np.float32)


class NumericFeature(BaseFeature):
    def __init__(
        self,
        feature_name: str,
        default_value: float = 0.0,
        range: Optional[Tuple[float, float]] = None,
        is_key: bool = False,
    ):
        super().__init__(
            feature_name=feature_name,
            feature_type="numeric",
            feature_kind=FeatureKind.Embedding,
            is_key=is_key,
            input_size=None,
            output_size=1,
        )

        self.default_value = default_value
        self.range = range

    ###################
    # Private methods #
    ###################

    def _empty_embedding(self) -> np.ndarray:
        return np.array([self.default_value], dtype=np.float32)

    #############
    # Overrides #
    #############

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "default_value": self.default_value,
                "range": self.range,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            default_value=config["default_value"],
            range=config["range"],
            is_key=config["is_key"],
        )

    def preprocess_data(self, data: Any) -> Any:
        if data is not None:
            data = float(data)

            if self.range is not None:
                data = (data - self.range[0]) / (self.range[1] - self.range[0])
        else:
            data = self.default_value

        return data

    def process_data(self, data: Any) -> Any:
        return np.array([data], dtype=np.float32)


class ShortTextFeature(BaseTextFeature):
    def __init__(
        self,
        feature_name: str,
        is_key: bool = False,
        input_size: Optional[Union[int, Tuple[int, int]]] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type="tfhub_dev_google_nnlm_en_dim128_2",
            model_url="https://tfhub.dev/google/nnlm-en-dim128/2",
            is_key=is_key,
            input_size=input_size,
            output_size=128,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            is_key=config["is_key"],
            input_size=config["input_size"],
        )


class LongTextFeature(BaseTextFeature):
    def __init__(
        self,
        feature_name: str,
        is_key: bool = False,
        input_size: Optional[Union[int, Tuple[int, int]]] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type="tfhub_dev_google_universal_sentence_encoder_large_5",
            model_url="https://tfhub.dev/google/universal-sentence-encoder-large/5",
            is_key=is_key,
            input_size=input_size,
            output_size=512,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            is_key=config["is_key"],
            input_size=config["input_size"],
        )


class StandardImageFeature(BaseImageFeature):
    def __init__(
        self,
        feature_name: str,
        is_key: bool = False,
        folder: Optional[Union[str, di.Folder]] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type="tfhub_dev_google_imagenet_inception_v3_feature_vector_5",
            model_url="https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5",
            is_key=is_key,
            folder=folder,
            input_size=(500, 500),
            output_size=2048,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            is_key=config["is_key"],
            folder=config["folder"],
        )


class ClothingImageFeature(BaseImageFeature):
    def __init__(
        self,
        feature_name: str,
        is_key: bool = False,
        folder: Optional[Union[str, di.Folder]] = None,
    ) -> None:
        super().__init__(
            feature_name=feature_name,
            feature_type="tfhub_dev_google_experts_bit_r50x1_in21k_clothing_1",
            model_url="https://tfhub.dev/google/experts/bit/r50x1/in21k/clothing/1",
            is_key=is_key,
            folder=folder,
            input_size=(500, 500),
            output_size=2048,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            feature_name=config["feature_name"],
            is_key=config["is_key"],
            folder=config["folder"],
        )


#####################
# Multiple Features #
#####################


class FeatureSet:
    def __init__(
        self,
        features: List[BaseFeature],
        token_size: int = 128,
    ) -> None:
        self.features = features
        self.token_size = token_size

    ###################
    # Private methods #
    ###################

    def _get_row_processed_data_of_kind(
        self, row_data: Any, kind: FeatureKind
    ) -> List[Any]:
        if self.features is None:
            raise Exception("Features not set")

        return [
            f.process(data=row_data[f.feature_name])
            for f in self.features
            if f.feature_kind == kind
        ]

    def _get_row_processed_data_of_kind_as_dict(
        self, row_data: Any, kind: FeatureKind
    ) -> Dict[str, Any]:
        if self.features is None:
            raise Exception("Features not set")

        return {
            f.feature_name: f.process(data=row_data[f.feature_name])
            for f in self.features
            if f.feature_kind == kind
        }

    ####################
    # Static / Private #
    ####################

    @staticmethod
    def _pad_and_stack(
        embeddings: List[np.ndarray], token_size: Optional[int]
    ) -> np.ndarray:
        # If we don't have a token size, we can just concatenate
        if token_size is None:
            return np.concatenate(embeddings, axis=0)
        else:
            # Otherwise, we need to pad and then truncate the embeddings
            truncated_embeddings = []

            for embedding in embeddings:
                length = embedding.shape[0]
                remainder = length % token_size
                if remainder != 0:
                    # Pad the embedding to the nearest multiple of token size
                    padding_size = token_size - remainder
                    padded_embedding = np.pad(
                        embedding, (0, padding_size), mode="constant"
                    )
                else:
                    padded_embedding = embedding

                # Reshape the embedding into a matrix with n rows of size token_size
                num_pieces = padded_embedding.shape[0] // token_size
                reshaped_embedding = padded_embedding[
                    : num_pieces * token_size
                ].reshape(-1, token_size)
                truncated_embeddings.append(reshaped_embedding)

            # Stack the embeddings into a single matrix
            return np.concatenate(truncated_embeddings, axis=0)

    ##################
    # Public methods #
    ##################

    def set_features(self, features: List[BaseFeature]) -> None:
        self.features = features

    def sanity_check(self) -> None:
        if self.features is None:
            raise Exception("Features not set")

        num_keys = len([f for f in self.features if f.is_key])

        if num_keys == 0:
            raise Exception("No key features found")

        if num_keys > 1:
            raise Exception(
                "Too many key features found. There should be only 1 key feature."
            )

    def sanity_check_data(self, data: Union[List[Dict], pd.DataFrame]) -> None:
        """Sanity check the raw data being fed into the model

        Args:
            data (List[Dict] or pd.DataFrame): The raw input data

        Raises:
            Exception: If the data is not set
            Exception: If a feature is missing from the data
        """
        # Self data independent sanity check
        self.sanity_check()

        # Check whether the data is set
        if data is None:
            raise Exception("Data not set")

        for feature in self.features:
            # Check whether the data is valid
            feature.sanity_check_data(data)

    def get_row_embedding_dimension(self) -> int:
        return sum([f.output_size for f in self.features if f.feature_kind == FeatureKind.Embedding])  # type: ignore

    def get_row_embedding(self, row_data: Any) -> np.ndarray:
        return FeatureSet._pad_and_stack(
            self._get_row_processed_data_of_kind(
                row_data=row_data, kind=FeatureKind.Embedding
            ),
            self.token_size,
        )

    def get_row_metadata(self, row_data: Any) -> Dict[str, Any]:
        return self._get_row_processed_data_of_kind_as_dict(
            row_data=row_data, kind=FeatureKind.Metadata
        )

    def get_row_output(self, row_data: Any) -> Dict[str, Any]:
        return self._get_row_processed_data_of_kind_as_dict(
            row_data=row_data, kind=FeatureKind.Output
        )

    def get_row_key(self, row_data: Any) -> Any:
        """Returns the key for the given row data."""
        return [row_data[f.feature_name] for f in self.features if f.is_key][0]

    def iterate_embeddings_from_data(
        self, data: Union[List[Dict], pd.DataFrame], return_keys: bool
    ) -> Iterable[Union[Tuple[Any, np.ndarray], np.ndarray]]:
        """Loads the features from the given dataframe."""
        # Sanity check.
        self.sanity_check_data(data)

        data_iter = None

        if isinstance(data, pd.DataFrame):
            data_iter = it.iterate_dataframe(data, return_index=False)
        elif isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):
                data_iter = data

        if data_iter is None:
            raise Exception('Data type "{0}" not supported'.format(type(data)))

        # Iterate over the rows of the dataframe, returning the column values
        # as a dictionary.
        for product in data_iter:
            # Extract the key from the dictionary.
            product_key = self.get_row_key(product)

            # Convert the dictionary into a vector embedding.
            product_embedding = self.get_row_embedding(product)

            # Return the key and the embedding.
            if return_keys:
                yield product_key, product_embedding
            else:
                yield product_embedding

    #################
    # Configuration #
    #################

    def get_config(self):
        return {
            "token_size": self.token_size,
            "features": [f.get_config() for f in self.features],
        }

    @classmethod
    def from_config(cls, config):
        token_size = config["token_size"]
        features = []

        for feature_config in config["features"]:
            feature_class = feature_config["feature_class"]
            feature = globals()[feature_class].from_config(feature_config)
            features.append(feature)

        return cls(token_size=token_size, features=features)
