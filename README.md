# Generating_YT_Video_Summary_and_Quiz_sessions_from_Transcripts
In this repo we aim to get a concise YouTube video summary, review it to determine whether it's worth watching, extract step-by-step guidance so you could easily follow along, and at the end, generate a quiz to test your understanding.

A lot of people use YouTube to learn new things. This shouldn't come as a surprise: YouTube has educational content on pretty much any topic, from academic subjects like math and programming to hands-on projects, tutorials, and preparation for professional certifications. But as a learning tool, YouTube isn't perfect. Some videos have too many ads and sponsorship interruptions, some are slowed down by non-essential information, while others require viewers to pause frequently just to follow the steps. Imagine if we could get a concise video summary, review it to determine whether it's worth watching, extract step-by-step guidance so you could easily follow along, and at the end, generate a quiz to test your understanding. Wouldn't that be awesome?

In this tutorial, we will build exactly that!

We will create a notebook, install libraries, and start experimenting. This notebook can be executed on cloud, i.e. Google Colab, SageMaker Studio Lab, etc.; or locally if you have sufficient CPU-GPU resources.
We will learn how to use open-source models from the Hugging Face Hub for inference. We will utilize pre-trained sequence-to-sequence models to summarize YouTube transcripts and translate them to a different language.
We will then experiment with ChatGPT APIs and leverage the ChatGPT APIs to generate a step-by-step guide from a YouTube video. Additionally, we will create a quiz to test your understanding of the material.
