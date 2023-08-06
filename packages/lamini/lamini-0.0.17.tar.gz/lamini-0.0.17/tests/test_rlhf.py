from llama import Type, Context, LLMEngine

from llama.program.util.run_ai import query_get_models

import unittest
import time
import datetime


class Tweet(Type):
    tweet: str = Context("a viral tweet")
    likes: int = Context("likes the tweet gets")
    retweets: int = Context("retweets the tweet gets")


class User(Type):
    username: str = Context("A user's handle on twitter")


class TestRLHF(unittest.TestCase):
    def test_rlhf(self):
        llm = LLMEngine(id="tweets", model_name="hf-internal-testing/tiny-random-gpt2")

        llm.add_data(get_tweet_data()[:2])

        llm.improve(
            on="tweet",
            to="make it shorter",
            good_examples=[
                Tweet(
                    tweet="Solopreneurs, don't chase more clients - it's a beast that'll destroy you. ",
                    likes=45,
                    retweets=10,
                )
            ],
            bad_examples=[
                Tweet(
                    tweet="They tell you to chase more clients. If you're a Solopreneur providing a professional service, you're feeding a beast that will destroy you. Your goal is not MORE clients. Your goal is BETTER clients. 2-3 great clients could set you for life. I'll tell you why and what to do.",
                    likes=5,
                    retweets=1,
                )
            ],
        )

        start_time = datetime.datetime.now()

        job = llm.submit_job(
            input=User(username="lawrencekingyo"),
            output_type=Tweet,
            random=True,
            rlhf=True,
            generate_finetuning_data=True,
            replace_with_finetune_model=False,
        )

        print("Launched job", job)

        status = llm.check_job_status(job["job_id"])
        assert status["status"] not in ("NOT_SCHEDULED", "ERRORED")

        while status["status"] != "DONE":
            print(f"job not done. waiting... {status}")
            time.sleep(10)
            status = llm.check_job_status(job["job_id"])
            assert status["status"] not in ("NOT_SCHEDULED", "ERRORED")

        result = llm.get_job_results(job["job_id"], output_type=Tweet)
        print(result)

        trained_model = None

        while datetime.datetime.now() - start_time < datetime.timedelta(minutes=10):
            model = get_model(type_signature="tweetsUserTweet")

            if model is None:
                print(f"training job not done. waiting...")
                time.sleep(10)
                continue

            print("Checking model", model)

            if datetime.datetime.fromisoformat(model["creation_time"]) > start_time:
                trained_model = model
                break
            time.sleep(10)

        self.assertTrue(trained_model is not None)

        result = llm(
            input=User(username="lawrencekingyo"),
            output_type=Tweet,
            replace_with_finetune_model=True,
        )


def get_model(type_signature: str):
    models = query_get_models({"type_signature": type_signature})

    if len(models) > 0:
        return models[0]

    return None


def get_tweet_data():
    return [
        [
            User(username="syswarren"),
            Tweet(
                tweet="Tools aren't going to make you great designers. Your way of thinking, attention to detail, and ability to see the bigger picture will.",
                likes=1000,
                retweets=81,
            ),
        ],
        [
            User(username="TheJackForge"),
            Tweet(
                tweet="I don't like telling people how to live their lives, but you should probably learn how to use Figma.",
                likes=341,
                retweets=28,
            ),
        ],
        [
            User(username="iamharaldur"),
            Tweet(
                tweet="Remember when we had the mental energy to hate a new logo?",
                likes=1000,
                retweets=59,
            ),
        ],
        [
            User(username="lexfridman"),
            Tweet(
                tweet="ChatGPT puts a mirror to humanity.",
                likes=11100,
                retweets=874,
            ),
        ],
        [
            User(username="iamaaronwill"),
            Tweet(
                tweet="I had to make you uncomfortable otherwise you would never have moved. - The Universe",
                likes=4000,
                retweets=1000,
            ),
        ],
    ]
