# -*- coding: utf-8 -*-
import argparse
import random
import re

from rich.console import Console
from madhac.Logger import Logger


def get_parser():
    desc = 'This script replaces the variables of a template file with the provided values.'
    author = 'Noa'
    description = desc + '\n' + author

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbosity',
        action='count',
        default=0,
        help='verbosity level (-v for verbose, -vv for debug)',
    )
    parser.add_argument(
        '-q',
        '--quiet',
        dest='quiet',
        action='store_true',
        default=False,
        help='Show no information at all',
    )

    parser.add_argument(
        'file',
        help='Template file',
    )
    parser.add_argument(
        'out',
        help='Output file',
    )

    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        help='Prompt for the value of each template variable',
    )
    parser.add_argument(
        '-t',
        '--template',
        action='append',
        nargs=2,
        metavar=('VAR', 'VAL'),
        help='Value for the template variable',
    )

    return parser


def get_options():
    return get_parser().parse_args()


def get_quote():
    quotes = [
        'It\'s no use going back to yesterday, because I was a different person then.',
        'We\'re all mad here.',
        'Curiouser and curiouser!',
        'I don\'t think -- " "Then you shouldn\'t talk.',
        'Your hair wants cutting',
        'Not all who wander are lost.',
        'I am not crazy; my reality is just different from yours.',
    ]
    return random.choice(quotes)


def replace_template_variables(content: str, variables: dict):
    """Replaces each variable in the content string with its corresponding value.

    Each variable in the content is identified by the following pattern:
    ```text
    ${...}
    ```

    If a variable doesn't have a corresponding value, or if the provided value is None, then a ValueError is raised.
    """
    for key in variables:
        value = variables[key]
        regex = '\\$\\{{{}\\}}'.format(key)
        content = re.sub(regex, value, content)

    return content


def main(options, logger, console):
    # Read template
    with open(options.file, 'r') as fin:
        data = fin.read()

    vars = {f: None for f in re.findall(r'\$\{([a-zA-Z0-9_-]+)\}', data)}

    if options.template:
        for key, value in options.template:
            if key not in vars:
                logger.warning(f'The provided variable ({key}) is not a template variable.')
            else:
                vars[key] = value

    # Interactive
    if options.interactive:
        for key in vars:
            if vars[key] is None:
                vars[key] = input(f'{key}=')

    # Make sure no variable is unset
    unset = list(filter(lambda k: vars[k] is None, vars))
    if len(unset) > 0:
        str_unset = ", ".join(unset)
        logger.error(f'The following template variable are not set: {str_unset}')
        exit(1)

    data = replace_template_variables(data, vars)

    # Generate output file
    with open(options.out, 'w+') as fout:
        fout.write(data)


if __name__ == "__main__":
    try:
        # Command line arguments
        options = get_options()

        console = Console()
        logger = Logger(console, options.verbosity, options.quiet)

        logger.info(get_quote())
        main(options, logger, console)
    except KeyboardInterrupt:
        logger.info('Terminating script...')
        raise SystemExit
