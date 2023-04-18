import splitter
import sender
import click
import json

VERSION = "0.1"


@click.command()
@click.option('-d', '--dependency', help='File containing dependencies, format=JSON')
@click.option('-o', '--output-xml', help='output.xml from previous test run')
@click.option('-t', '--timed-cluster-size', help='Size of the execution time clusters', default=5, show_default=True,
              type=int)
@click.option('-r', '--random-cluster-size', help='Size of the random clusters', default=5, show_default=True, type=int)
@click.option('-q', '--queue', help='Name of queue', default="probot_queue", show_default=True)
@click.option('-h', '--host', help='Name of host', default='localhost', show_default=True)
def main(dependency, output_xml, timed_cluster_size, random_cluster_size, queue, host):
    """
    Split and send clusters
    :param dependency: dependency.json
    :param output_xml: output.xml with execution times
    :param timed_cluster_size: maximum size of the timed clusters
    :param random_cluster_size: maximum size of the random clusters
    :param queue: queue name
    :param host: host
    :return:
    """
    # print(dependency)
    # print(output_xml)
    # print(timed_cluster_size)
    # print(random_cluster_size)
    # print(queue)
    # print(host)
    clusters = splitter.main(dependency, output_xml, timed_cluster_size, random_cluster_size)
    click.secho("Probot generated these clusters:", fg='cyan')
    count = 0
    for cluster in clusters:
        click.echo(cluster)
        count += 1
    click.secho(f"{count} cluster(s)", fg='yellow')

    sender_connection = sender.open_sending_connection(host)
    sender_channel = sender.open_sending_channel(queue, host)
    for item in clusters:
        sender.send_message(json.dumps(item), sender_channel, queue)
    sender_connection.close()


if __name__ == '__main__':
    click.echo(
        f"{click.style('Pr', fg='red')}"
        f"{click.style('ob', fg='magenta')}"
        f"{click.style('ot', fg='cyan')} "
        f"{click.style(f'VER. {VERSION}', fg='bright_green')}")
    click.secho("for Robot Framework (https://robotframework.org/)", fg='yellow')
    main()
