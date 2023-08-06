
from omegaconf import OmegaConf
from kafka import KafkaConsumer
from datetime import timedelta

from dna import initialize_logger, config
from dna.event.types import TrackDeleted, TrackletId
from dna.node import EventListener
from dna.event.track_event import TrackEvent
from dna.event.utils import read_tracks_json
from dna.assoc.associator_motion import NodeAssociationSchema, MotionBasedTrackletAssociator
from dna.event.event_processors import PrintEvent
from dna.assoc import Association, AssociationCollector, AssociationCollection
from dna.assoc.closure import AssociationClosureBuilder
from dna.assoc.utils import ClosedAssociationPublisher, AssociationCloser, FixedIntervalCollector

import logging
LOGGER = logging.getLogger('dna.script.sync_tracklets')

import argparse
def parse_args():
    parser = argparse.ArgumentParser(description="Tracklet and tracks commands")
    
    parser.add_argument("node_pairs", nargs='+', help="target node ids")
    parser.add_argument("--boostrap_servers", default=['localhost:9092'], help="kafka server")
    parser.add_argument("--max_distance_to_camera", type=float, metavar="meter", default=55,
                        help="max. distance from camera (default: 55)")
    parser.add_argument("--max_track_distance", type=float, metavar="meter", default=5,
                        help="max. distance between two locations (default: 5)")
    parser.add_argument("--window_interval", type=float, metavar="seconds", default=1,
                        help="window interval seconds (default: 1)")
    parser.add_argument("--closure_build_interval", type=float, metavar="seconds", default=3,
                        help="window interval seconds (default: 3)")
    parser.add_argument("--idle_timeout", type=float, metavar="seconds", default=1,
                        help="idle timeout seconds (default: 1)")
    parser.add_argument("--logger", metavar="file path", help="logger configuration file path")

    return parser.parse_known_args()


def main():
    args, _ = parse_args()

    initialize_logger(args.logger)
    logger = logging.getLogger('dna.assoc.motion')
    
    # argument에 기술된 conf를 사용하여 configuration 파일을 읽는다.
    conf = config.to_conf(args)
    
    assoc_pairs = [tuple(pair_str.split('-')) for pair_str in args.node_pairs]
    schema = NodeAssociationSchema(assoc_pairs)
        
    window_interval_ms = round(args.window_interval * 1000)
    associator = MotionBasedTrackletAssociator(schema,
                                               window_interval_ms=window_interval_ms,
                                               max_distance_to_camera=args.max_distance_to_camera,
                                               max_track_distance=args.max_track_distance,
                                               idle_timeout=args.idle_timeout,
                                               logger=logger)
    
    intvl_collector = FixedIntervalCollector(interval_ms=3*1000)
    associator.add_listener(intvl_collector)
    
    closure_collection = AssociationCollection(keep_best_association_only=True,
                                               logger=logger.getChild('closures'))
    closure_builder = AssociationClosureBuilder(collection=closure_collection)
    closure_builder.add_listener(PrintEvent("**** "))
    intvl_collector.add_listener(closure_builder)
    # associator.start()
    
    bootstrap_servers = config.get(conf, 'bootstrap_servers', default=['localhost:9092'])
    offset = config.get(conf, 'auto_offset_reset', default='earliest')
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                             auto_offset_reset=offset,
                             key_deserializer=lambda k: k.decode('utf-8'))
    consumer.subscribe(['track-events'])
    
    count = 0
    while True:
        partitions = consumer.poll(timeout_ms=1000, max_records=100)
        if partitions:
            for topic_info, partition in partitions.items():
                if topic_info.topic == 'track-events':
                    for te in (TrackEvent.deserialize(serialized.value) for serialized in partition):
                        count += 1
                        associator.handle_event(te)
        else:
            break
    
    associator.close()
    for assoc in closure_collection:
        print(assoc)
            
if __name__ == '__main__':
    main()