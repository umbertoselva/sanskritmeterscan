The Sanskrit Meterscan
======================

The Sanskrit Meterscan ([sanskritmeterscan.net](http://sanskritmeterscan.net)) is a web tool that outputs an interlinear metrical scansion of poetic verses composed in the Sanskrit language.

An input such as:

    yé triṣaptā́ḥ pariyánti
    víśvā rūpā́ṇi bíbhrataḥ |
    vācás pátir bálā téṣāṃ
    tanvò adyá dadhātu me ||1||

will produce the following output

    yé triṣaptā́ḥ pariyánti
    HLHHLLHL
    víśvā rūpā́ṇi bíbhrataḥ |
    HHHHLHLL
    vācás pátir bálā téṣāṃ
    HHLHLHHH
    tanvò adyá dadhātu me ||1||
    HHHLLHLH

The metrical notation is the following:

*   H = ‘Heavy’ syllable
*   L = ‘Light’ syllable

Development
-----------

A first demo of the Python script that outputs the metrical scansion was designed by Kristen De Joseph in 2014. Umberto Selva revised the Python script and developed the web app around it with Python (Flask), HTML, CSS and Javascript in 2020.

How to use it
-------------

The Sanksrit Meterscan works with plain text and .txt files only.

You can choose to:

*   Upload a .txt file (max size 2MB) containing your verses
    *   Choose your file and press the “Scan File” button
    *   A scansion will be prepared and you will be asked whether you want to
        *   Download the scansion as a .txt file (the filename will be your original file’s name followed by \_SCAN.txt)
        *   Display the scansion as HTML in a new tab
*   Paste plain text in the textarea
    *   Press the “Scan Text” button
        *   A scansion will be displayed as HTML in a new tab

### Leading and trailing notations

Please check the checkbox if, on each single line of your text, the verses are preceded by some verse number notation, as in the following example:

    Allowed input (with checkbox checked):
    <1.1.1a>   śaṃ no devīr abhiṣṭaya 
    <1.1.1b>   āpo bhavantu pītaye | 
    <1.1.1c>   śaṃ yor abhi sravantu naḥ ||

N.B. If some lines feature a preceding verse number notation and some lines don’t, as in the following example, the program will **not** produce a correct output.

    Not-allowed input:
    <1.1.1a>   śaṃ no devīr abhiṣṭaya 
    āpo bhavantu pītaye | 
    śaṃ yor abhi sravantu naḥ || 

That is because, if the checkbox is ticked, the program will very simply remove all the text before the first _whitespace_ on each line. Therefore, in the example above, not only the leading notation on line 1a will be removed, but also the words `āpo` (on line 1b) and `śaṃ` (on line 1c), and the resulting scansion would be incorrect. For the same reason, if your leading notation contains _whitespace_, only the portion preceding such whitespace will be removed, and the output will once again be incorrect.

The program should be able to automatically remove any existing trailing notation on any line without problems, regardless of whether each line features it or only some do or whether they feature different types of notation. Therefore texts as the following (typical of the GRETIL library) should pose no problems.

    Allowed input (checkbox unchecked):
    asty uttarasyāṃ diśi devatātmā himālayo nāma nagādhirājaḥ /
    pūrvāparau toyanidhī vigāhya sthitaḥ pṛthivyā iva mānadaṇḍaḥ // Ks_1.1 //

Vedic (Syllable restoration - Caesura)
--------------------------------------

The Vedic version of the Meterscan ([sanskritmeterscan.net/vedic](http://sanskritmeterscan.net/vedic)) has the following features:

*   it tolerates accents
*   it counts the vowel preceding _ch_ as heavy
*   it applies the _vocalis ante vocalem corripitur_ rule
*   but it **does not** automate syllable restoration (as in _tanvè_ > _tanúve_ )

If the verses consist of 11 or 12 syllables and there is a whitespace after the 4th or 5th syllable, it automatically **attempts** to insert a caesura (represented by the “|” sign).

To illustrate the functionalities just described, please look at the following example:

    10.129.1a     nā́sad āsīn nó sád āsīt tadā́nīṃ
    10.129.1b     nā́sīd rájo nó vyòmā paró yát
    10.129.1c     kím ā́varīvaḥ kúha kásya śármann
    10.129.1d     ámbhaḥ kím āsīd gáhanaṃ gabhīrám

The above input will yield the following output (with checkbox checked):

    10.129.1a     nā́sad āsīn nó sád āsīt tadā́nīṃ
    HLHH|H|LHHLHH
    10.129.1b     nā́sīd rájo nó vyòmā paró yát
    HHLHHHHLHL
    10.129.1c     kím ā́varīvaḥ kúha kásya śármann
    LHLHH|LLHLHH
    10.129.1d     ámbhaḥ kím āsīd gáhanaṃ gabhīrám
    HHLHH|LLHLHL

As you can see, the Vedic Meterscan was able to recognize that line 1a is an 11-syllable line. It thus attempted to insert the caesura. In fact it inserted two, after the 4th and after the 5th syllable, because theoretically the caesura could appear in either places.  
As for line 1b, it contains the word _vyòma_, in which a syllable should be restored (_víoma_). The Vedic Meterscan is not programmed to operate syllable restoration. Therefore it counted 10 syllables in total and did not attempt to insert a caesura.  
In lines c and d, the Vedic Meterscan correctly counted 11 syllables and thus tried to insert a caesura, which could only go after the 5th syllable in either lines.

N.B. If the inputted text features two 11 or 12-syllable lines in the same row of text, the Vedic Meterscan will “perceive” them as a single poetic line, it will count a total of more than 11/12 syllables, and thus it will not insert any caesura. For instance, the following input

    10.129.01ab     nā́sad āsīn nó sád āsīt tadā́nīṃ nā́sīd rájo nó vyòmā paró yát |
    10.129.01cd     kím ā́varīvaḥ kúha kásya śármann ámbhaḥ kím āsīd gáhanaṃ gabhīrám ||

will yield

    10.129.01ab     nā́sad āsīn nó sád āsīt tadā́nīṃ nā́sīd rájo nó vyòmā paró yát |
    HLHHHLHHLHHHHLHHHHLHL
    10.129.01cd     kím ā́varīvaḥ kúha kásya śármann ámbhaḥ kím āsīd gáhanaṃ gabhīrám ||
    LHLHHLLHLHHHHLHHLLHLHL

We hope that, despite these limited functionalities, Vedic scholars will find this tool useful too.