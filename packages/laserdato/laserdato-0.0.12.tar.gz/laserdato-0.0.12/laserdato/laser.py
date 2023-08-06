from .embed import embed_sentences
import numpy as np
from pathlib import Path
from .get_model import load_or_download_file
import time
from .lib.constants import langs


class Laser:
    def embed_sentences(
        self, sentences: list[str], target_devices: list[int] = None, lang: str = None
    ):
        version = 0
        if lang is not None:
            if lang not in langs:
                raise ValueError(f"Language {lang} not supported")
            version = 1
            pt = load_or_download_file(f"laser3-{lang}.{version}.pt")
        else:
            pt = load_or_download_file("laser2.pt")
        spm = load_or_download_file("laser2.spm").as_posix()
        vocab = load_or_download_file("laser2.cvocab")
        embeddings = embed_sentences(
            sentences=sentences,
            encoder_path=str(pt),
            spm_model=str(spm),
            verbose=True,
            max_tokens=12000,
            buffer_size=10000,
            target_devices=target_devices,
        )
        return embeddings


if __name__ == "__main__":
    laser = Laser()
    # sentences = ["This is a sentence", "this is another sentences."] * 1000000
    sentences = ["This is a sentence", "this is another sentences."] * 10

    t = time.time()
    # print(sentences)
    # embeddings = laser.embed_sentences(sentences=sentences, target_devices=[0, 1])
    embeddings = laser.embed_sentences(sentences=sentences)
    # dim = 1024
    # embeddings.resize(embeddings.shape[0] // dim, dim)
    print(embeddings)
    print(embeddings.shape)
    print(type(embeddings))
    print(len(embeddings))
    print(time.time() - t)
