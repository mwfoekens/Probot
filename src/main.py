import sys

from pika.exceptions import AMQPConnectionError

import splitter
import sender
import click

VERSION = "0.9.1"


@click.command()
@click.option('-d', '--dependency', help='File containing dependencies, format=JSON')
@click.option('-o', '--output-xml', help='output.xml from previous test run')
@click.option('-t', '--timed-group-size', help='Size of the execution time groups', default=5, show_default=True,
              type=int)
@click.option('-r', '--random-group-size', help='Size of the random groups', default=5, show_default=True, type=int)
@click.option('-q', '--queue', help='Name of queue', default="probot_queue", show_default=True)
@click.option('-h', '--host', help='Name of host', default='localhost', show_default=True)
@click.option('-p', '--port', help='port of MQ', default=5672, show_default=True, type=int)
@click.option('-s', '--suites_location', help='Location of suites that need to be split up', required=True)
def main(dependency: str, output_xml: str, timed_group_size: int, random_group_size: int, queue: str, host: str,
         port: int, suites_location: str) -> None:
    """
    \b
    Split and send groups
    :param dependency:          dependency.json
    :param output_xml:          output.xml with execution times
    :param timed_group_size:    maximum size of the timed groups
    :param random_group_size:   maximum size of the random groups
    :param queue:               queue name
    :param host:                host name
    :param port:                Port number
    :param suites_location:     location of the suites that need to be split up
    :return:                    None
    """
    # print(dependency)
    # print(output_xml)
    # print(timed_group_size)
    # print(random_group_size)
    # print(queue)
    # print(host)
    # print(port)
    # print(suites_location)
    groups = splitter.main(dependency, output_xml, timed_group_size, random_group_size, suites_location)
    click.secho("Probot generated these groups:", fg='cyan')
    count = 0
    for group in groups:
        click.echo(group)
        count += 1
    click.secho(f"{count} group(s)", fg='yellow')

    try:
        sender.send_messages(host, port, queue, groups)
    except AMQPConnectionError as e:
        click.secho("Could not connect to queue.", err=True, fg="red")
        click.secho(f"Args: {e.args}", err=True, fg="red")
        sys.exit(1)

    click.secho("All groups sent. Exiting...", fg='cyan')
    sys.exit(0)


if __name__ == '__main__':
    click.echo(
        f"{click.style('Pr', fg='red')}"
        f"{click.style('ob', fg='magenta')}"
        f"{click.style('ot', fg='cyan')} "
        f"{click.style(f'VER. {VERSION}', fg='bright_green')}")
    click.secho("for Robot Framework\t https://robotframework.org/", fg='yellow')
    click.secho("GitHub:\t\t\t https://github.com/mwfoekens/Probot", fg='blue')
    main()
