from sentencepiece import SentencePieceProcessor
from laserdato import Laser

sp = SentencePieceProcessor(
    model_file="/home/gauthier.roy/test_python/env_de_test/lib/python3.10/site-packages/laserdato/models/laser2.spm"
)

test = ["This is a sentence", "this is another sentences."]
laser = Laser()
embeddings = laser.embed_sentences(sentences=test)
print(embeddings)
# print(sp.EncodeAsPieces(tes))
# print(sp.encode_as_pieces("test"))
