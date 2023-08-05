"""Console script for saxtract."""
#!/usr/bin/env python3 # noqa: E265

import sys
import click
from .saxtract import Saxtract


@click.command()
@click.argument('tags', nargs=-1, default=None)
@click.option('--instream', type=click.File('r'), default=sys.stdin)
@click.option('--outstream', type=click.File('w'), default=sys.stdout)
@click.option('--child-tag', default=None, help='xml tag of each record which will be split via newline')
@click.option('--show-tags/--no-show-tags', default=False)
@click.option('-v', '--verbose', count=True)
def main(tags, instream, outstream, child_tag, show_tags, verbose):
    """Console script for saxtract."""
    # override the default ContextHandler
    handler = Saxtract(tags=tags, instream=instream, outstream=outstream,
                       child_tag=child_tag, show_tags=show_tags, verbose=verbose)
    handler.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
