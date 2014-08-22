import os
import subprocess

import click
from dns import resolver
from dockertools import utils


DOCKER = os.environ.get('DOCKER', '/usr/bin/docker')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def get_host(hostname):
    try:
        query = resolver.query('_docker_registry.{}'.format(hostname), 'PTR')
        answer = list(query)[0]
    except:
        return hostname
    else:
        return answer.to_text().rstrip('.')


def get_host_ui(hostname):
    if hostname:
        registry = get_host(hostname)
        if registry != hostname:
            click.secho('Resolved {} to {}'.format(
                click.style(hostname, fg='yellow'),
                click.style(registry, fg='yellow')
            ))
        return registry


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('image', metavar='NAME[:TAG]')
@click.argument('registry', required=False)
def push(image, registry):
    """
    Push an image or a repository to the given registry, independently from
    its current tag.
    """

    registry = get_host_ui(registry)
    repo = utils.full_name(image, registry=registry)

    if repo != image:
        subprocess.call([DOCKER, 'tag', image, repo])
    subprocess.call([DOCKER, 'push', repo])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('image', metavar='NAME[:TAG]')
@click.argument('registry', required=False)
def pull(image, registry):
    """
    Pull an image or a repository from the given registry, independently from
    its tag.
    """

    registry = get_host_ui(registry)
    repo = utils.full_name(image, registry=registry)

    subprocess.call([DOCKER, 'pull', repo])

    if repo != image:
        subprocess.call([DOCKER, 'tag', repo, image])
