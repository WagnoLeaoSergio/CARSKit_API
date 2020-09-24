![PyPI](https://img.shields.io/pypi/v/carskit-api)

# CARSKit-API

CARSKit-API is a software based on a command line interface that serves as an abstraction layer for the [CARSKit](https://github.com/irecsys/CARSKit) recommendation system engine. Built entirely in python, it aims to provide both a more dynamic and secure way of handling the input and output of engine data.

## Requirements

It is necessary that both python and java are installed on the computer to run the software.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install carskit-api
```

## Usage

First, it is necessary to create a folder for the rating data that will be used.

```shell
$ mkdir data
```

Remember that the data must be in the same format that the engine requires. If in doubt, look in the [User Guide](https://arxiv.org/abs/1511.03780).

With the folder created, enter it and create another one for the results that the engine will generate and insert the data set that will be used.

```shell
$ cd data
$ mkdir results
$ paste ratings.csv
```

Now we need to specify both the data set path and the results folder name for the API.

```shell
$ capi settings --set "dataset_path" --value ./ratings.csv
$ capi settings --set "results_fodername" --value "results"
```

You can use the command `capi -h` to know more about the api's commands.

By now, it is assumed that we have everything to run the the engine. You do that using the following command:

```shell
$ capi run
```

After executing the command, two new json files will be created in the same directory where the data set is, one of them is a statistics file that the engine extracted from the data set and the other is a recommendations file where, for each user of the data set, the top N items recommended for the same, in each possible combination of context (if specified), will be listed.

To change a specific configuration of the engine, the top N recommendations as example, we just need to use the following command:

```shell
$ capi settings -s "topN" --value 10
```

And a new settings file will be generated with the new configuration.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
