def parse_log(fp):
    data = {}
    current_label = None
    with open(fp) as fi:
        for index, line in enumerate(fi):
            if '====' in line:
                current_label = None
                continue
            if not line:
                continue
            timestamp, speed, unit, window_speed, window_unit, blocks, percentage = line.split()
            speed = float(speed)
            window_speed = float(window_speed)
            if not current_label:
                current_label = timestamp
                data[current_label] = []
            if window_unit == 'B/s':
                window_speed *= 1 / 1024 / 1024
            if window_unit == 'KB/s':
                window_speed *= 1 / 1024
            if window_unit == 'MB/s':
                window_speed *= 1
            data[current_label].append((timestamp, window_speed))
    # print(data)
    return data


def main():
    parse_log('./logs/PCL SZ/AU Sydney.log')


if __name__ == '__main__':
    main()
