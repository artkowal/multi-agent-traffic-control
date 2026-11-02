# multi-agent-traffic-control

System wieloagentowy do monitorowania ruchu ulicznego w Tarnowie: wykrywanie i prognozowanie korków, adaptacyjne sterowanie sygnalizacją, trasy alternatywne i ostrzeżenia.

## Dokumentacja

- [Architektura, dane wejściowe i wyjściowe, proaktywność](docs/architektura.md) ([PDF](docs/architektura.pdf))

## Struktura repozytorium

```
multi-agent-traffic-control/
├── docs/                 # dokumentacja (.md + wygenerowane PDF, diagramy)
├── sumo/
│   ├── network/          # mapa Tarnowa (OSM → .net.xml)
│   └── scenarios/        # scenariusze testowe (.sumocfg, trasy, zdarzenia)
├── src/
│   ├── agents/           # agenci fazy 1 (SPADE)
│   ├── llm/              # agenci i narzędzia fazy 2
│   ├── sim/              # połączenie z SUMO (TraCI)
│   └── common/           # komunikaty, konfiguracja, wspólne typy
├── dashboard/            # panel operatora
├── data/                 # dane zewnętrzne (MPK, GPR, pomiary)
├── experiments/          # wyniki uruchomień i porównania KPI
└── tests/
```
