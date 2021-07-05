import argparse
from highlight_butler.handlers.highlight_import_handler import HighlightImportHandler
from highlight_butler.utils.config import Config

def main():

    parser = argparse.ArgumentParser(
        description="Highlight butler imports highlights from various sources and creates markdown notes for note-taking systems")

    parser.add_argument("--config", type=argparse.FileType("r"),
                        default="./highlight_butler/resources/config.yaml", help="config file")
    
    args = parser.parse_args()
    
    _config = Config()
    _config.load(args.config)
    
    highlightImportHandler: HighlightImportHandler = HighlightImportHandler()
    highlightImportHandler.handle()


if __name__ == "__main__":
    main()
