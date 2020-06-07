import sys
import bz2
import csv
import jsonlines
from pathlib import Path

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: {} /path/to/jsonl/directory".format(sys.argv[0]))
        exit(1)

    data_directory = Path(sys.argv[1])

    if not data_directory.is_dir():
        print("Directory {} not found".format(data_directory))
        exit(1)

    hashtag_nodes = {}
    hashtag_edges = {}

    for bz2_filename in data_directory.glob("*.bz2"):

        jsonl_filename = bz2_filename.with_suffix(".jsonl")

        if not jsonl_filename.is_file():
            with open(jsonl_filename, 'wb') as jsonl_file, open(bz2_filename, 'rb') as bz2_file:
                jsonl_file.write(bz2.decompress(bz2_file.read()))

        with jsonlines.open(jsonl_filename) as reader:
            for tweet in reader.iter(type=dict, skip_invalid=True):

                if (
                    not tweet.get("delete")
                    and not tweet.get("retweeted_status")
                    and tweet.get("lang") == "en"
                ):

                    hashtags = [
                        h["text"]
                        for h in tweet["entities"]["hashtags"]
                    ]

                    for index, hashtag in enumerate(hashtags, start=1):

                        if hashtag_nodes.get(hashtag):
                            hashtag_nodes[hashtag] += 1
                        else:
                            hashtag_nodes[hashtag] = 1

                        for co_hashtag in hashtags[index:]:
                            if co_hashtag != hashtag:
                                edge = tuple(sorted([hashtag, co_hashtag]))
                                if hashtag_edges.get(edge):
                                    hashtag_edges[edge] += 1
                                else:
                                    hashtag_edges[edge] = 1

    with open("hashtag_nodes.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Size"])
        writer.writerows(sorted(
            [
                (h, hashtag_nodes[h])
                for h in hashtag_nodes if hashtag_nodes[h] > 1
            ],
            key=lambda t: t[1],
            reverse=True
        ))

    with open("hashtag_edges.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight"])
        writer.writerows(sorted(
            [
                (h[0], h[1], hashtag_edges[h])
                for h in hashtag_edges if hashtag_edges[h] > 1
            ],
            key=lambda t: t[2],
            reverse=True
        ))
