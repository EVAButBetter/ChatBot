from intent_classification.intent_classification_model import IntentClassificationModel


GENERIC_DATASET_PATH = "./intent_classification/datasets/generic.yml"
DOMAIN_DATASET_PATH = "./datasets/domain.yml"
EMBEDDER_TRAIN_DATASET_PATH = "./intent_classification/datasets/glove.6B.100d.txt"

# **** BUILD GENERIC INTENT CLASSIFIER****#
print("#### TRAINING GENERIC INTENT CLASSIFIER ####\n")

intentClassModel = IntentClassificationModel(embedder_train_data_path=EMBEDDER_TRAIN_DATASET_PATH,
                                             domain_dataset_path=DOMAIN_DATASET_PATH)

text,labels = intentClassModel.load_data_generic(GENERIC_DATASET_PATH)

label_encoder_output="./intent_classification/utils/generic_label_encoder.pkl"
tokenizer_output = "./intent_classification/utils/generic_tokenizer.pkl"
model_output = "./intent_classification/models/generic_intent_classifier.h5"
accuracy_output = "./intent_classification/plots/generic_accuracy.png"
loss_output = "./intent_classification/plots/generic_loss.png"
intentClassModel.execute_train_pipeline(text, labels, label_encoder_output, tokenizer_output, accuracy_output,
                                        loss_output, model_output)

print("#### VALIDATING GENERIC INTENT CLASSIFIER ON DOMAIN / NOT-DOMAIN CLASSIFICATION ####\n")
intentClassModel.validate_generic_model(GENERIC_DATASET_PATH)


# **** BUILD DOMAIN INTENT CLASSIFIER ****#
print("#### TRAINING DOMAIN INTENT CLASSIFIER ####\n")

text,labels = intentClassModel.load_data_domain()

label_encoder_output="./intent_classification/utils/domain_label_encoder.pkl"
tokenizer_output = "./intent_classification/utils/domain_tokenizer.pkl"
model_output = "./intent_classification/models/domain_intent_classifier.h5"
accuracy_output = "./intent_classification/plots/domain_accuracy.png"
loss_output = "./intent_classification/plots/domain_loss.png"
intentClassModel.execute_train_pipeline(text, labels, label_encoder_output, tokenizer_output, accuracy_output,
                                        loss_output, model_output)

print("#### FINISHED BUILDING INTENT CLASSIFIERS ####")

#TODO: OTHER CLASSIFIERS