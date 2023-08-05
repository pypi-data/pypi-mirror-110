*** Settings ***
Library     FTSASeleniumLibrary
Library     String
Library     OperatingSystem
Library     Collections
Variables   ../resources/locators.py

*** Variables ***
${HOST}             ${EMPTY}
${PORT}             ${EMPTY}
${GRID_NAME}        ${EMPTY}
${SELENIUM_NAME}    ${EMPTY}
${PERFIL}           ${EMPTY}

*** Keywords ***
Inicializo o servidor remoto
    ${server}               INIT REMOTE SERVER     browser=${project.get('prop','BROWSER')}
    ${HOST} =               GET FROM DICTIONARY    ${server}    host
    SET SUITE VARIABLE      ${HOST}
    ${PORT} =               GET FROM DICTIONARY    ${server}    port
    SET SUITE VARIABLE      ${PORT}
    ${GRID_NAME} =          GET FROM DICTIONARY    ${server}    grid_name
    SET SUITE VARIABLE      ${GRID_NAME}
    ${SELENIUM_NAME} =      GET FROM DICTIONARY    ${server}    selenium_name
    SET SUITE VARIABLE      ${SELENIUM_NAME}
    LOG TO CONSOLE          '${SELENIUM_NAME}' execution container initialized at http://${HOST}:${PORT}/wd/hub inside '${GRID_NAME}' network.

Finalizo o servidor remoto
    END REMOTE SERVER       selenium_name=${SELENIUM_NAME}  grid_name=${GRID_NAME}
    LOG TO CONSOLE          Sincronizando dados da execução...

Abro o navegador
    INIT RECORD TEST VIDEO  test_name=${TEST NAME}    selenium_name=${SELENIUM_NAME}  grid_name=${GRID_NAME}
    LOG TO CONSOLE          Gravador de vídeo inicializado\n
    OPEN BROWSER            ${project.get('prop','URL')}    ${project.get('prop','BROWSER')}
    ...                     remote_url=http://${HOST}:${PORT}/wd/hub

Fecho o navegador
    CLOSE ALL BROWSERS
    END RECORD TEST VIDEO

Sou um "${nome_perfil}"
    ${nome_perfil}          CONVERT TO LOWER CASE   ${nome_perfil}
    SET SUITE VARIABLE      ${PERFIL}               ${nome_perfil}
    ${botao_login_novamente_presente}  RUN KEYWORD AND RETURN STATUS    ELEMENT SHOULD BE VISIBLE   ${botao_login_novamente}
    RUN KEYWORD IF          ${botao_login_novamente_presente}           CLICK ELEMENT   ${botao_login_novamente}

Autenticar-se com
    [Arguments]   ${cpf}   ${senha}
    ELEMENT SHOULD BE VISIBLE   ${campo_usuario}
    INPUT TEXT                  ${campo_usuario}   ${cpf}
    ELEMENT SHOULD BE VISIBLE   ${campo_senha}
    INPUT TEXT                  ${campo_senha}     ${senha}
    ELEMENT SHOULD BE VISIBLE   ${botao_entrar}
    CLICK ELEMENT               ${botao_entrar}

Informo os dados de autenticação do usuário
    ${cpf}     Catenate   SEPARATOR=_   ${PERFIL}  cpf
    ${senha}   Catenate   SEPARATOR=_   ${PERFIL}  senha
    Autenticar-se com  ${project.get('prop', '${cpf}')}  ${project.get('prop', '${senha}')}

Informo dados inválidos nos campos de autenticação
    [Arguments]         ${cpf}   ${senha}
    Autenticar-se com   ${cpf}   ${senha}

Verifico que a autenticação foi realizada com sucesso
    PAGE SHOULD CONTAIN  Log In Successful

Verifico que a autenticação não foi realizada
    PAGE SHOULD CONTAIN  Usuário ou senha inválidos

Verifico que a o botão entrar não está habilitado
    ELEMENT SHOULD BE DISABLED   ${botao_entrar}
