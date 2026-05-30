# Roadmap: pysib — ACM TOMS Algorithm Paper

Target: ACM Transactions on Mathematical Software, Algorithm paper.  
Submission = PDF do artigo + ZIP do software (CALGO).

---

## 0. Estratégia editorial

O artigo deve ser estruturado como um **TOMS Algorithm paper**, não como manual de
usuário. A narrativa central deve deixar claras três contribuições:

1. **Pacote livre em Python para identificação polinomial clássica** — implementação
   aberta e integrada dos estimadores ARX, SM, IV, correlation, OE, ARMAX e BJ, com
   convenção comum de modelos.
2. **Núcleo de otimização especializado em C para PEM não linear** — otimizador
   desenhado especificamente para OE, ARMAX e BJ, com muitos passos pequenos,
   sensibilidades estruturadas, Gauss--Newton e LAPACK, viabilizado por implementação
   de baixo nível para reduzir overhead.
3. **Implementação aberta dos métodos filtrados / cost-function shaping** — integração
   em software livre dos métodos filtrados fundamentados nos artigos já publicados,
   aplicados aos estimadores não lineares.

Reprodutibilidade não deve ser apresentada como contribuição científica; deve ser
tratada como requisito transversal de conformidade com TOMS/CALGO. Todos os
resultados do artigo devem ter drivers e saídas esperadas no pacote submetido.

Estrutura do artigo (implementada):

1. Introduction (inclui related work)
2. Problem and Model Classes
3. Algorithms (Linear Estimators | Nonlinear PEM + Optimization Core | Filtered Continuation)
4. Software Organization
5. Numerical Results (Robustness under Noisy Data | Effect of Filtered Continuation)
6. Conclusion

---

## 1. Artigo (manuscript) — status

### 1.1 Concluído

- [x] Introdução — 5 parágrafos: contexto, lacuna, pysib, contribuições, organização
- [x] Conclusão — três contribuições, resultados principais, disponibilidade CALGO
- [x] Abstract alinhado com três contribuições
- [x] Seção Algorithms reestruturada com três subseções
- [x] Software Organization — Python/C, convenção unificada, article/manual boundary
- [x] Numerical Results — Robustness under Noisy Data (tabela + figura)
- [x] Numerical Results — Effect of Filtered Continuation (tabela + figura)
- [x] Removido `lstlisting` Python do artigo
- [x] Removido `listings` package não mais usado
- [x] Tabela de arquitetura alinhada com nomenclatura das seções
- [x] Related work integrado na Introduction
- [x] Estrutura de seções alinhada com guidelines TOMS Algorithm
- [x] Seção Exact Recovery substituída por parágrafo sobre testes unitários

### 1.2 Pendente (ajustes finos)

- [ ] Prefixar título com `Algorithm XXXX:` (número atribuído pela revista)
- [ ] Verificar se há URLs inline que devem migrar para `\cite{}`
- [ ] Adicionar entrada `.bib` apontando para versões futuras do software
- [ ] Adicionar `alt` descriptions às figuras (aviso acmart acessibilidade)

---

## 2. Experimentos — status

### 2.1 Concluído

- [x] `artigo/experiments/robustness_noisy_data.py` — simulação Monte Carlo
- [x] `artigo/experiments/robustness_noisy_data_plot.py` — análise e figuras
- [x] `artigo/experiments/robustness_noisy_data.npz` — dados salvos
- [x] `artigo/experiments/robustness_noisy_data_results.md` — tabela estatística
- [x] `artigo/experiments/robustness_noisy_data_parameters.pdf` — histogramas SM/OE
- [x] `artigo/experiments/filtered_continuation_oe.py` — simulação Monte Carlo
- [x] `artigo/experiments/filtered_continuation_oe_plot.py` — análise e figuras
- [x] `artigo/experiments/filtered_continuation_oe.npz` — dados salvos
- [x] `artigo/experiments/filtered_continuation_oe_results.md` — tabela estatística
- [x] `artigo/experiments/filtered_continuation_oe_errors.pdf` — histograma + boxplot

### 2.2 Pendente

- [ ] Salvar arquivos de saída esperada em `expected_output/` para validação CALGO

---

## 3. User Manual — status

- [x] `userManual/main.tex` — overview, instalação, API reference, exemplos
- [x] `userManual/main.pdf` compilado
- [x] API reference cobre todas as funções públicas
- [x] Instruções de instalação com dependências

---

## 4. Software (ZIP para CALGO) — pendente

### 4.1 Estrutura do ZIP (obrigatória pelo guideline)

```
userManual.pdf
userManual/        ← fonte LaTeX do manual
Python/            ← código fonte pysib
Doc/               ← LICENSE, README top-level
```

- [ ] Reorganizar repositório ou preparar script de empacotamento para gerar o ZIP com essa estrutura
- [ ] Remover do ZIP: `.git`, `.gitignore`, `.so` precompilados, `.o`, `.a`
- [ ] Drivers devem ter arquivo de **saída esperada** para comparação (`expected_output/`)
- [ ] Drivers não devem exigir input interativo (já atendido)

### 4.2 Código (pysib v1.0)

- [ ] Verificar que o pacote roda em **Linux** (além de macOS)
- [ ] Garantir que `make` (ou `cmake`) builda tudo de forma portável em Linux e macOS

---

## 5. Checklist final antes de submeter

- [ ] `make clean && make` no artigo: zero erros, zero warnings relevantes
- [ ] Todos os drivers rodam sem erro em Linux e macOS
- [ ] Saídas dos drivers batem com `expected_output/`
- [ ] ZIP tem a estrutura exata: `userManual.pdf`, `userManual/`, `Python/`, `Doc/`
- [ ] Nenhum arquivo precompilado no ZIP
- [ ] Gerar códigos CCS corretos em https://dl.acm.org/ccs/ccs.cfm
- [x] Preencher ORCID no ScholarOne
- [ ] Contato prévio com editor recomendado para Algorithm papers (Tim Hopkins — `T.R.Hopkins@kent.ac.uk`)
