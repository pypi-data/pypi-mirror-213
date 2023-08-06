from .embed import embed_sentences
import numpy as np
from .get_model import load_or_download_file
from .lib.constants import laser3_langs, langs_with_specific_vocab


class Laser:
    def __init__(
        self, target_devices: list[int] = None, lang: str = None, cpu: bool = True
    ):
        """
        :param target_devices: list of GPU ids to use for embedding, if None, will use the first GPU available
        :param lang: only to be specified if using laser3, must be in laser3_langs. If None, will use laser2
        :param cpu: if True, will use CPU for embedding and ignore target_devices
        """
        self.lang = lang
        self.target_devices = target_devices
        self.cpu = cpu

    def embed_sentences(
        self, sentences: list[str], verbose: bool = False
    ) -> list[np.ndarray]:
        """
        :param sentences: list of sentences to embed
        :param verbose: if True, will print progress
        :return: list of embeddings
        """
        version = 0
        if self.lang is not None:
            if self.lang not in laser3_langs:
                raise ValueError(f"Language {self.lang} not supported")
            version = 1
            pt = load_or_download_file(f"laser3-{self.lang}.v{version}.pt")
            if self.lang in langs_with_specific_vocab:
                spm = load_or_download_file(
                    f"laser3-{self.lang}.v{version}.spm"
                ).as_posix()
                vocab = load_or_download_file(f"laser3-{self.lang}.v{version}.cvocab")
        else:
            pt = load_or_download_file("laser2.pt")
        spm = load_or_download_file("laser2.spm").as_posix()
        vocab = load_or_download_file("laser2.cvocab")
        embeddings = embed_sentences(
            sentences=sentences,
            encoder_path=str(pt),
            spm_model=str(spm),
            verbose=verbose,
            max_tokens=12000,
            buffer_size=10000,
            target_devices=self.target_devices,
            cpu=self.cpu,
        )
        return embeddings
