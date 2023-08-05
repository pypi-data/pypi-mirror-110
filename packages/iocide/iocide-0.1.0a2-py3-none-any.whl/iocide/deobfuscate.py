from unidecode import unidecode


def normalise(text: str):
	visibile_text = text.replace('\u200b', '')
	return unidecode(visibile_text, errors='preserve')
