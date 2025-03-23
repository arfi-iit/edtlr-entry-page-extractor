"""Romanian Canonical Form."""
import unicodedata


class DIACRITICS:
    """Defines constants for Romanian diacritics."""

    CIRCUMFLEX_ACCENT = '\u0302'
    BREVE = '\u0306'
    COMMA_BELOW = '\u0326'

    ABOVE_LETTER = [CIRCUMFLEX_ACCENT, BREVE]
    BELOW_LETTER = [COMMA_BELOW]
    ALL = ABOVE_LETTER + ABOVE_LETTER

    CIRCUMFLEX_MARK = format(ord(CIRCUMFLEX_ACCENT), '04x')  # 0302
    BREVE_MARK = format(ord(BREVE), '04x')  # 0306
    COMMA_BELOW_MARK = format(ord(COMMA_BELOW), '04x')  # 0326
    MARKS_ABOVE = [CIRCUMFLEX_MARK, BREVE_MARK]
    MARKS_BELOW = [COMMA_BELOW_MARK]
    ALL_MARKS = MARKS_ABOVE + MARKS_BELOW


def get_valid_diacritics(chr: str) -> list[str] | None:
    """Get the diacritics that are valid for the provided character.

    Parameters
    ----------
    chr: str, reqired
        The character for which to get valid diacritics.

    Returns
    -------
    diacritics: list of str or None
        The list of valid diacritics for the provided character, or None.
    """
    if chr is None or len(chr) != 1:
        raise ValueError("Value must have length 1.")

    chr = chr.upper()
    if chr == 'A':
        return DIACRITICS.ABOVE_LETTER
    if chr == "I":
        return [DIACRITICS.CIRCUMFLEX_ACCENT]
    if chr in "ST":
        return DIACRITICS.BELOW_LETTER
    return None


def to_normalization_form_c(value: str) -> str:
    """Convert the value to Normalization Form C (NFC).

    Parameters
    ----------
    value: str, required
        The value to normalize.

    Returns
    -------
    normal_form: str
        The normal form of the provided string.
    """
    return unicodedata.normalize('NFC', value)


def code_point_to_char(code_point: str) -> str:
    """Convert the specified Unicode code point to its string representation.

    The `code_point` is a string representation of an int value in base 16
    without the prefix; e. g.: 0302, 0326 etc.

    Parameters
    ----------
    code_point: str, required
        The base 16 representation of a code point, without prefix.

    Returns
    -------
    value: str
        The string that represents the code point.
    """
    return chr(int(code_point, 16))


def decompose_char(chr: str) -> tuple[str, list[str]]:
    """Decompose the provided char into its base character and combining characters.

    Parameters
    ----------
    chr: str, required
        The character to decompose.

    Returns
    -------
    (base_chr, combining_chars): tuple of (str, list of str)
        The decomposition of the provided characters.
    """
    if chr is None or len(chr) != 1:
        raise ValueError("The provided string should be of length 1.")

    chr = to_normalization_form_c(chr)
    combining = []
    composition = unicodedata.decomposition(chr)
    if len(composition) == 0:
        return (chr, [])

    while len(composition) > 0:
        chr_cp, comb_cp = composition.split()
        combining.insert(0, comb_cp)
        chr = code_point_to_char(chr_cp)
        composition = unicodedata.decomposition(chr)
    return (chr, [code_point_to_char(cp) for cp in combining])


def normalize(text: str) -> str | None:
    """Remove the accents in the provided string, except for Romanian diacritic marks.

    Parameters
    ----------
    text: str, required
        The character to strip of accents other than Romanian diacritics.

    Returns
    -------
    normalized: str
        The provided text without accents other than Romanian diacritics.
    """
    if text is None:
        return None

    def normalize_chr(chr):
        chr, combining = decompose_char(chr)
        valid_marks = get_valid_diacritics(chr)
        if valid_marks is None:
            return chr

        diacritic = next((c for c in combining if c in valid_marks), None)
        if diacritic is None:
            return chr
        return chr + diacritic

    return "".join([normalize_chr(c) if c.isalpha() else c for c in text])
