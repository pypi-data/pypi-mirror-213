"""
Main code
"""
from ._version import __version__
import argparse
import sys
import subprocess
import logging
import os
import yaml
import logging
logger = logging.getLogger('bigenius_discovery')
logging.getLogger('logger').disabled = True
logging.getLogger('datahub.ingestion.run.pipeline').disabled = True
logging.getLogger('datahub.ingestion.source.s3.data_lake_utils').disabled = True

# Initialize coloredlogs.
import coloredlogs


os.environ["DATAHUB_TELEMETRY_ENABLED"] = "false"
os.environ["WERCKER_ROOT"] = "false"
os.environ["SPARK_VERSION"]="3.0"

from datahub.ingestion.run.pipeline import Pipeline

def main(parser=argparse.ArgumentParser()):
    """main function"""

    coloredlogs.install(level=logging.ERROR)

    parser.add_argument("-f", "--file", type=str, required=True, help="Source file")
    parser.add_argument(
        "-e", "--version", action="store_true", help="Shows the app version."
    )
    parser.add_argument(
        "-q", "--quick", action="store_true", help="Skip the Python library install"
    )
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
)
    parser.add_argument("-l", "--loglevel", action="store_true", help="Shows the output.")

    args = parser.parse_args()
    #logging.basicConfig(level=args.loglevel)
    
    coloredlogs.install(level=args.loglevel)

    if args.version:
        return __version__

    config_dict = load_config_json(args.file)
    source_type = config_dict.get("source", {}).get("type")
    output_file = config_dict.get("sink", {}).get("config", {}).get("filename")
    
    execute_pip_deplyoment(source_type, args.quick)
    try:
        pipeline = Pipeline.create(config_dict)

        logger.debug(f"cli_report:{pipeline.cli_report}")
        pipeline.run()
        print(f"Discovery file saved at {output_file}")
    except Exception as e:
        logger.error(f"An error happen! Message:{str(e)}") 

def set_log_level(loglevel: str):
    """will support log level configuration"""
    


def load_config_json(filename: str):
    """Load ingestion config from file"""
    logger.debug(f"Opening config file: {filename}")
    with open(filename, "r") as stream:
        try:
            # Converts yaml document to python object
            config_dict = yaml.safe_load(stream)

            return config_dict
            # Printing dictionary
            #print(config_dict)
            
        except yaml.YAMLError as exception_object:
            print(exception_object)

        


def execute_pip_deplyoment(source_type, quick):
    """Execute pip deloyment"""
    logger.debug(f"source_type:{source_type}")
    package = f"acryl-datahub[{source_type}]"
    print(f"biGENIUS discovery started with {source_type} driver.")
    if not quick:
        logger.debug(f"package:{package}")
        logger.debug(f"Install pip update and install the following pip package:{package}")
        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip","-q"])
        subprocess.call([sys.executable, "-m", "pip", "install", str(package), "-q"])
    logger.debug(f"Environment is prepared")


if __name__ == "__main__":
    main()
