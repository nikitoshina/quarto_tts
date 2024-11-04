# Quarto TTS: Add Text-to-Speech to Your Quarto Projects

Try it out: https://nikitoshina.quarto.pub/quarto_tts/

Enhance your Quarto project with a text-to-speech (TTS) reader, just like the ones you find in Medium articles! This repository provides a filter that processes your markdown files, wraps strings in <span> tags with unique IDs, and uses the 11Labs API to convert the text into audio files. It then adds precise timestamps to your HTML pages alongside an audio player. The result is a fully functional screen reader for your markdown content—with complete control over the audio—that even works offline!

> Main benefit is that you can have full control over the audio, including what is being read, it what order, and how it is sematically broken up. In the future, I will make a code parser, so I can finally listen to code blocks without "opening bracket" and "closing bracket". 

Or you can use audio-native 11labs feature: https://elevenlabs.io/blog/audio-native

## Getting Started

1.	11Labs API Key: Ensure you have an 11Labs API key stored in your .env file or set as an environment variable `ELEVEN_LABS_API_KEY`.
2.	Use a Quarto Project: I recommend using a Quarto project for seamless integration.
3.	Code Blocks: By default, code blocks are not processed. If you need this feature, please submit an issue or create a pull request.
4.	Customization:
    -	Processing Logic: Modify `run_tts.py` to adjust how the Pandoc Abstract Syntax Tree (AST) is processed, allowing you to include or exclude specific elements.
    -	Audio Player Appearance: To change the look of the audio player, edit the template within `run_tts.py`.
5.	Pandoc Workflow Compatibility: With minor adjustments, you can adapt this tool to work with any Pandoc workflow.
6.	Dependencies: I’ve minimized dependencies—you only need to install panflute and have Python 3.10 or higher (it may work with earlier versions).

A working example is included in this repository.

## Installation

Get 11Labs API key: https://11labs.io/ and store it in your `.env` file.

Make sure you have Python 3.10 or higher installed and install the dependencies:

```
pip install panflute
```

To enable TTS functionality, add the following line to your `_quarto.yml` file:

```
add_tts: true
```

Additionally you can specify the voice_id from 11labs:

```
voice_id: 9Ft9sm9dzvprPILZmLJl
```

## Notes

1.	Development Iterations:

    -	Initially, a single Lua filter was considered, but it wasn’t feasible due to how Quarto and Pandoc handle Lua dependencies.
    -	The solution uses two filters: add_meta.lua to insert metadata and run_tts.py to perform TTS conversion and modify the AST.

2.	Caching Mechanism:

    -	Generating audio files can be resource-intensive and costly if done repeatedly. To address this, a caching system checks if the TSV files (which store IDs and words) have changed.
    -	If the files haven’t changed, the system uses previously generated audio files.
    -	To force a re-run, delete the corresponding old_tsv file or remove the entire tts_cache folder.
