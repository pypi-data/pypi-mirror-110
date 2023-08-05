*** Settings ***
Documentation   UC000: Database
Default Tags    all   web   uc000   ct003   fb   database

Library     FTSADatabaseLibrary

*** Test Cases ***
CRUD da tabela Person no Banco de dados Oracle
    # ATENÇÃO: Antes de executar este caso de teste é necessário conectar à VPN do TJPB
    CONNECT TO DATABASE USING CUSTOM PARAMS    cx_Oracle
    ...     'CJO_TEST/Teste123#@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle-bd-teste.tjpb.jus.br)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=oracleteste.tjpb.jus.br)))'
    CREATE TABLE            person (id integer, first_name varchar(40), second_name varchar(40))
    INSERT                  person      (101, 'Joao', 'Goes')
    INSERT                  person      (102, 'Caio', 'Lima')
    UPDATE                  person      first_name='Jonas', second_name='Silva'       id=101
    LOG TO CONSOLE          person      first_name='Jonas'
    @{results}    SELECT    table_name=person
    FOR    ${item}    IN    @{results}
        LOG TO CONSOLE      ${item}
    END
    DELETE                  person      id=101
    DROP TABLE              person
    DISCONNECT FROM DATABASE
