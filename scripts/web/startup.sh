#!/usr/bin/env bash

if [[ $WEBHOOK_URL != "" ]];
  then
    exec uvicorn src.main:create_app --port=8443 --host=0.0.0.0
  else
    exec python src/main_polling.py
fi;