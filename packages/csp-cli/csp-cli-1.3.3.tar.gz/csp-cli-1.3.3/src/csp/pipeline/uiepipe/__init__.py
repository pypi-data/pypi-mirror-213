#!/usr/bin/env python
# encoding: utf-8
from csp.pipeline.uiepipe.doccano import do_convert as doccano
from csp.pipeline.uiepipe.evaluate import do_eval as evaluate
from csp.pipeline.uiepipe.finetune import do_train as finetune
from csp.pipeline.uiepipe.predict import extract as spo
if __name__ == '__main__':
    print("start")
