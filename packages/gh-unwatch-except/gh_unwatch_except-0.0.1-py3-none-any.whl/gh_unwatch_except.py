import os
import sys

import click
from github import Github


@click.command()
@click.argument('keywords', nargs=-1)
def main(keywords):
    try:
        token = os.environ['GITHUB_ACCESS_TOKEN']
    except KeyError:
        raise click.ClickException('Environment variable "GITHUB_ACCESS_TOKEN" is not set.')

    gh = Github(token)
    user = gh.get_user()
    watched = user.get_watched()

    skip = []
    unwatch = []

    for repo in watched:
        if any(keyword in repo.name for keyword in keywords):
            if click.confirm(f'Do you want to unwatch repository "{repo.full_name}" ?'):
                unwatch.append(repo)
            else:
                skip.append(repo)
        else:
            unwatch.append(repo)

    click.secho('Unwatch repositories', bg='red', fg='black')
    for repo in unwatch:
        click.secho(f'\t {repo.full_name}', fg='red')

    click.secho('Watch repositories', bg='green', fg='black')
    for repo in skip:
        click.secho(f'\t {repo.full_name}', fg='green')

    if click.confirm('\nAre you sure you want to proceed?'):
        for repo in unwatch:
            click.echo(f'Unwatching "{repo.full_name}" ...')
            user.remove_from_watched(repo)
        click.echo('DONE!')


if __name__ == '__main__':
    main()
