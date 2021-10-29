import pandas as pd
import typing
import networkx as nx
import matplotlib.pyplot as plt
from utils.models import Station
from pyvis.network import Network


def distribute_by_railway(stations: pd.DataFrame) -> typing.Dict[str, list[Station]]:
    rez = dict()
    for i in range(len(stations)):
        station = Station(
            name=stations.at[i, 'name'],
            railway=stations.at[i, 'railway'],
            customhouse=stations.at[i, 'customhouse'],
            id=stations.at[i, 'id'],
            x_coord=stations.at[i, 'x_coord'],
            y_coord=stations.at[i, 'y_coord']
        )
        if 'None' in (stations.at[i, 'name'], stations.at[i, 'railway'],
                      stations.at[i, 'customhouse'], stations.at[i, 'id']):
            continue
        if stations.at[i, 'railway'] not in rez:
            rez[stations.at[i, 'railway']] = [station]
        else:
            rez[stations.at[i, 'railway']].append(station)
    return rez


def create_connections_for_one_railway(stations: list[Station]) -> list[tuple[int]]:
    connections = list()

    for first_station in range(len(stations)):
        shortest_length, id_of_closest_node = 10 ** 18, -1
        distanses = []
        for second_station in range(first_station + 1, len(stations)):

            cur_len = (stations[first_station].x_coord - stations[second_station].x_coord) ** 2 + \
                      (stations[first_station].y_coord - stations[second_station].y_coord) ** 2
            distanses.append((cur_len, second_station))

        distanses.sort()
        if len(distanses) > 0:
            connections.append((stations[first_station].id, stations[distanses[0][1]].id))
        # if len(distanses) > 1:
        #     dist_first_second = (stations[distanses[0][1]].x_coord - stations[distanses[1][1]].x_coord) ** 2 + \
        #                         (stations[distanses[0][1]].y_coord - stations[distanses[1][1]].y_coord) ** 2
        #     dist_main_second = (stations[first_station].x_coord - stations[distanses[1][1]].x_coord) ** 2 + \
        #                        (stations[first_station].y_coord - stations[distanses[1][1]].x_coord) ** 2
        #     if dist_main_second < dist_first_second:
        #         connections.append((stations[first_station].id, stations[distanses[1][1]].id))
    return connections


def draw_graph(all_stations: pd.DataFrame, edges: list[tuple[int]]) -> None:
    G = nx.Graph()
    print(all_stations.id)
    G.add_nodes_from(all_stations.id)
    nx.set_node_attributes(G, all_stations['name'].to_dict(), 'station_name')
    nx.set_node_attributes(G, all_stations['railway'].to_dict(), 'line_name')
    for edge in edges:
        print(edge)
        G.add_edge(*edge)
    # print(G.nodes)
    plt.figure(figsize=(10, 8))
    poses = {int(id): [float(y), float(x)] for id, x, y in all_stations[['id', 'x_coord', 'y_coord']].values }
    # print(poses)
    # print(nx.number_connected_components    (G))
    print(nx.get_node_attributes(G, 'station_name'))
    nx.draw(
        G,
        poses,
        width=0.5,
        node_size=10,
        # labels=nx.get_node_attributes(G, 'station_name'),
        # font_size=8
    )
    plt.show()
