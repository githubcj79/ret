#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def main():
    file_path = 'config.yaml'
    dict_ = read_yaml(file_path)


if __name__ == '__main__':
    main()
