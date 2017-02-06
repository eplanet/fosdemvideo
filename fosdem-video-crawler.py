#!/usr/bin/python3

import os, sys
import argparse, logging
import urllib.request
import lxml.html
import concurrent.futures

URL_TEMPLATE = "https://fosdem.org/%d/schedule/xml"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FOSDEM video crawler")
    parser.add_argument("--output", help="Output directory", required=True)
    parser.add_argument("--year", type=int, default=2017,
            help="Year for which to crawl videos (default: %(default)s)")
    parser.add_argument("--extension", default="mp4",
            help="Extension for video download (default: %(default)s)")
    parser.add_argument("--jobs", type=int, default=1,
            help="Number of threads (default: %(default)s)")
    args = parser.parse_args(sys.argv[1:])
    logging.basicConfig(level=logging.DEBUG)

    if args.output is None or not os.path.exists(args.output):
        logging.error("Provided output '%s' does not exist" % (args.output))
        parser.print_help()
        sys.exit(1)

    url = URL_TEMPLATE % (args.year)
    res = urllib.request.urlopen(url)
    doc = lxml.html.parse(res)
    ns = {"re": "http://exslt.org/regular-expressions"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as e:
        for video_url in doc.xpath(r"//link[re:test(@href, '\.(?:mp4)', 'i')]/@href",
                namespaces=ns, smart_strings=False):
            parsed_url = urllib.parse.urlsplit(video_url)
            target_path = os.path.join(args.output,
                    os.path.dirname(parsed_url.path)[parsed_url.path.find(str(args.year)):])
            target_filename = os.path.basename(parsed_url.path)
            target_filepath = os.path.join(target_path, target_filename)
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            if os.path.exists(target_filepath):
                logging.warn("Target file already exists: %s" % (target_filepath))
            else:
                logging.debug("Saving to: %s" % (target_filepath))
                e.submit(urllib.request.urlretrieve, video_url, target_filepath)
