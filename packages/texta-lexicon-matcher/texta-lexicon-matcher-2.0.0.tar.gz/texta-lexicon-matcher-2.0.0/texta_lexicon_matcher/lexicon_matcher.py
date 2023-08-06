# -*- coding: utf-8 -*-
import regex as re
from typing import List, Dict, Tuple, Union


SUPPORTED_MATCH_TYPES = (
    "prefix",
    "exact",
    "subword"
)

SUPPORTED_OPERATORS = (
    "or",
    "and"
)

class LexiconMatcher:
    """ Match words/phrases in a lexion.
    """
    def __init__(self, lexicon: Union[str, List[str]],
                       operator: str = "or",
                       match_type: str = "prefix",
                       required_words: float = 1.0,
                       phrase_slop: int = 0,
                       counter_slop: int = 0,
                       return_fuzzy_match: bool = True,
                       counter_matches_preceeding: bool = True,
                       counter_matches_succeeding: bool = True,
                       n_allowed_edits = 0,
                       ignore_case = True,
                       ignore_punctuation = True,
                       counter_lexicon: Union[str, List[str]] = []):
        """
        Parameters:
            lexicon - lexicon containing words/phrases/regexes to match (as list or file_path)
            operator - logic operator used between the lexicon entries ("or","and")
            match_type - how to match lexicon entries ("prefix","fuzzy","exact")
            required_words - the proportion of words required to be in the text to obtain the tag (only for operator="and")
            phrase_slop - how many words are allowed between lexicon phrase entities
            counter_slop - how many words are allowed between nullifying lex entries and main lex entries
            return_fuzzy_match - if match_type == prefix or fuzzy, return whole word matched instead of the original lex word
            counter_matches_proceeding - TODO
            counter_matches_succeeding - TODO
            n_allowed_edits - how many edits (insertions/substitutions/deletions) in total are allowed while matching
            ignore_case - whether to use case sensitive or insensitive matching
            counter_lexicon - lexicon containing words/phrases/regexes which nullify main lex words (as list or file_path)

        :type lexicon: list or string (containing lex file name)
        :type operator: string
        :type match_type: string
        :type required_words: float (in range [0,1])
        :type phrase_slop: int
        :type counter_slop: int
        :type counter_lexicon: list or string (containing lex file name)
        """
        self._insertions_weight = 1
        self._deletions_weight = 1
        self._substitutions_weight = 1

        self._match_type = match_type
        self._operator = operator
        self._phrase_slop = phrase_slop
        self._required_words = required_words
        self._return_fuzzy_match = return_fuzzy_match
        self._counter_matches_preceeding = counter_matches_preceeding
        self._counter_matches_succeeding = counter_matches_succeeding
        self._n_allowed_edits = n_allowed_edits
        self._ignore_case = ignore_case
        self._ignore_punctuation = ignore_punctuation
        self._punctuation_to_ignore = "[^!.?;: ]"
        self._counter_slop = counter_slop
        self._punctuation = [".", "!", "?"]
        self._counter_ignore_pattern = "[.!?]"

        self._edit_pattern = self._get_edit_pattern()
        self._counter_lexicon = self._parse_lex(counter_lexicon)
        self._lexicon = self._parse_lex(lexicon)
        self._patterns = self._generate_patterns(self._lexicon, operator, match_type)
        self._counter_patterns = self._generate_patterns(self._counter_lexicon, operator="or", match_type="exact")


    def _parse_lex(self, lexicon: Union[str, List[str]]) -> List[str]:
        if isinstance(lexicon, list):
            lex = lexicon
        elif isinstance(lexicon, str):
            lex = self._load_lex(lexicon)
        else:
            lex = []
        return lex

    def _load_lex(self, lexicon: str) -> List[str]:
        words = []
        with open(lexicon) as f:
            content = f.read().strip()
            words = content.split("\n")
        return words

    def _get_prefix(self, match_type: str) -> str:
        if match_type == "subword":
            if self._return_fuzzy_match:
                prefix =  r"(?<=(^|\W))(?:\w*("
            else:
                prefix =  r"(?<=(^|\W)\w*)(?:("
        else:
            prefix = r"(\s|^)(?:("
        return prefix

    def _get_suffix(self, match_type: str) -> str:
        if match_type == "exact":
            suffix = r"))(?=((\W*)\s|$))"
        else:
            if self._return_fuzzy_match:
                suffix =  r")\w*)(?=(?:\W|$))"
            else:
                suffix = r"))"
        return suffix

    def _get_edit_pattern(self) -> str:
        i_w = self._insertions_weight
        d_w = self._deletions_weight
        s_w = self._substitutions_weight

        edit_pattern = rf"{{{i_w}i+{d_w}d+{s_w}s<={self._n_allowed_edits}}}"
        return edit_pattern

    def _get_slop_pattern(self) -> str:
        # \S vs \w?
        if self._ignore_punctuation:
            slop_pattern = rf"\s*(\S+\s+){{,{self._phrase_slop}}}"
        else:
            slop_pattern = rf"\s*({self._punctuation_to_ignore}+\s+){{,{self._phrase_slop}}}"
        return slop_pattern

    def _add_slops(self, lex_words: List[str]) -> List[str]:
        lex_with_slops = []
        if self._phrase_slop == 0:
            lex_with_slops = lex_words
        else:
            slop_pattern = self._get_slop_pattern()
            for phrase in lex_words:
                words = phrase.split()
                pattern = slop_pattern.join(words)
                lex_with_slops.append(pattern)
        return lex_with_slops

    def _dispend_counter_matches(self, counter_matches: List[str], unpacked_match, text: str):
        match = unpacked_match[0]
        match_start = match["span"][0]
        match_end = match["span"][1]

        for counter_match in counter_matches:
            counter_match_start = counter_match["span"][0]
            counter_match_end = counter_match["span"][1]

            if self._counter_matches_preceeding and counter_match_end < match_start:
                section = text[counter_match_end:match_start].strip()
                if not self._ignore_punctuation:
                    if re.search(self._counter_ignore_pattern, section):
                        continue

                words = section.split()

                # Don't allow punctuation chars as separate words
                words = [w for w in words if w not in self._punctuation]

                if len(words) <= self._counter_slop:
                    return []

            if self._counter_matches_succeeding and counter_match_start > match_end:
                section = text[match_end:counter_match_start].strip()
                if not self._ignore_punctuation:
                    if re.search(self._counter_ignore_pattern, section):
                        continue

                words = section.split()
                # Don't allow punctuation chars as separate words
                words = [w for w in words if w not in self._punctuation]

                if len(words) <= self._counter_slop:
                    return []

        return unpacked_match

    def _generate_patterns(self, lexicon: List[str], operator: str, match_type: str) -> List[str]:
            patterns = []
            prefix = self._get_prefix(match_type)
            suffix = self._get_suffix(match_type)

            lex_with_slops = self._add_slops(lexicon)

            if operator == "or":
                pattern = "|".join(lex_with_slops)
                if self._n_allowed_edits > 0:
                    pattern = rf"({pattern}){self._edit_pattern}"
                full_pattern = prefix + pattern + suffix
                patterns.append(full_pattern)
            else:
                for w in lex_with_slops:
                    if self._n_allowed_edits > 0:
                        w = rf"({w}){self._edit_pattern}"
                    full_pattern = prefix + w + suffix
                    patterns.append(full_pattern)
            return patterns

    def _unpack_match(self, match) -> List[Dict[str, Union[str, List[int]]]]:
        raw_start = match.start()
        raw_end = match.end()
        raw_str_val = match.group()

        if re.search(r"^\s", raw_str_val):
            raw_start += 1
        if re.search(r"\s$", raw_str_val):
            raw_end -= 1
        span = [raw_start, raw_end]
        str_val = raw_str_val.strip()
        unpacked_match = [{"str_val": str_val.lower(), "span": span}]
        return unpacked_match

    def _get_counter_matches(self, text: str) -> List[Dict[str, Union[str, List[int]]]]:
        counter_matches = []
        for pattern in self._counter_patterns:
            if self._ignore_case:
                matches = re.finditer(pattern, text, flags=re.IGNORECASE)
            else:
                matches = re.finditer(pattern, text)
            for match in matches:
                unpacked_match = self._unpack_match(match)
                counter_matches.extend(unpacked_match)
        return counter_matches

    def get_matches(self, text: str) -> List[Dict[str, Union[str, List[int]]]]:
        matches_list = []
        found_matches = 0
        nr_patterns = len(self._patterns)

        counter_matches = self._get_counter_matches(text)

        for pattern in self._patterns:
            pattern_matches = 0

            if self._ignore_case:
                matches = re.finditer(pattern, text, flags=re.IGNORECASE)
            else:
                matches = re.finditer(pattern, text)

            for i, m in enumerate(matches):

                unpacked_match = self._unpack_match(m)

                if self._counter_lexicon:
                    unpacked_match = self._dispend_counter_matches(counter_matches, unpacked_match, text)

                if unpacked_match:
                    pattern_matches+=1

                matches_list.extend(unpacked_match)

            if pattern_matches > 0:
                found_matches+=1

            if self._operator == "and" and pattern_matches == 0 and self._required_words == 1.0:
                break

        if self._operator == "and" and (found_matches/float(nr_patterns)) < self._required_words:
            matches_list = []

        return matches_list
