ambiente
--------
$ conda create --name etilt36 python=3.6 -y
$ conda activate etilt36
$ conda deactivate
$ conda --version

habituales
----------
$ clear
$ tree -a -I ".git|__pycache__|.gitignore" -L 3 -D

probaré logoru
--------------
https://github.com/Delgan/loguru
https://loguru.readthedocs.io/en/stable/overview.html#installation
pip install loguru

(etilt36) ~/Documents/lab/ret-project/ret-git $ python
Python 3.6.12 |Anaconda, Inc.| (default, Sep  8 2020, 23:10:56)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from loguru import logger
>>> logger.debug("That's it, beautiful and simple logging!")
2021-02-15 10:08:59.409 | DEBUG    | __main__:<module>:1 - That's it, beautiful and simple logging!
>>>

things I've learnt
------------------
- buscar en github antes de hacer (python)
