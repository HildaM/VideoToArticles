# VideoToAriticles

This project is based on the ideas from the blog [An attempt to solve the LLM challenge by @karpathy](https://twitter.com/MisbahSy/status/1763639317270786531) and attempts to implement the VideoToArticles functionality.

> Note: Progress is being made on VideoToArticleWithNoImage, with the image insertion feature currently in development.

## How To Run

Set your OpenAI Key in the `.env` file, and be sure choose the model which support long-context, otherwise the it will failed.

Based on your device, setting the env blew:
- device: `cuda` or `cpu`, Apple Sillcon please choose `mps`.
- whisper_model: 
    - `tiny`
    - `base`
    - `small`
    - `medium`
    - `large`
- LONG_CONTEXT_MODEL:
    - if True, it will choose a prompt that intergrate previous paragraph as a reference to generate the next paragraph. This will increase the contextual coherence of the generated paragraphs.
    - if False, it will choose a shorter prompt which saving token consumption
- ARTICLE_LANGUAGE:
    - `cn` or `en`. Based on your video language to choose prompt language

After you set your config, run the following command:
1. `pip install -r requirement.txt`
2. cd VideoToArticleWithNoImage
3. `python main.py`
4. Enter your local video file path

If the program runs smoothly, the final generated articles will be stored in the `result` folder.
The `temp` folder is used to store intermediate files during the program's execution, which can be deleted upon successful completion.

## TODO

- [ ] Intergrate image in articles