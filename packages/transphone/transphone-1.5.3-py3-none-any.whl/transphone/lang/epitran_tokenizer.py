"""Basic Epitran class for G2P in most languages."""
import logging
import os.path
import sys
import csv
import unicodedata
from collections import defaultdict
from typing import DefaultDict, Callable  # pylint: disable=unused-import
from phonepiece.epitran import read_epitran_g2p
from phonepiece.lexicon import read_lexicon
from phonepiece.inventory import read_inventory
import re
from transphone.lang.base_tokenizer import BaseTokenizer
from epitran.ppprocessor import PrePostProcessor
from phonepiece.ipa import read_ipa
import epitran

logger = logging.getLogger('epitran')

customized_epitran_dict = {
    'spa': 'spa-Latn',
    'deu': 'deu-Latn',
    'ita': 'ita-Latn',
    'rus': 'rus-Cyrl',
    'fra': 'fra-Latn',
}

raw_epitran_dict = {
     'tur': 'tur-Latn',
     'vie': 'vie-Latn',
     'aar': 'aar-Latn',
     'got': 'got-Latn',
     'lsm': 'lsm-Latn',
     'swa': 'swa-Latn',
     'aii': 'aii-Syrc',
     'hak': 'hak-Latn',
     'ltc': 'ltc-Latn-bax',
     'swe': 'swe-Latn',
     'amh': 'amh-Ethi',
     'hat': 'hat-Latn-bab',
     'tam': 'tam-Taml',
     'hau': 'hau-Latn',
     'mal': 'mal-Mlym',
     'hin': 'hin-Deva',
     'mar': 'mar-Deva',
     'tel': 'tel-Telu',
     'ara': 'ara-Arab',
     'hmn': 'hmn-Latn',
     'mlt': 'mlt-Latn',
     'tgk': 'tgk-Cyrl',
     'ava': 'ava-Cyrl',
     'hrv': 'hrv-Latn',
     'mon': 'mon-Cyrl-bab',
     'tgl': 'tgl-Latn',
     'aze': 'aze-Latn',
     'hsn': 'hsn-Latn',
     'mri': 'mri-Latn',
     'hun': 'hun-Latn',
     'msa': 'msa-Latn',
     'tha': 'tha-Thai',
     'ilo': 'ilo-Latn',
     'mya': 'mya-Mymr',
     'tir': 'tir-Ethi',
     'ind': 'ind-Latn',
     'nan': 'nan-Latn',
     'ita': 'ita-Latn',
     'bxk': 'bxk-Latn',
     'jam': 'jam-Latn',
     'nld': 'nld-Latn',
     'tpi': 'tpi-Latn',
     'cat': 'cat-Latn',
     'jav': 'jav-Latn',
     'nya': 'nya-Latn',
     'tuk': 'tuk-Latn',
     'ceb': 'ceb-Latn',
     'jpn': 'jpn-Ktkn-red',
     'ood': 'ood-Latn-sax',
     'ces': 'ces-Latn',
     'cjy': 'cjy-Latn',
     'ori': 'ori-Orya',
     'ckb': 'ckb-Arab',
     'orm': 'orm-Latn',
     'cmn': 'cmn-Latn',
     'kat': 'kat-Geor',
     'pan': 'pan-Guru',
     'uew': 'uew',
     'kaz': 'kaz-Latn',
     'pii': 'pii-latn_Wiktionary',
     'uig': 'uig-Arab',
     'csb': 'csb-Latn',
     'ukr': 'ukr-Cyrl',
     'deu': 'deu-Latn',
     'pol': 'pol-Latn',
     'urd': 'urd-Arab',
     'kbd': 'kbd-Cyrl',
     'por': 'por-Latn',
     'uzb': 'uzb-Latn',
     'khm': 'khm-Khmr',
     'ron': 'ron-Latn',
     'fas': 'fas-Arab',
     'kin': 'kin-Latn',
     'run': 'run-Latn',
     'kir': 'kir-Latn',
     'rus': 'rus-Cyrl',
     'wuu': 'wuu-Latn',
     'sag': 'sag-Latn',
     'xho': 'xho-Latn',
     'sin': 'sin-Sinh',
     'yor': 'yor-Latn',
     'kmr': 'kmr-Latn',
     'sna': 'sna-Latn',
     'yue': 'yue-Latn',
     'som': 'som-Latn',
     'zha': 'zha-Latn',
     'ful': 'ful-Latn',
     'lao': 'lao-Laoo-prereform',
     'spa': 'spa-Latn-eu',
     'zul': 'zul-Latn',
     'gan': 'gan-Latn',
     'sqi': 'sqi-Latn',
     'lij': 'lij-Latn'
}


def read_epitran_tokenizer(lang_id, g2p_model=None, device=None, use_lexicon=True):
    if lang_id in customized_epitran_dict:
        return read_customized_epitran_tokenizer(customized_epitran_dict[lang_id], use_lexicon)
    elif lang_id in raw_epitran_dict:
        return read_raw_epitran_tokenizer(raw_epitran_dict[lang_id], use_lexicon)
    else:
        raise ValueError('Unknown epitran id: {}'.format(lang_id_or_epi_id))


def read_raw_epitran_tokenizer(lang_id_or_epi_id, use_lexicon=True):

    if '-' in lang_id_or_epi_id:
        lang_id, writing_system = lang_id_or_epi_id.split('-', 1)
    else:
        lang_id = lang_id_or_epi_id
        writing_system = 'Latn'

    if use_lexicon:
        lexicon = read_lexicon(lang_id)
    else:
        lexicon = {}

    return RawEpitranTokenizer(lang_id, writing_system, lexicon)


