# extract-keywords-from-youtube-videos
This project combines [youtube-dl](https://github.com/ytdl-org/youtube-dl), [whisper](https://github.com/openai/whisper), [LangChain](https://github.com/hwchase17/langchain) and [ChatGPT](https://chat.openai.com/) to extract keywords from YouTube videos. It was intented as a tool for [Lyon Data Science](https://www.youtube.com/@lyondatascience/videos) to better reference its videos.

## Setup
To build the docker image, run the following command:
```bash
docker build -t extract-keywords-from-youtube-videos .
```

Now you can run a container like this:
```bash
docker run -it --gpus all extract-keywords-from-youtube-videos
```

**Note:** It is better to have a GPU to run this project as `whisper` will run faster. I suppose it could work on CPU but it would be very slow and I did not test it.

## Usage
### Set OpenAI API Key
As ChatGPT is used, you need to enter a valid OpenAI API key. You can get one [here](https://platform.openai.com/). Then, run the following command:
```bash
cp .env.template .env
```

And write your API key in the `.env` file.

### Run the pipeline
This project uses [DVC](https://dvc.org/) to orchestrate the pipeline. At any point, run `dvc status` to see the status of the pipeline.

You can see and edit the list of videos to process in `dvc.yaml`. For example:
```yaml
vars:
  - videos:
    - name: Où va la Data Science ?
      url: https://www.youtube.com/watch?v=bONAu-W44b8
    - name: Techniques pour améliorer son éligibilité pour travailler dans la data
      url: https://www.youtube.com/watch?v=N-7zRvzRr0I
    - name: Le long parcours d'un cas d'usage applicatif en NLP, de 2013 à 2022
      url: https://www.youtube.com/watch?v=Ki0pKl3TwdU
```

To run the pipeline, run `dvc repro`.

**Warning:** Be careful when running the pipeline as it will use ChatGPT which will cost you money. When possible, try to retrieve the results from the cache using `dvc pull` and `dvc checkout`.

**Note:** For now there is no DVC remote which means that your cache is only stored locally and there is no way to `dvc push/pull` it to synchronize with others. However you can already look at the results in the `data` folder. In the future, I will add a DVC remote on Google Drive to store the cache, in particular the audio files extracted from the videos (which would be too heavy to store with Git).
