# Script Comparator — Guia de integração noutros projetos

Este documento é o checklist operacional para transformar o componente numa dependência de outro programa AndreOS.

## 1. Escolher o modo de integração

### Durante desenvolvimento
Copiar/vendorizar apenas src/script_comparator/.

### Entre vários repositórios
Usar uma dependência Git/submodule ou mecanismo equivalente, fixando uma versão/commit conhecido.

### Após release estável
Usar o pacote Python versionado.

## 2. Não copiar a GUI

O consumidor não precisa de:
- PyQt;
- ficheiros de interface;
- FastAPI;
- frontend;
- documentação interna;
- scripts de demonstração.

A dependência runtime é o pacote script_comparator.

## 3. Importar apenas a API pública

Usar imports a partir de script_comparator.

Não importar funções privadas de core.py. Se uma nova capacidade for necessária, ela deve ser promovida para a API pública através de alteração documentada e testada.

## 4. Fluxo mínimo recomendado

1. recolher caminhos dos ficheiros;
2. chamar group_files/analyze_files;
3. mostrar ao utilizador a análise e a base escolhida;
4. chamar consolidate_group ou consolidate_all;
5. verificar validated;
6. verificar conflicts;
7. apresentar warnings;
8. guardar/mostrar backup_dir;
9. registar o MergeResult no log do anfitrião.

## 5. Regra de aprovação

O anfitrião deve considerar a consolidação automática aprovada apenas quando:

- validated == True;
- conflicts está vazio;
- a operação corresponde ao grupo esperado;
- o utilizador ou política do anfitrião autorizou a mutação quando esta for destrutiva.

## 6. Migração do shim antigo

Se o projeto antigo usar:

    from MODULO_SCRIPT_COMPARATOR import consolidate_group

pode continuar temporariamente.

Depois deve migrar para:

    from script_comparator import consolidate_group

O shim pode ser removido do consumidor apenas depois de a nova importação estar validada.

## 7. Testes obrigatórios no consumidor

Antes de ativar a funcionalidade em produção, testar pelo menos:

- duas versões Python com função ausente numa delas;
- conflito Python na mesma função;
- JSON com chave ausente;
- JSON com valor divergente;
- extensões diferentes;
- ficheiro inválido;
- backup criado;
- nomes originais preservados;
- falha durante escrita/renomeação;
- operação sem conflitos;
- operação com conflitos bloqueada.

## 8. Versionamento

Quando este componente receber a primeira release estável, o consumidor deve fixar uma versão compatível em vez de acompanhar alterações arbitrárias de main.

Mudanças incompatíveis devem gerar nova versão major. Alterações compatíveis devem seguir semver.

## 9. Responsabilidades

### Biblioteca
- análise;
- agrupamento;
- merge;
- conflito;
- validação;
- backup;
- resultado estruturado.

### Projeto anfitrião
- UI;
- permissões;
- autenticação;
- logs;
- confirmação humana;
- seleção de ficheiros;
- política de automação;
- armazenamento dos relatórios.

## 10. Consumidores previstos

Primeiro candidato: script-reviewer-mobile.

Outros candidatos: Build Control Center, DGM-MAT e futuras ferramentas AndreOS onde comparação/consolidação de versões seja necessária.

A integração deve ser feita individualmente e testada antes de tornar o componente partilhado uma dependência transversal.
