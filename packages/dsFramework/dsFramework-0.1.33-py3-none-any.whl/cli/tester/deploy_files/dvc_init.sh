dvc init
dvc config core.analytics false
dvc remote add --default ds-ml-artifacts gs://dozi-stg-ds-apps-1-ds-apps-ds-ml-artifacts/{name-your-artifacts}
dvc remote modify ds-ml-artifacts projectname dozi-stg-ds-apps-1

dvc add --recursive pipeline/artifacts
# add your artifacts
git add pipeline/artifacts/models/full_bert_ner_with_text_model_150k.sav.dvc pipeline/artifacts/models/full_bert_ner_state_dict_150k_cpu.dict.dvc pipeline/artifacts/vocabs/buzzwords.json.dvc pipeline/artifacts/models/full_bert_ner_state_dict_150k.dict.dvc pipeline/artifacts/models/full_bert_ner_with_text_model_150k_cpu.sav.dvc pipeline/artifacts/vocabs/normalize.json.dvc pipeline/artifacts/vocabs/weighted_vocab.pkl.dvc
git commit -m "Add data and artifacts to DVC"
dvc push


