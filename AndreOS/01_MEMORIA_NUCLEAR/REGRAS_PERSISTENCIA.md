# Regras de persistência AndreOS

## 1. Fonte única de memória persistente

`C:\AndreOS-Memory` é o clone local da repo GitHub `AndreVazao/andreos-memory`.

## 2. Memória por projeto

Cada projeto deve ter uma pasta própria em:

`AndreOS/02_PROJETOS/<PROJETO>/`

Repos diferentes que pertencem ao mesmo produto/ecossistema podem partilhar uma única pasta de memória de projeto. A memória não precisa de seguir 1:1 a quantidade de repos.

## 3. Atualização obrigatória

Após uma alteração relevante de arquitetura, decisão, integração, correção ou estado do projeto:

- atualizar a memória;
- validar o conteúdo;
- fazer commit;
- fazer push.

## 4. Leitura antes de continuar

Quando uma sessão começa ou muda de computador/agente, a memória do projeto deve ser consultada antes de alterar código.

## 5. Segurança

Nunca guardar segredos, credenciais, tokens, cookies ou chaves privadas.

## 6. Recuperação

O antigo vault foi mantido fora da repo como arquivo de recuperação:

`C:\AndreOS-Memory-LEGACY-2026-10-07`

Não editar esse arquivo como fonte normal.
