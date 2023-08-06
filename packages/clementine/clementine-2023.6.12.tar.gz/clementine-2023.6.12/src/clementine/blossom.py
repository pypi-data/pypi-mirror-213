"""Visualization and demonstration utilities."""

import asyncio
import builtins
import importlib
import os
from typing import Optional


async def async_screenshot(
    url: str,
    *,
    output_dir: Optional[str] = None,
    filename: Optional[str] = None,
    full_page: bool = False
) -> list[str]:
  """Take screenshots of a webpage in light and dark mode.

  Use `blossom.async_screenshot()` in asynchronous contexts, such as in a Jupyter
  notebook. Use `blossom.screenshot()` in synchronous contexts, such as in a
  synchronous Python script.

  **Prerequisites**:

  1. Install the Playwright Python package: `pip install playwright`.
  2. Install the Playwright browser dependencies: `playwright install webkit`.


  **Example usage**:

  In a Python script:

  ```python
  from clementine import blossom

  paths = blossom.screenshot('https://example.com')
  ```

  In a Jupyter notebook or other asynchronous context:

  ```python
  from clementine import blossom
  from IPython.display import display, Image

  paths = await blossom.async_screenshot('https://example.com')
  for path in paths:
    display(Image(path, width=600))
  ```

  Args:
    url: The URL to take screenshots of. The URL must include the scheme, e.g. 
      https:// or file:///.
    output_dir: The directory to save the screenshots to. Defaults to
      'screenshots' in the current working directory.
    filename: The base filename to use for the screenshots. Defaults to
      'screenshot'. The screenshots will be saved as screenshot-light.png and
      screenshot-dark.png, for example.
    full_page: Whether to take a screenshot of the full page. Defaults to False.

  Raises:
    ImportError: If the Playwright Python package is not installed.
    Error: If the browser cannot be launched or an invalid url is provided.

  Returns:
    A list of the paths to the screenshots.
  """
  try:
    pw_async_api = importlib.import_module('playwright.async_api')
    pw_api_types = importlib.import_module('playwright._impl._api_types')
  except ImportError as e:
    raise ImportError(
        'The Playwright Python package is not installed. Install it with '
        '`pip install playwright`.'
    ) from e

  async_playwright = pw_async_api.async_playwright
  PlaywrightError = pw_api_types.Error

  output_dir = output_dir or os.path.join(os.getcwd(), 'screenshots')
  filename = filename or 'screenshot'
  output_paths = []

  async with async_playwright() as p:
    try:
      browser = await p.webkit.launch()
    except PlaywrightError as e:
      raise OSError(
          'The browser could not be launched. Install the Playwright browser '
          'dependencies with `playwright install webkit`.'
      ) from e

    page = await browser.new_page()
    await page.goto(url)

    os.makedirs(output_dir, exist_ok=True)
    for color_scheme in ('light', 'dark'):
      await page.emulate_media(color_scheme=color_scheme)
      path = os.path.join(output_dir, f'{filename}-{color_scheme}.png')
      await page.screenshot(path=path, full_page=full_page)
      output_paths.append(path)

    await browser.close()

  return output_paths


def screenshot(
    url: str,
    *,
    output_dir: Optional[str] = None,
    filename: Optional[str] = None,
    full_page=False
) -> list[str]:
  """Runs the coroutine function `blossom.async_screenshot()` and returns its
  results."""
  screenshot.__doc__ = async_screenshot.__doc__
  if getattr(builtins, '__IPYTHON__', False):
    raise RuntimeError(
        'The function `blossom.screenshot()` cannot be called in an asynchronous '
        'context, such as in a Jupyter notebook. Use `blossom.async_screenshot()` '
        'instead.'
    )
  return asyncio.run(
      async_screenshot(
          url, output_dir=output_dir, filename=filename, full_page=full_page
      )
  )
