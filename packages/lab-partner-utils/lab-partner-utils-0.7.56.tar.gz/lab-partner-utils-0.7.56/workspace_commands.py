#!/usr/bin/env python
import click


@click.group()
def cmd():
    """
    Example LAB_WORKSPACE discovered commands
    """
    pass


@cmd.command()
def hello():
    """
    Example command that prints 'hello world' to stdout
    """
    click.echo('hello world')


if __name__ == '__main__':
    cmd()