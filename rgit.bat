@echo off
chcp 65001 > NULL

if "%~1" == "" GOTO HELP
if "%~1" == "save" GOTO SAVE
if "%~1" == "savemain" GOTO SAVEMAIN
if "%~1" == "push" GOTO PUSH
if "%~1" == "pull" GOTO PULL
if "%~1" == "revert" GOTO REVERT

echo unknown command
GOTO END

:SAVE
if "%~2" == "" GOTO NO_ARGUMENT
echo A salvar...
git add .
git commit -m "%~2"
GOTO END

:SAVEMAIN
echo A salvar para o main...
git checkout main
git merge rafa
git checkout rafa
GOTO END

:PULL
echo A atualizar o projeto...
git checkout main
git pull upstream main
git checkout rafa
git merge main
GOTO END

:PUSH
echo A atualizar a branch main
git checkout main
git push
git checkout rafa
GOTO END

:REVERT
echo A reverter...
if "%~2" == "" (git revert HEAD~1) else (git revert HEAD~%2)
GOTO END

:NO_ARGUMENT
echo Falta a mensagem...
GOTO END


:HELP
echo rgit save "[mensagem]" - Salva as alterações na branch de desenvolvimento local
echo rgit savemain - Salva as alterações na branch main local
echo rgit push - Atualiza a repo no github com a branch main local
echo rgit pull - Sincroniza com a branch main com o projeto principal
echo rgit status - Status dos ficheiros
echo rgit revert - Reverte a branch de desenvolvimento para o que esta no main
echo rgit revert HEAD~[numero] - Reverte para n commits antes (default=1)
GOTO END

:END

