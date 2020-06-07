# Twitter Hashtags Network Generator

Input: tweets from [Internet Archive](https://archive.org/search.php?query=collection%3Atwitterstream&sort=-publicdate).

Output: csv files ready for [Gephi](https://gephi.org/).

Pre-requisites:

- Python 3.7+
- [jsonlines](https://jsonlines.readthedocs.io/en/latest/)

Usage:

- download and decompress a supported archive (file `archiveteam-twitter-stream-*`)
- run `python main /path/to/data/` where `path/to/data/` is a folder containing `.bz2` files
- check if `hashtag_nodes.csv` and `hashtag_edges.csv` are created and are not empty
- import both files in Gephi using [Data Laboratory](https://github.com/gephi/gephi/wiki/Import-CSV-Data)
- apply your filters, layouts, analysis, and enjoy!

Warnings:

- retweets and tweets with no `lang="en"` attribute are rejected
- hashtags with only one occurence are filtered out
- edges between hashtags with weight equal to one are filtered out

## License

Public Domain.
