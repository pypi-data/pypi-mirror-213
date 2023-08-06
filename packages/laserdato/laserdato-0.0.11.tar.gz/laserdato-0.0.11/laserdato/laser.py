from .embed import embed_sentences
import numpy as np
from pathlib import Path
from .get_model import load_or_download_file
import time


class Laser:
    def embed_sentences(
        self, sentences: list[str], target_devices: list[int] = None, lang: str = None
    ):
        if lang is not None:
            raise NotImplementedError("Language not implemented yet.")
        pt = load_or_download_file("laser2.pt")
        spm = load_or_download_file("laser2.spm").as_posix()
        embeddings = embed_sentences(
            sentences=sentences,
            encoder_path=str(pt),
            spm_model=str(spm),
            verbose=True,
            max_tokens=12000,
            buffer_size=10000,
            target_devices=target_devices,
        )
        # https://github.com/facebookresearch/LASER/tree/main/tasks/embed
        # dim = 1024
        # X.resize(X.shape[0] // dim, dim)

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
