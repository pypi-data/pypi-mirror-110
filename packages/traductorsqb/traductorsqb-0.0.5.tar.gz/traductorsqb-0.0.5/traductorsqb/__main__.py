from translate import Translator
import click


@click.command()
@click.argument('palabra_en')
def main(palabra_en):
	print('Traduciendo...')
	translator = Translator(from_lang='english', to_lang='Spanish')
	palabra_es = translator.translate(palabra_en)
	print(f"{palabra_en} -> {palabra_es}")

if __name__ == '__main__':
	main()