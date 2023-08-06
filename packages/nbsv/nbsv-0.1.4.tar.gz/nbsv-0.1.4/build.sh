# Install the python. This will also build the TS package.
pip install -e '.[test, examples]'

# For classic notebook, you need to run:
jupyter nbextension install --py --overwrite --symlink --sys-prefix nbsv
jupyter nbextension enable --py --sys-prefix nbsv
# Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
# the `install` command every time that you rebuild your extension. For certain installations
# you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
# of those flags here.

# When developing your extensions, you need to manually enable your extensions with the
# notebook / lab frontend. For lab, this is done by the command:
jupyter labextension develop --overwrite .
yarn clean
yarn build