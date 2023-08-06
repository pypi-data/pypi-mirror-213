# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perceiver',
 'perceiver.data',
 'perceiver.data.audio',
 'perceiver.data.text',
 'perceiver.data.vision',
 'perceiver.model',
 'perceiver.model.audio',
 'perceiver.model.audio.symbolic',
 'perceiver.model.core',
 'perceiver.model.text',
 'perceiver.model.text.classifier',
 'perceiver.model.text.clm',
 'perceiver.model.text.common',
 'perceiver.model.text.mlm',
 'perceiver.model.vision',
 'perceiver.model.vision.image_classifier',
 'perceiver.model.vision.optical_flow',
 'perceiver.scripts',
 'perceiver.scripts.audio',
 'perceiver.scripts.text',
 'perceiver.scripts.vision']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1,<3.0',
 'einops>=0.4,<0.5',
 'fairscale>=0.4,<0.5',
 'fsspec[s3]',
 'jsonargparse[signatures]>=4.18,<5.0',
 'pytorch-lightning>=2.0,<3.0',
 'tensorboard>=2.11,<3.0',
 'torch-optimizer>=0.3,<0.4',
 'torch>=2.0,<3.0',
 'torchmetrics>=0.9,<0.10']

extras_require = \
{'audio': ['datasets>=2.4,<3.0',
           'transformers>=4.28,<5.0',
           'pretty_midi>=0.2.10,<0.3.0'],
 'text': ['datasets>=2.4,<3.0',
          'tokenizers>=0.12,<0.13',
          'transformers>=4.28,<5.0'],
 'vision': ['datasets>=2.4,<3.0',
            'torchvision>=0.15,<0.16',
            'opencv-python>=4.6.0.66,<5.0.0.0']}