def read_customized_epitran_tokenizer(lang_id_or_epi_id, use_lexicon=True):

    if '-' in lang_id_or_epi_id:
        lang_id, writing_system = lang_id_or_epi_id.split('-', 1)
    else:
        lang_id = lang_id_or_epi_id
        writing_system = 'Latn'

    if use_lexicon:
        lexicon = read_lexicon(lang_id)
    else:
        lexicon = {}

    return CustomizedEpitranTokenizer(lang_id, writing_system, lexicon)


class CustomizedEpitranTokenizer(BaseTokenizer):

    def __init__(self, lang_id, writing_system=None, lexicon=None):
        super().__init__(lang_id, None)

        #self.lexicon = read_lexicon(lang_id)

        """Constructor"""
        self.lang_id = lang_id
        self.writing_system = writing_system

        if writing_system:
            lang_id = lang_id + '-' + writing_system

        if not lexicon:
            lexicon = {}

        self.lexicon = lexicon

        self.g2p = read_epitran_g2p(lang_id)
        self.inv = read_inventory(self.lang_id)
        self.ipa = read_ipa()

        self.regexp = self._construct_regex(self.g2p.keys())
        self.nils = defaultdict(int)

        self.cache = defaultdict(list)

        self.preprocessor = PrePostProcessor(lang_id, 'pre', False)
        #self.postprocessor = PrePostProcessor(lang_id, 'post', False)

    def _construct_regex(self, g2p_keys):
        """Build a regular expression that will greadily match segments from
           the mapping table.
        """
        graphemes = sorted(g2p_keys, key=len, reverse=True)
        return re.compile(f"({r'|'.join(graphemes)})", re.I)

    def match_word(self, text, verbose=False):
        ipa_lst = []
        while text:
            logger.debug('text=', repr(list(text)))
            if verbose:
                print('text=', repr(list(text)))

            m = self.regexp.match(text)
            if m:
                source = m.group(0)
                try:
                    targets = self.g2p[source]
                    if verbose:
                        print(source, ' -> ', targets)
                except KeyError:
                    logger.debug("source = '%s''", source)
                    logger.debug("self.g2p[source] = %s'", self.g2p[source])
                    targets = []
                except IndexError:
                    logger.debug("self.g2p[source]= %s", self.g2p[source])
                    targets = []

                ipa_lst.extend(targets)
                text = text[len(source):]
            else:
                self.nils[text[0]] += 2
                text = text[1:]
        ipa_lst = self.inv.remap(ipa_lst)
        return ipa_lst


    def tokenize(self, text: str, verbose: bool=False):
        text = text.lower()

        ipa_lst = []

        for word in text.split():

            if word in self.cache:
                ipa_lst.extend(self.cache[word])

            elif word in self.lexicon:
                phonemes = self.lexicon[word]
                ipa_lst.extend(phonemes)
                self.cache[word] = phonemes
                log = f"lexicon {word} -> {phonemes}"
                self.logger.info(log)
                if verbose:
                    print(log)
            else:
                norm_word = unicodedata.normalize('NFC', word)

                norm_word = self.preprocessor.process(norm_word)

                word_ipa_lst = self.match_word(norm_word, verbose)

                log = f"rule raw: {word} -> norm: {norm_word} -> {word_ipa_lst}"
                self.logger.info(log)
                if verbose:
                    print(log)

                #word_ipa_lst = self.ipa.tokenize(self.postprocessor.process(''.join(word_ipa_lst)))

                self.cache[word] = word_ipa_lst
                ipa_lst.extend(self.cache[word])

        return ipa_lst


class RawEpitranTokenizer(BaseTokenizer):

    def __init__(self, lang_id, writing_system='Latin', lexicon=None):
        super().__init__(lang_id, None)

        #self.lexicon = read_lexicon(lang_id)

        """Constructor"""
        self.lang_id = lang_id
        self.writing_system = writing_system

        if writing_system:
            lang_id = lang_id + '-' + writing_system

        if not lexicon:
            lexicon = {}

        self.lexicon = lexicon

        self.g2p = epitran.Epitran(lang_id)
        self.inv = read_inventory(self.lang_id)
        self.ipa = read_ipa()

        self.cache = defaultdict(list)


    def tokenize(self, text: str, verbose: bool=False):
        text = text.lower()

        ipa_lst = []

        for word in text.split():

            if word in self.cache:
                ipa_lst.extend(self.cache[word])

            elif word in self.lexicon:
                phonemes = self.lexicon[word]
                ipa_lst.extend(phonemes)
                self.cache[word] = phonemes
                log = f"lexicon {word} -> {phonemes}"
                self.logger.info(log)
                if verbose:
                    print(log)
            else:

                word_ipa_lst = self.g2p.trans_list(word)
                word_ipa_lst = self.inv.remap(word_ipa_lst, broad=True)

                log = f"rule raw: {word} -> remap {word_ipa_lst}"
                self.logger.info(log)
                if verbose:
                    print(log)

                #word_ipa_lst = self.ipa.tokenize(self.postprocessor.process(''.join(word_ipa_lst)))

                self.cache[word] = word_ipa_lst
                ipa_lst.extend(self.cache[word])

        return ipa_lst