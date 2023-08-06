import os
import click

@click.command(name='process_rfile')
@click.option('-i', '--input_file', 'filename', required=True, 
              help='Input ROOT file to process.')
@click.option('-c', '--config', 'config_path', required=True,
              help='Path to the processor card.')
@click.option('--multithread/--no-multirhread', default=True, show_default=True,
              help='Enable implicit multi-threading.')
@click.option('-t', '--tag', default=None,
              help='Include `tag` as a global variable.')
@click.option('-f', '--flag', default=None,
              help='Flags to set (separated by commas).')
@click.option('-v', '--verbosity',  default="INFO", show_default=True,
              help='verbosity level ("DEBUG", "INFO", "WARNING", "ERROR")')
def process_rfile(filename, config_path, multithread, tag, flag, verbosity):
    """
    Process a ROOT file based on RDataFrame routines.
    """
    from quickstats.components.processors import RooProcessor
    from quickstats.utils.string_utils import split_str
    if flag is not None:
        flags = split_str(flag, sep=',', remove_empty=True)
    else:
        flags = []
    rprocessor = RooProcessor(config_path, multithread=multithread, flags=flags, verbosity=verbosity)
    rprocessor.global_variables['tag'] = tag
    rprocessor.run(filename)