setup_kwargs = {
    'name': 'perceiver-io',
    'version': '0.11.0',
    'description': 'Perceiver IO',
    'long_description': '# Perceiver, Perceiver IO and Perceiver AR\n\nThis repository is a PyTorch implementation of Perceiver, Perceiver IO and Perceiver AR, with PyTorch Lightning\ninterfaces for model training and Hugging Face 🤗 interfaces for inference.\n\n<table>\n  <tr>\n    <td>\n       <b>Perceiver</b>: General Perception with Iterative Attention\n       (<a href="https://arxiv.org/abs/2103.03206">paper</a>,\n        <a href="https://www.youtube.com/watch?v=P_xeshTnPZg">video</a>)\n    </td>\n    <td><img src="docs/images/small-perceiver.png" alt="Perceiver"/></td>\n  </tr>\n  <tr>\n    <td>\n      <b>Perceiver IO</b>: A General Architecture for Structured Inputs & Outputs\n      (<a href="https://arxiv.org/abs/2107.14795">paper</a>,\n       <a href="https://www.deepmind.com/blog/building-architectures-that-can-handle-the-worlds-data">blog post</a>)\n    </td>\n    <td><img src="docs/images/small-perceiver-io.png" alt="Perceiver IO"/></td>\n  </tr>\n  <tr>\n    <td>\n      General-purpose, long-context autoregressive modeling with <b>Perceiver AR</b>\n      (<a href="https://arxiv.org/abs/2202.07765">paper</a>,\n       <a href="https://www.deepmind.com/blog/perceiver-ar-general-purpose-long-context-autoregressive-generation">blog post</a>)\n    </td>\n    <td><img src="docs/images/small-perceiver-ar.png" alt="Perceiver AR"/></td>\n  </tr>\n</table>\n\n## Overview\n\nCore of the `perceiver-io` library are *backend models*, lightweight PyTorch implementations of Perceiver,\nPerceiver IO and Perceiver AR. They can be wrapped into [PyTorch Lightning](https://pytorch-lightning.readthedocs.io/en/stable/)\nmodules for training (*Lightning interface*) and 🤗 modules for inference (*Hugging Face interface*). See\n[library design](docs/library-design.md) for details.\n\n<p align="center">\n    <img src="docs/images/library-design-small.jpg" alt="library-design"/>\n</p>\n\nThe command line interface for training is implemented with [Lightning CLI](https://pytorch-lightning.readthedocs.io/en/stable/cli/lightning_cli.html).\nTraining datasets are 🤗 [datasets](https://huggingface.co/docs/datasets) wrapped into PyTorch Lightning data modules.\nFor NLP tasks, `perceiver-io` supports all 🤗 [fast tokenizers](https://huggingface.co/docs/transformers/fast_tokenizers)\nand the 🤗 Perceiver UTF-8 bytes tokenizer.\n\n## Documentation\n\n- [Installation](#installation)\n- [Getting started](#getting-started)\n- [Library design](docs/library-design.md)\n- [Pretrained models](docs/pretrained-models.md)\n- [Training examples](docs/training-examples.md)\n- [Inference examples](examples/inference.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krasserm/perceiver-io/blob/main/examples/inference.ipynb)\n- [Model construction](docs/model-construction.md)\n- [Building blocks](docs/building-blocks.md)\n\n## Installation\n\n### Via pip\n\n```shell\npip install perceiver-io[text,vision,audio]\n```\n\n### From sources\n\nInstallation from sources requires a [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and a\n[Poetry](https://python-poetry.org/docs/#installation) (1.2.0 or higher) installation.\n\nCreate and activate the `perceiver-io` conda environment:\n\n```shell\nconda env create -f environment.yml\nconda activate perceiver-io\n```\n\nInstall main and test dependencies, including all extras:\n\n```shell\n# Without dependencies required for examples\npoetry install --all-extras\n```\n\nIf you want to run the [examples](examples) locally, additionally use `--with examples`:\n\n```shell\npoetry install --all-extras --with examples\n```\n\n### Docker image\n\n```shell\ndocker pull ghcr.io/krasserm/perceiver-io:latest\n```\n\nSee [Docker image](docs/docker-image.md) for details.\n\n## Getting started\n\n### Inference\n\n#### Optical flow\n\nCompute the optical flow between consecutive frames of an input video and write the rendered results to an output\nvideo:\n\n```python\nfrom urllib.request import urlretrieve\nfrom transformers import pipeline\n\nfrom perceiver.data.vision import video_utils\nfrom perceiver.model.vision import optical_flow  # register auto-classes and pipeline\n\nurlretrieve(\n    url="https://martin-krasser.com/perceiver/flow/sintel_clip_cave_dragon_fight.mp4",\n    filename="sintel_clip_cave_dragon_fight.mp4",\n)\n\n# Create optical flow pipeline\noptical_flow_pipeline = pipeline("optical-flow", model="krasserm/perceiver-io-optical-flow", device="cuda:0")\n\n# load consecutive video frame pairs\nframe_pairs = video_utils.read_video_frame_pairs("sintel_clip_cave_dragon_fight.mp4")\n\n# create and render optical flow for all frame pairs\noptical_flows = optical_flow_pipeline(frame_pairs, render=True, device="cuda:0")\n\n# create video with rendered optical flows\nvideo_utils.write_video("sintel_clip_cave_dragon_fight_output.mp4", optical_flows, fps=24)\n```\n\nHere is a side-by-side comparison of the input and output video:\n\n<p align="center">\n    <img src="docs/images/optical-flow.gif" alt="optical-flow-sbs">\n</p>\n\n#### Symbolic audio generation\n\nCreate audio sequences by generating symbolic ([MIDI](https://en.wikipedia.org/wiki/MIDI)) audio data and converting the\ngenerated audio symbols into WAV output using [fluidsynth](https://www.fluidsynth.org/) (_Note:_ fluidsynth must be installed\nin order for the following example to work):  \n\n```python\nfrom transformers import pipeline\nfrom pretty_midi import PrettyMIDI\nfrom perceiver.model.audio import symbolic  # auto-class registration\n\nrepo_id = "krasserm/perceiver-ar-sam-giant-midi"\n\nprompt = PrettyMIDI("prompt.mid")\naudio_generator = pipeline("symbolic-audio-generation", model=repo_id)\n\noutput = audio_generator(prompt, max_new_tokens=64, num_latents=1, do_sample=True, top_p=0.95, temperature=1.0, render=True)\n\nwith open("generated_audio.wav", "wb") as f:\n    f.write(output["generated_audio_wav"])\n```\n\nExamples of generated audio sequences are available on the 🤗 [hub](https://huggingface.co/krasserm/perceiver-ar-sam-giant-midi#audio-samples).\n\nSee [inference examples](https://colab.research.google.com/github/krasserm/perceiver-io/blob/main/examples/inference.ipynb)\nfor more examples.\n\n### Training\n\nTrain a small Perceiver IO image classifier (907K parameters) on MNIST from the command line. The classifier\ncross-attends to individual pixels of input images with [repeated cross-attention](docs/building-blocks.md).\nSee [image classification](docs/training-examples.md#image-classification) training example for more details.\n\n```shell\npython -m perceiver.scripts.vision.image_classifier fit \\\n  --model.num_latents=32 \\\n  --model.num_latent_channels=128 \\\n  --model.encoder.num_frequency_bands=32 \\\n  --model.encoder.num_cross_attention_layers=2 \\\n  --model.encoder.num_self_attention_blocks=3 \\\n  --model.encoder.num_self_attention_layers_per_block=3 \\\n  --model.encoder.first_self_attention_block_shared=false \\\n  --model.encoder.dropout=0.1 \\\n  --model.encoder.init_scale=0.1 \\\n  --model.decoder.num_output_query_channels=128 \\\n  --model.decoder.dropout=0.1 \\\n  --model.decoder.init_scale=0.1 \\\n  --data=MNISTDataModule \\\n  --data.batch_size=64 \\\n  --optimizer=AdamW \\\n  --optimizer.lr=1e-3 \\\n  --lr_scheduler.warmup_steps=500 \\\n  --trainer.accelerator=gpu \\\n  --trainer.devices=1 \\\n  --trainer.max_epochs=30 \\\n  --trainer.logger=TensorBoardLogger \\\n  --trainer.logger.save_dir=logs \\\n  --trainer.logger.name=logs\n```\n\n[Model construction](docs/model-construction.md) describes how to implement model-specific command line interfaces\nwith the Lightning CLI. Training checkpoints are written to the `logs/img_clf/version_0/checkpoints` directory. Assuming\na checkpoint with filename `epoch=025-val_loss=0.065.ckpt` exists, it can be converted to a `perceiver-io` 🤗 model with\n\n```python\nfrom perceiver.model.vision.image_classifier import convert_mnist_classifier_checkpoint\n\nconvert_mnist_classifier_checkpoint(\n    save_dir="example/mnist-classifier",\n    ckpt_url="logs/img_clf/version_0/checkpoints/epoch=025-val_loss=0.065.ckpt",\n)\n```\n\nso that it can be used in a 🤗 image classification pipeline\n\n```python\nfrom datasets import load_dataset\nfrom transformers import pipeline\n\nmnist_dataset = load_dataset("mnist", split="test")[:9]\n\nimages = mnist_dataset["image"]\nlabels = mnist_dataset["label"]\n\nclassifier = pipeline("image-classification", model="example/mnist-classifier")\npredictions = [pred[0]["label"] for pred in classifier(images)]\n\nprint(f"Labels:      {labels}")\nprint(f"Predictions: {predictions}")\n```\n```\nLabels:      [7, 2, 1, 0, 4, 1, 4, 9, 5]\nPredictions: [7, 2, 1, 0, 4, 1, 4, 9, 5]\n```\n\nor loaded directly:\n\n```python\nimport torch\nfrom transformers import AutoModelForImageClassification, AutoImageProcessor\n\nmodel = AutoModelForImageClassification.from_pretrained("example/mnist-classifier")\nprocessor = AutoImageProcessor.from_pretrained("example/mnist-classifier")\n\ninputs = processor(images, return_tensors="pt")\n\nwith torch.no_grad():\n    # use perceiver-io Hugging Face model\n    output_1 = model(**inputs).logits\n\nwith torch.no_grad():\n    # or use perceiver-io backend model directly  \n    output_2 = model.backend_model(inputs.pixel_values)\n\nprint(f"Predictions: {output_1.argmax(dim=-1).numpy().tolist()}")\nprint(f"Predictions: {output_2.argmax(dim=-1).numpy().tolist()}")\n```\n```\nPredictions: [7, 2, 1, 0, 4, 1, 4, 9, 5]\nPredictions: [7, 2, 1, 0, 4, 1, 4, 9, 5]\n```\n\nSee [training examples](docs/training-examples.md) for more examples.\n\n## Articles\n\nArticles referencing this repository:\n\n- [Training compute-optimal Perceiver AR language models](https://krasserm.github.io/2023/01/23/scaling-perceiver-ar/)\n- [A gentle introduction to Rotary Position Embedding](https://krasserm.github.io/2022/12/13/rotary-position-embedding/)\n\n## Other implementations\n\n- [Perceiver](https://paperswithcode.com/paper/perceiver-general-perception-with-iterative#code)\n- [Perceiver IO](https://paperswithcode.com/paper/perceiver-io-a-general-architecture-for#code)\n- [Perceiver AR](https://paperswithcode.com/paper/general-purpose-long-context-autoregressive#code)\n',
    'author': 'Martin Krasser',
    'author_email': 'krasserm@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/krasserm/perceiver-io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
