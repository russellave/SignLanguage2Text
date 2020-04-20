import gpt_2_simple as gpt2
import os
import requests

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/
    
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')
single_text = gpt2.generate(sess,
              run_name='play',
              length=50,
              temperature=0.8,
              prefix="JULIET:\nwherefore art thou Romeo?\n\nROMEO:",
              nsamples=1,
              batch_size=1,
              return_as_list=True
              )[0]
print(single_text)