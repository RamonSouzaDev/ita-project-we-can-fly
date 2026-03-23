#!/bin/bash
echo "Iniciando lavagem militar do histórico do Git..."
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch *.html *.doc *.pdf *.csv temp_output.txt DECLARAÇÃO_ASSINADA_RAMON.doc UK_Engineering_Council_Dossier.pdf 00_Intro_We_Can_Fly.pdf" \
  --prune-empty --tag-name-filter cat -- --all

echo "Forçando destruição de backups de commit..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "Sobrescrevendo o GitHub na nuvem..."
git push origin --force --all
echo "Limpeza TRL-9 completa!"
