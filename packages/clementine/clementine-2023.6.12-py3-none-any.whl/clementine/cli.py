"""The clementine CLI."""

import click

from clementine import about, blossom

_CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}


@click.group(context_settings=_CONTEXT_SETTINGS, help=about.__description__)
@click.version_option(
    about.__version__, '-v', '--version', message=about.__pretty_version__
)
def main():
  """The main entry point for the clementine CLI."""
  pass


@main.command()
@click.argument('url')
@click.option(
    '-o',
    '--output-dir',
    help=(
        'The directory to save the screenshots to. Defaults to "screenshots" '
        'in the current working directory.'
    )
)
@click.option(
    '-f',
    '--filename',
    help=(
        'The base filename to use for the screenshots. Defaults to "screenshot". '
        'The screenshots will be saved as screenshot-light.png and '
        'screenshot-dark.png, for example.'
    )
)
@click.option(
    '--full-page/--no-full-page',
    default=False,
    help='Whether to take a screenshot of the full page. Defaults to False.'
)
def screenshot(url, output_dir, filename, full_page):
  """Take screenshots of a webpage in light and dark mode. The URL must include
  the scheme, e.g. https:// or file:///.
  """
  paths = blossom.screenshot(
      url, output_dir=output_dir, filename=filename, full_page=full_page
  )
  click.echo(f'The screenshots of {url} were saved at these paths: ')
  for path in paths:
    click.echo(f'- {path}')


if __name__ == '__main__':
  main()
