# VideoToAriticles

This project is based on the ideas from the blog [An attempt to solve the LLM challenge by @karpathy](https://twitter.com/MisbahSy/status/1763639317270786531) and attempts to implement the VideoToArticles functionality.

Currently, progress is made on VideoToArticleWithNoImage, with the image insertion feature under development.

## How To Run

Set your OpenAI Key in the `.env` file, and be sure choose the model which support long-context, otherwise the it will failed.

Based on your device, setting the env blew:
- device: cuda or cpu or mps
- whisper_model: 
    - `tiny`	39 M	tiny.en	tiny	~1 GB	~32x
    - `base`	74 M	base.en	base	~1 GB	~16x
    - `small`	244 M	small.en	small	~2 GB	~6x
    - `medium`	769 M	medium.en	medium	~5 GB	~2x
    - `large`	1550 M	N/A	large	~10 GB	1x

After you set your config, run the following command:
1. `pip install -r requirement.txt`
2. cd VideoToArticleWithNoImage
3. `python main.py`

## TODO

- [ ] Intergrate image in articles