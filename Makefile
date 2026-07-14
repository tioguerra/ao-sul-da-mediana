PYTHON ?= python3
export MPLCONFIGDIR := $(CURDIR)/.cache/matplotlib

.PHONY: help setup static figures cultural-maps distances reproduce validate check clean

help:
	@echo "setup          instala as dependências"
	@echo "figures        regenera as quatro figuras bibliográficas"
	@echo "cultural-maps  regenera os mapas culturais sem chamadas de API"
	@echo "distances      recalcula distâncias e contribuições por item"
	@echo "reproduce      executa todas as reproduções offline"
	@echo "validate       valida estrutura, cobertura e ausência de segredos"
	@echo "check          compila, reproduz e valida"

setup:
	$(PYTHON) -m pip install -r requirements.txt

static:
	$(PYTHON) -m compileall -q artigo scripts

figures:
	$(PYTHON) artigo/gerar-graficos.py

cultural-maps:
	$(PYTHON) artigo/mapa-cultural/gerar-mapa-cultural.py
	$(PYTHON) artigo/mapa-cultural/gerar-mapa-cultural-com-maritaca.py
	$(PYTHON) artigo/mapa-cultural/gerar-mapa-cultural-llms-multicondicao.py
	$(PYTHON) artigo/mapa-cultural/gerar-cinco-figuras-llms.py

distances:
	$(PYTHON) artigo/mapa-cultural/analisar-distancias-resultados.py

reproduce: figures cultural-maps distances

validate:
	$(PYTHON) scripts/validate_project.py

check: static reproduce validate

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .cache

