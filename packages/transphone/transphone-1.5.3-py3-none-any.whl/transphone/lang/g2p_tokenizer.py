from phonepiece.lang import normalize_lang_id
from phonepiece.lexicon import read_lexicon
from transphone.lang.base_tokenizer import BaseTokenizer


def read_g2p_tokenizer(lang_id, g2p_model='latest', device=None):
    lang_id = normalize_lang_id(lang_id)
    return G2PTokenizer(lang_id, g2p_model, device)

class G2PTokenizer(BaseTokenizer):

    def __init__(self, lang_id, g2p_model='latest', device=None):
        super().__init__(lang_id, g2p_model, device)

        self.lexicon = read_lexicon(lang_id)



    def tokenize(self, text, use_g2p=True, use_space=False, verbose=False):

        norm_text = text.translate(str.maketrans('', '', self.punctuation)).lower()
        log = f"normalization: {text} -> {norm_text}"
        self.logger.info(log)

        if verbose:
            print(log)

        text = norm_text

        result = []

        for word in text.split():
            if word in self.cache:
                result.extend(self.cache[word])
            elif word in self.lexicon:
                phonemes = self.lexicon[word]
                result.extend(phonemes)
                self.cache[word] = phonemes
                log = f"lexicon {word} -> {phonemes}"
                self.logger.info(log)
                if verbose:
                    print(log)
            else:
                phonemes = self.g2p.inference_batch(word, self.lang_id, verbose=verbose)
                remapped_phonemes = self.inventory.remap(phonemes)

                log = f"g2p batch mode: {word} ->  {remapped_phonemes}"
                self.logger.info(log)
                if verbose:
                    print(log)
                self.add_cache(word, remapped_phonemes)
                result.extend(remapped_phonemes)
            if use_space:
                result.append('<SPACE>')

        return result
