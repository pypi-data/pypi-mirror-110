# run-web-pycode

A simple package to execute remote python scripts

example:

``` bash
# run_web_pycode https://raw.githubusercontent.com/AngusWG/run-web-pycode/master/tests/a_script.py
pyw run https://raw.githubusercontent.com/AngusWG/run-web-pycode/master/tests/a_script.py

# set proxy
pyw set_proxy http https://127.0.0.1:9999
pyw set_proxy http # for unset

# get help
pyw --help
pyw run --help
pyw set_proxy --help
```

* pyw is simplified command as run_web_pycode

---

* [Black formatter](https://github.com/psf/black)

> This project use black, please set `Continuation indent` = 4  
> Pycharm - File - Settings - Editor - Code Style - Python - Tabs and Indents

* [Flake8 lint](https://github.com/PyCQA/flake8)

> Use flake8 to check your code style.

## Features

- [x] Run code by Url
- [x] A simple entry point `pyw`
- [x] Set proxy
- [ ] package to pypi
- [ ] Convert GitHub.com url to <raw.githubusercontent.com> file
