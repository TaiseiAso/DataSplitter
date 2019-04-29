# coding: utf-8

"""テキストデータを学習用/検証用/評価用に分割する"""
__author__ = "Aso Taisei"
__version__ = "1.0.0"
__date__ = "27 Apr 2019"


# 必要なモジュールのインポート
import glob
import os
import yaml


def file_split(config):
    """
    テキストデータを学習用/検証用/評価用に分割
    @param config 設定ファイル情報
    """
    size_all = config['size']

    if size_all < 3:
        size_all = 3

    fn = config['filename']
    fn_train = fn['train'] + "_"
    fn_validate = fn['validate'] + "_"
    fn_test = fn['test'] + "_"

    ratio = config['ratio']
    train_ratio = ratio['train']
    validate_ratio = ratio['validate']
    test_ratio = ratio['test']

    if train_ratio < 0:
        train_ratio = 0
    if validate_ratio < 0:
        validate_ratio = 0
    if test_ratio < 0:
        test_ratio = 0

    all_ratio = train_ratio + validate_ratio + test_ratio

    blank_split = config['blank_split']

    if not os.path.isdir("data"):
        print("no data folder")
        return

    # splitedフォルダがなければ作成する
    if not os.path.isdir("splited"):
        os.mkdir("splited")

    # splitedフォルダ内のファイルをすべて削除
    for root, _, files in os.walk("splited", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

    files = glob.glob("data/*")

    if files == []:
        print("no data file")
        return

    for root, _, files in os.walk("data", topdown=False):
        for file in files:

            isDialog = False
            dialog = 0
            turn = 0

            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                line = f.readline()
                while line:
                    turn += 1
                    if blank_split and line == "\n":
                        isDialog = True
                        dialog += 1
                    line = f.readline()

            if isDialog:
                size_original = dialog
            else:
                size_original = turn

            if size_original < 2:
                print(file + ": Too small (data size < 2)")
                continue

            size_use = size_all
            if size_original < size_all:
                size_use = size_original

            if train_ratio == 0:
                size_train = 0
            else:
                size_train = max([1, int(train_ratio * size_use / all_ratio)])

            if validate_ratio == 0:
                size_validate = 0
            else:
                size_validate = max([1, int(validate_ratio * size_use / all_ratio)])

            if test_ratio == 0:
                size_test = 0
            else:
                size_test = size_use - size_train - size_validate

            size_list = [size_train, size_validate, size_test]

            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:

                for i, type in enumerate([fn_train, fn_validate, fn_test]):

                    if size_list[i] > 0:
                        cnt = 0

                        with open("splited/" + type + file, 'w', encoding='utf-8') as f_splited:
                            while True:
                                line = f.readline()
                                f_splited.write(line)

                                if not isDialog or line == "\n":
                                    cnt += 1

                                if cnt == size_list[i]:
                                    break

            print(file + ": " + str(size_original) + " -> " + str(size_use) + " -> " + str(size_train) + " / " + str(size_validate) + " / " + str(size_test))


if __name__ == '__main__':
    # 設定ファイルを読み込む
    config = yaml.load(stream=open("config/config.yml", 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)

    # 学習用/検証用/評価用に分割
    file_split(config)
