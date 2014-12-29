import zlib
import zmq.green as zmq
import requests
import simplejson
import datetime
import argparse
import logging
import sys

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-E", "--elasticsearch", type=str, default='localhost:9200', help="Elasticsearch HTTP host:port")
    parser.add_argument("-I", "--index", type=str, default='eddn-%Y.%m.%d', help="Elasticsearch index")
    parser.add_argument("-R", "--relay", type=str, default='tcp://eddn-relay.elite-markets.net:9500', help="EDDN Relay URL")
    parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0, help="increases log verbosity for each occurence.") 
    parser.add_argument('-O', "--output", type=argparse.FileType('w'), default=sys.stdout, help="redirect output to a file") 

    args = parser.parse_args()
    
    logging.basicConfig(stream=args.output, level=logging.DEBUG, format='%(asctime)s (%(levelname)s): %(message)s')
    log = logging.getLogger(__file__)

    # sets log level to ERROR going more verbose for each new -v.
    log.setLevel(max(4 - args.verbosity, 0) * 10)

    log.info("Starting up")

    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    try:
        subscriber.connect(args.relay)
    except:
        log.error("Failed to connect to relay")
        sys.exit(1)
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    log.info("Connected to relay - waiting for data")

    while True:
        market_json = zlib.decompress(subscriber.recv())
        market_data = simplejson.loads(market_json)

        elasticsearch_url = 'http://%s/%s/market' % (
            args.elasticsearch,
            datetime.datetime.now().strftime(args.index)
        )

        log.info("Received data")
        log.debug("Sending %s to %s" % (market_data, elasticsearch_url))

        try:
            requests.post(elasticsearch_url, market_json)
        except:
            log.error("Failed to send data to elasticsearch - quitting")
            sys.exit(2)

if __name__ == '__main__':
    main()
