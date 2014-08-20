import docker
import argparse
from dockertools import utils


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('registry')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    repo = utils.full_name(args.image, registry=args.registry)

    c = docker.Client()
    c.tag(args.image, repo)
    c.push(repo, stream=False)
