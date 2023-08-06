# LASERDATO

This package is created to use simply [LASER](https://github.com/facebookresearch/LASER) from MetaAI to create embeddings. It uses list of string as input and returns list of numpy arrays as output instead of using files. It also does not require external tools to be installed. The package automatically downloads the required laser models.

## Issues

* Because of an [issue](https://github.com/facebookresearch/fairseq/issues/5012) with faiss this package cannot go above pyhton 3.10.

* If you encounter the following error:

```
RuntimeError: 
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.

        This probably means that you are not using fork to start your
        child processes and you have forgotten to use the proper idiom
        in the main module:

            if __name__ == '__main__':
                freeze_support()
                ...

        The "freeze_support()" line can be omitted if the program
        is not going to be frozen to produce an executable.
```

You might need to use this (strutucture)[https://pytorch.org/docs/stable/notes/windows.html#multiprocessing-error-without-if-clause-protection] to used embed_sentences with multiple GPUs 

```
def main()
    # do something here

if __name__ == '__main__':
    main()
```


## License

LASER is BSD-licensed, as found in the [`LICENSE`](LICENSE) file in the root directory of this source tree.

## Supported languages

The original LASER model was trained on the following languages:

Afrikaans, Albanian, Amharic, Arabic, Armenian, Aymara, Azerbaijani, Basque, Belarusian, Bengali,
Berber languages, Bosnian, Breton, Bulgarian, Burmese, Catalan, Central/Kadazan Dusun, Central Khmer,
Chavacano, Chinese, Coastal Kadazan, Cornish, Croatian, Czech, Danish, Dutch, Eastern Mari, English,
Esperanto, Estonian, Finnish, French, Galician, Georgian, German, Greek, Hausa, Hebrew, Hindi,
Hungarian, Icelandic, Ido, Indonesian, Interlingua, Interlingue, Irish, Italian, Japanese, Kabyle,
Kazakh, Korean, Kurdish, Latvian, Latin, Lingua Franca Nova, Lithuanian, Low German/Saxon,
Macedonian, Malagasy, Malay, Malayalam, Maldivian (Divehi), Marathi, Norwegian (Bokmål), Occitan,
Persian (Farsi), Polish, Portuguese, Romanian, Russian, Serbian, Sindhi, Sinhala, Slovak, Slovenian,
Somali, Spanish, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Turkish, Uighur,
Ukrainian, Urdu, Uzbek, Vietnamese, Wu Chinese and Yue Chinese.

It has also observed that the model seems to generalize well to other (minority) languages or dialects, e.g.

Asturian, Egyptian Arabic, Faroese, Kashubian, North Moluccan Malay, Nynorsk Norwegian, Piedmontese, Sorbian, Swabian,
Swiss German or Western Frisian.

