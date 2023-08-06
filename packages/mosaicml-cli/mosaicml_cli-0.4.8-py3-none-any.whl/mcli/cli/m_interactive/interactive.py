"""
mcloud interactive
"""

import argparse
import logging
from typing import Optional

from mcli.api.cluster import get_clusters
from mcli.api.exceptions import MintException
from mcli.api.mint import shell
from mcli.api.model.run import RunConfig
from mcli.api.runs.api_create_run import create_run
from mcli.cli.m_connect.m_connect import configure_connection_argparser, get_tmux_command, wait_for_run
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_types import get_hours_type

logger = logging.getLogger(__name__)


def interactive(
    name: Optional[str] = None,
    cluster: Optional[str] = None,
    gpu_type: Optional[str] = None,
    gpus: Optional[int] = None,
    hours: Optional[float] = None,
    image: str = 'mosaicml/pytorch',
    rank: int = 0,
    connect: bool = True,
    command: Optional[str] = None,
    **kwargs,
) -> int:
    del kwargs

    if not cluster:
        clusters = get_clusters()
        if not clusters:
            raise RuntimeError('No clusters available. Contact your administrators to set one up')
        elif len(clusters) == 1:
            cluster = clusters[0].name
        else:
            values = ", ".join([c.name for c in clusters])
            raise RuntimeError('Multiple clusters available. Please use the --cluster argument to set the '
                               f'cluster to use for interactive. Available clusters: {values}')

    run_config = RunConfig(
        name=name or f'interactive-{(gpu_type or "none").replace("_", "-")}-{gpus or 0}'.lower(),
        image=image,
        command=f'sleep {int(3600 * (hours or 1))}',
        gpu_num=gpus,
        gpu_type=gpu_type,
        cluster=cluster,
        optimization_level=0,
    )

    run = create_run(run_config)
    ready = wait_for_run(run)
    if not ready:
        return 1

    if not connect:
        return 0

    try:
        mint_shell = shell.MintShell(run.name, rank=rank)
        mint_shell.connect(command=command)
    except MintException as e:
        logger.error(f'{FAIL} {e}')
        return 1
    return 0


def interactive_entrypoint(
    name: Optional[str] = None,
    cluster: Optional[str] = None,
    gpu_type: Optional[str] = None,
    gpus: Optional[int] = None,
    hrs: Optional[float] = None,
    hours: Optional[float] = None,
    image: str = 'mosaicml/pytorch',
    connect: bool = True,
    rank: int = 0,
    command: Optional[str] = None,
    tmux: Optional[bool] = None,
    **kwargs,
) -> int:
    del kwargs

    # Hours can be specified as a positional argument (hrs) or named argument (hours)
    if hours and hrs:
        logger.error(f'{FAIL} The duration of your interactive session was specified twice. '
                     'Please use only the positional argument or --hours. '
                     'See mcli interactive --help for more details.')

    hours = hrs or hours
    if hours is None:
        logger.error(f'{FAIL} Please specify the duration of your interactive session. '
                     'See mcli interactive --help for details.')
        return 1

    if tmux:
        command = get_tmux_command()

    return interactive(
        name=name,
        cluster=cluster,
        gpu_type=gpu_type,
        gpus=gpus,
        hours=hours,
        image=image,
        rank=rank,
        connect=connect,
        command=command,
    )


# TODO: Move into mcli/cli/m_interactive/m_interactive.py once kube mcli deprecated
def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:

    hrs_grp = parser.add_mutually_exclusive_group()
    hrs_grp.add_argument(
        'hrs',
        metavar='HOURS',
        nargs='?',
        type=get_hours_type(),
        help='Number of hours the interactive session should run',
    )
    hrs_grp.add_argument(
        '--hours',
        nargs='?',
        type=get_hours_type(),
        help='Number of hours the interactive session should run',
    )

    parser.add_argument(
        '--name',
        default=None,
        metavar='NAME',
        type=str,
        help='Name for the interactive session. '
        'Default: "interactive-<gpu type>-<gpu num>"',
    )

    parser.add_argument(
        '--image',
        default='mosaicml/pytorch',
        help='Docker image to use',
    )

    cluster_arguments = parser.add_argument_group(
        'Compute settings',
        'These settings are used to determine the cluster and compute resources to use for your interactive session',
    )
    cluster_arguments.add_argument('--cluster',
                                   default=None,
                                   metavar='CLUSTER',
                                   help='Cluster where your interactive session should run. If you '
                                   'only have one available, that one will be selected by default. '
                                   'Depending on your cluster, you\'ll have access to different GPU types and counts. '
                                   'See the available combinations above. ')

    cluster_arguments.add_argument(
        '--gpu-type',
        metavar='TYPE',
        help='Type of GPU to use. Valid GPU types depend on the cluster and GPU numbers requested',
    )
    cluster_arguments.add_argument(
        '--gpus',
        type=int,
        metavar='NGPUs',
        help='Number of GPUs to run interactively. Valid GPU numbers depend on the cluster and GPU type',
    )

    connection_arguments = parser.add_argument_group(
        'Connection settings',
        ('These settings are used for connecting to your interactive session. '
         'You can reconnect anytime using `mcli connect`'),
    )
    connection_arguments.add_argument(
        '--no-connect',
        dest='connect',
        action='store_false',
        help='Do not connect to the interactive session immediately',
    )
    configure_connection_argparser(connection_arguments)
    parser.set_defaults(func=interactive_entrypoint)
    return parser


def add_interactive_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    examples = """

Examples:

# Create a 1 hour run to be used for interactive
> mcli interactive --hours 1

# Connect to the latest run
> mcli connect
    """

    interactive_parser: argparse.ArgumentParser = subparser.add_parser(
        'interactive',
        help='Create an interactive session',
        description=('Create an interactive session. '
                     'Once created, you can attach to the session. '),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=examples,
    )
    get_parser = configure_argparser(parser=interactive_parser)
    return get_parser
