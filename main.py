from utils import loading_info, graph_working
import pandas as pd


def main():
    stations_list = pd.read_csv('stations.csv', sep=';')
    # print(stations_list['id'].to_dict())
    # print("id;railway;name;customhouse;x_coord;y_coord")
    # values = []
    # for station in loading_info.add_coords2stations(stations_list):
    #     values.append(';'.join(map(str, [station.id, station.railway, station.name, station.customhouse, station.x_coord, station.y_coord])))
    # values.sort(key=lambda x: int(x.split(';')[0]))
    # print('\n'.join(values))
    # return
    distro = graph_working.distribute_by_railway(stations_list)
    anses = []

    for key, stations in distro.items():

        # print(key)
        anses += graph_working.create_connections_for_one_railway(stations)

        # print(*item, sep=';')
    # print('first;second')
    # for i in anses:
    #     print(*i)
    graph_working.draw_graph(stations_list, anses)

    # res = loading_info.get_rw_urls()
    # print(len(res))
    # # res = res[:10]
    # rez = loading_info.get_stations_info(res)
    #
    # dop_anses = []
    # for station in rez:
    #
    #   dop_anses.append((station.name, station.id, station.railway, station.customhouse))


if __name__ == '__main__':
    main()