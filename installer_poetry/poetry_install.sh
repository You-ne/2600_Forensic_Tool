#!/usr/bin/env zsh

#curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 - --version=1.4.0


if [ -d "$HOME/.local/bin" ] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
	export PATH="$HOME/.local/bin:$PATH"
	echo 'PATH="$HOME/.local/bin:$PATH"' >> $HOME/.profile
fi
