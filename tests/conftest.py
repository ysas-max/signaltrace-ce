"""Configurações compartilhadas para a suíte de testes.

Este arquivo garante que o diretório raiz do projeto seja adicionado ao
``sys.path`` durante a execução dos testes, permitindo que os módulos
em ``src`` sejam importados corretamente.  Sem essa configuração, o
``pytest`` pode alterar o diretório de trabalho atual e impedir a
resolução do pacote ``src``.
"""

import sys
from pathlib import Path

# Configure a writable temporary directory for pytest fixtures.
#
# On some systems (e.g. certain Windows configurations) the default
# temporary directory used by pytest may be in a protected location
# (such as AppData\Local\Temp) and cause PermissionError: [WinError 5].
# To avoid this, we set the standard temporary environment variables to
# a directory inside the project root that we can always write to.
import os

tmp_base = Path(__file__).resolve().parents[1] / "tmp"
tmp_base.mkdir(exist_ok=True)
for var in ("TMPDIR", "TEMP", "TMP"):
    # Only override if not already defined to respect user settings
    if not os.environ.get(var):
        os.environ[var] = str(tmp_base)

# Adiciona o diretório raiz do repositório ao sys.path
root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))