from googletrans import Translator

translator = Translator()
print(translator.translate('veritas lux mea', src='la', dest='en').text)