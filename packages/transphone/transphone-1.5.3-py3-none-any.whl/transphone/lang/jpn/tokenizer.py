from transphone.utils import import_with_auto_install
from transphone.lang.jpn.kana2phoneme import Kana2Phoneme
from transphone.g2p import read_g2p
from phonepiece.inventory import read_inventory
from transphone.lang.jpn import jaconv
from transphone.lang.base_tokenizer import BaseTokenizer
from transphone.lang.jpn.normalizer import normalize_neologd, parse_jpn_number, parse_jpn_alphabet


def read_jpn_tokenizer(lang_id, g2p_model='latest', device=None, use_lexicon=True):
    return JPNTokenizer(lang_id, g2p_model, device)

class JPNTokenizer(BaseTokenizer):

    def __init__(self, lang_id, g2p_model='latest', device=None):

        super().__init__(lang_id, g2p_model, device)

        # import mecab and its dict
        MeCab = import_with_auto_install('MeCab', 'mecab-python3')
        import_with_auto_install('unidic_lite', 'unidic-lite')

        self.tagger = MeCab.Tagger()
        self.kana2phoneme = Kana2Phoneme()

    def tokenize_words(self, text:str):
        text = normalize_neologd(text)

        raw_words = self.tagger.parse(text).split('\n')

        result = []

        # exclude the last EOS word
        for word in raw_words[:-2]:
            raw = word.split('\t')[0]
            result.append(raw)

        return result

    def tokenize(self, text, use_g2p=True, use_space=False, verbose=False):

        text = normalize_neologd(text)

        raw_words = self.tagger.parse(text).split('\n')

        result = []

        # exclude the last EOS word
        for word in raw_words[:-2]:

            kana = word.split('\t')[1]
            raw = word.split('\t')[0]

            if str.isdigit(raw):
                hankaku_num = jaconv.z2h(kana)
                kana = jaconv.hira2kata(parse_jpn_number(hankaku_num))

            # interestingly, isalpha also return true for kana
            if str.isalpha(raw) and str.isascii(raw):
                kana = parse_jpn_alphabet(raw)

            res = self.kana2phoneme.convert(kana)

            if res == ['*'] and self.kana2phoneme.validate(raw):
                res = self.kana2phoneme.convert(raw)

            if verbose:
                print(kana, res)

            if res != ['*']:
                result.extend(res)
            elif use_g2p:
                if raw in self.cache:
                    result.extend(self.cache[raw])
                else:
                    phonemes = self.g2p.inference(raw)
                    remapped_phonemes = self.inventory.remap(phonemes)
                    if verbose:
                        print(f"g2p {raw} ->  {remapped_phonemes}")
                    self.cache[raw] = remapped_phonemes
                    result.extend(remapped_phonemes)

            if use_space:
                result.append('<SPACE>')

        return result