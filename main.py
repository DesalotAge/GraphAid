from utils import loading_info, graph_working
import pandas as pd


def main():
    stations_list = pd.read_csv('stations.csv', sep=';')
    # print(stations_list['id'].to_dict())
    print("id;railway;name;customhouse;x_coord;y_coord")
    # for i in range(len(stations_list)):
    #     print(i, stations_list.railway[i], stations_list.name[i], stations_list.customhouse[i], stations_list.x_coord[i], stations_list.y_coord[i], sep=';')
    # return
    # values = []
    # coords = dict()
    # for station in loading_info.add_coords2stations(stations_list):
    #
    #     if (station.x_coord, station.y_coord) not in coords:
    #         coords[(station.x_coord, station.y_coord)] = [station.id]
    #     else:
    #         coords[(station.x_coord, station.y_coord)] += [station.id]
    #     values.append(';'.join(map(str, [station.id, station.railway, station.name, station.customhouse, station.x_coord, station.y_coord])))
    # values.sort(key=lambda x: int(x.split(';')[0]))
    # print('\n'.join(values))
    # for i in coords:
    #     print(i)
    # print(len(coords))
    # return
    values = dict()

    for i in range(len(stations_list.x_coord)):
        if (stations_list.x_coord[i], stations_list.y_coord[i]) not in values:
            values[(stations_list.x_coord[i], stations_list.y_coord[i])] = [stations_list.id[i]]
        else:
            values[(stations_list.x_coord[i], stations_list.y_coord[i])] += [stations_list.id[i]]
    all_ids = []
    for i in values.values():
        if len(i) > 10:
            continue
        all_ids += i[:1]
        # print(i[:1])
    # print(all_ids)
    print(len(values))
    # for i in range(len(all_ids)):
    #     print(i, stations_list.railway[all_ids[i]], stations_list.name[all_ids[i]], stations_list.customhouse[all_ids[i]], stations_list.x_coord[all_ids[i]], stations_list.y_coord[all_ids[i]], sep=';')
    # # return
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
    # 549, 694
    # РЕаЕТАУ, УЛ.ПУШКИНА, 21
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