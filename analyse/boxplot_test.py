from analyse.parselog import parse_log

import os
import datetime
import matplotlib.pyplot as plt


def draw(fp='./logs/PCL SZ/NL Amsterdam.log', title=''):
    data = parse_log(fp)

    # Sample
    # sampled_data = {}
    # for i in range(len(data.keys())):
    #     if i % 1 == 0:
    #         k = list(data.keys())[i]
    #         sampled_data[k] = data[k]
    # data = sampled_data

    all_data = [
        list(map(lambda x: x[1], v[16:]))
        for k, v in data.items()
    ]

    labels = [
        #datetime.datetime.utcfromtimestamp(int(int(k) / 1000)).strftime('%Y-%m-%d %H:%M:%S')
        datetime.datetime.utcfromtimestamp(int(int(k) / 1000)).strftime('%H:%M')
        for k, v in data.items()
    ]

    plt.figure(figsize=(25, 9))
    plt.boxplot(
        all_data,
        notch=True,
        labels=labels,
        patch_artist=True,
    )
    # plt.yscale('log', basey=2)
    plt.title(title)
    plt.xticks(rotation=60)
    plt.hlines(10, 0, len(labels), colors='k', linestyles='solid', label='10M', data=None)

    plt.savefig('images/%s.png' % title)
    plt.show()
    plt.close()


def main():
    iter_paths = os.walk('./logs')
    for iter_path in iter_paths:
        root, _, file_list = iter_path
        for file in file_list:
            if file.endswith('.log'):
                draw(
                    os.path.join(root, file),
                    'PCL SZ %s' % file
                )


if __name__ == '__main__':
    main()
