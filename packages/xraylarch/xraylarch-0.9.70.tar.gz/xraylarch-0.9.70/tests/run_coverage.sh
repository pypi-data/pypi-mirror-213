coverage erase

coverage run --source=larch -a test_basic_processing.py
coverage run --source=larch -a test_funccalls.py
coverage run --source=larch -a test_importlarch.py
coverage run --source=larch -a test_interpreter.py
coverage run --source=larch -a test_jsonutils.py
coverage run --source=larch -a test_larch_plugin.py
coverage run --source=larch -a test_larchexamples_basic.py
coverage run --source=larch -a test_larchexamples_xafs.py
coverage run --source=larch -a test_larchexamples_xray.py
coverage run --source=larch -a test_plugins_call.py
coverage run --source=larch -a test_read_xafsdata.py
coverage run --source=larch -a test_symbol_callbacks.py

coverage html
