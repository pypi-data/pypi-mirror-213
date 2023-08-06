from llama import Type, Context, LLMEngine

import unittest

import llama


class TestParallel(unittest.TestCase):
    def test_parallel_complex(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptor(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        llm = LLMEngine(id="output_str")

        # future changes to remove this decorator
        @llm.parallel
        def circular_operation(descriptor: Descriptor) -> Descriptor:
            story = llm.add_model(input=descriptor, output_type=Story)
            descriptor = llm.add_model(input=story, output_type=Descriptor)
            return descriptor

        descriptors = [
            Descriptor(
                likes="llamas and other animals4c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals2b",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals3c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
        ]
        descriptors = [circular_operation(descriptor) for descriptor in descriptors]
        llama.run_all(descriptors)

    def test_parallel_simple(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptor(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        llm = LLMEngine(id="output_str")
        descriptors = [
            Descriptor(
                likes="llamas and other animals4c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals2b",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals3c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
        ]
        llm.add_data(
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky100",
            )
        )
        stories = [
            llm.add_model(input=descriptor, output_type=Story)
            for descriptor in descriptors
        ]
        llama.run_all(stories)

    def test_parallel_super_simple(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptor(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        llm = LLMEngine(id="output_str")
        descriptors = [
            Descriptor(
                likes="llamas and other animals4c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals2b",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals3c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
        ]
        llm.add_data(
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky100",
            )
        )
        stories = llm(descriptors, output_type=Story)
        print(stories)
