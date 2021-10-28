from utils import loading_info


def main():
    res = loading_info.get_rw_urls()
    print(len(res))
    # res = res[:10]
    rez = loading_info.get_stations_info(res)

    dop_anses = []
    for station in rez:
        dop_anses.append((station.name, station.id, station.railway, station.customhouse))



if __name__ == '__main__':
    main()