python train_scgpt.py \
    --output_dir ../../models/ \
    --do_train --do_eval \
    --eval_data_file ../../data/scgpt/upf-scgpt.txt \
    --per_gpu_train_batch_size 1 \
    --num_train_epochs 3 --learning_rate 0.001 --overwrite_cache --use_tokenize \
    --train_data_file ../../data/scgpt/upf-scgpt.txt --overwrite_output_dir --no_cuda


    # python train_scgpt.py --output_dir=/Users/macbook_pro/Documents/GitHub/ChatBot/generation/model --model_type=gpt2 --model_name_or_path=/Users/macbook_pro/Documents/GitHub/ChatBot/generation/sc_gpt/checkpoint --do_train --per_gpu_train_batch_size 1 --num_train_epochs 5 --learning_rate 5e-5 --overwrite_cache --use_tokenize --train_data_file=../../data/scgpt/upf-scgpt.txt --overwrite_output_dir