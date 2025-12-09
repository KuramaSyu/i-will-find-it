from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod
from datetime import datetime
from enum import Enum
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Any, Sequence

from torch import Tensor
from api import LoggingProvider


class Models(Enum):
    MINI_LM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"
    PARAPHRASE_MPNET_BASE_V2 = "sentence-transformers/paraphrase-mpnet-base-v2"
    DISTILBERT_BASE_NLI_STSB_ELECTRA = "sentence-transformers/distilbert-base-nli-stsb-mean-tokens"

class EmbeddingGeneratorABC(ABC):
    """Abstract base class for embedding generators."""


    @abstractmethod
    def generate(self, text: str) -> Tensor:
        pass

    @staticmethod
    def tensor_to_str_vec(tensor: Tensor) -> str:
        """
        Convert a tensor to a compact string representation of a vector.

        Args
        ----
        tensor : Tensor
            A tensor-like object that implements tolist() (e.g., torch.Tensor,
            numpy.ndarray). Intended for 1-D tensors.
        
        Returns
        -------
        str
            A string representing the tensor as a bracketed, comma-separated vector.

        Examples
        ---------
        - 1-D tensor `[1.0, 2.0, 3.0]` -> `"[1.0,2.0,3.0]"`
        - 2-D tensor `[[1, 2], [3, 4]]` -> `"[[1,2],[3,4]]"`
        """
        return f"[{','.join(str(x) for x in tensor.tolist())}]"

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the string name of the model."""
        ...


class EmbeddingGenerator(EmbeddingGeneratorABC):
    """Generates embeddings for given text using specified model."""
    def __init__(self, model_name: Models, logging_provider: LoggingProvider):
        self.model = SentenceTransformer(model_name.value)
        self.model_enum = model_name
        self.log = logging_provider(__name__, self)

    def generate(self, text: str) -> Tensor:
        start = datetime.now()
        embedding = self.model.encode(text)
        print(f"Embedding generation took: {datetime.now() - start}")
        return embedding

    @property
    def model_name(self) -> str:
        return self.model_enum.value