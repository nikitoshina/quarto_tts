from panflute import *
import os
# TODO: add skip if it says not to process. Also what do I do if it is just pandoc?
def prepare(doc):
    doc.counter = 1
    doc.word_map = {'text': [], 'counter': []}


def action(elem, doc):
    # Check if we should skip processing
    # if 'html' not in str(doc.get_metadata().get('output_format', 'missing')):
    #     return
    if not doc.get_metadata().get('add_tts', False):
        return

    if isinstance(elem, Str) or isinstance(elem, Code): 
        span = Span(elem, identifier=f'rd-{doc.counter}')
        doc.word_map['text'].append(elem.text)
        doc.word_map['counter'].append(doc.counter)
        doc.counter += 1
        return span


def finalize(doc):
    # Check if we should skip processing
    # if 'html' not in str(doc.get_metadata().get('output_format', 'missing')):
    #     return
    if not doc.get_metadata().get('add_tts', False):
        return

    global word_map
    word_map = doc.word_map
    global quarto_doc_params
    quarto_doc_params = doc.get_metadata().get('quarto_doc_params', {})
    output_directory = quarto_doc_params.get('output_directory', '.')
    output_file = quarto_doc_params.get('output_file', 'index.html')
    voice_id = doc.get_metadata().get('voice_id', "9Ft9sm9dzvprPILZmLJl")

    # Ensure the tts_cache/tsv_new directory exists
    os.makedirs("tts_cache/tsv_new", exist_ok=True)
    with open("tts_cache/tsv_new/" + os.path.splitext(os.path.basename(output_file))[0] + ".tsv", 'w') as f:
        for i in range(len(word_map['text'])):
            f.write(f"{word_map['counter'][i]}\t{word_map['text'][i]}\n")

    # need to write tsv file

    js_content = process_file(output_file, output_directory, voice_id)
    doc.content.append(RawBlock(js_content, format='html'))


    del doc.counter
    del doc.word_map


def stop_if(elem):
    return (isinstance(elem, MetaValue) or 
    (hasattr(elem, 'identifier') and (
        elem.identifier == "quarto-navigation-envelope" 
        # TODO: TOC inherits from titles in quarto
        )))

def prepare_tts(tsv_path, audio_path, js_path, audio_output_path, voice_id="9Ft9sm9dzvprPILZmLJl"):
    import http.client
    import json
    import csv
    import base64
    import os
    # Get the API key.
    if "ELEVEN_LABS_API_KEY" in os.environ:
        xi_api_key = os.environ["ELEVEN_LABS_API_KEY"]
    else:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ELEVEN_LABS_API_KEY='):
                    xi_api_key = line.split('=')[1].strip()
                    break

    if not xi_api_key:
        raise ValueError("ELEVEN_LABS_API_KEY is empty in .env file")




    symbols = {
        "id": [],
        "characters": []
    }

    with open(tsv_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        # next(reader)  # Skip header row
        for row in reader:
            # Convert row[0] to int when adding to symbols
            length = len(row[1])
            symbols["id"].extend([int(row[0])] * length)
            symbols["characters"].extend(list(row[1]))
            symbols["id"].extend([0])
            symbols["characters"].extend([" "])


    # print(symbols)

    joined_symbols = "".join(symbols["characters"])
    # print(joined_symbols)
    #     # Configure the request
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"

    stability = 0.5
    similarity_boost = 0.4
    style = 0.3
    apply_text_normalization = "auto"

    payload = {
        "text": joined_symbols,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style
        },
        "apply_text_normalization": apply_text_normalization
    }


    headers = {
        "xi-api-key": xi_api_key,
        "Content-Type": "application/json"
    }

    # Prepare the connection and request
    conn = http.client.HTTPSConnection("api.elevenlabs.io")
    conn.request("POST", url, json.dumps(payload), headers)

    # Get the response
    response = conn.getresponse()
    response_utf8 = response.read().decode("utf-8")
    response_json = json.loads(response_utf8)
    # print(response_json)
    out = response_json['alignment']
    audio_bytes = base64.b64decode(response_json["audio_base64"])

    with open(audio_path, 'wb') as f:
        f.write(audio_bytes)

    # print(out)

    # test = out["characters"] == symbols["characters"]
    # print(test)

    symbols["start_times"] = out["character_start_times_seconds"]

    # now I need to combine everything back

    solution = {
        "id": [],
        "start_times": [],
    }

    for i in sorted(list(set(symbols["id"]))):
        if i == 0:
            continue
        else:
            solution["id"].append(i)
            mask = [x == i for x in symbols["id"]]
            current_starts = [t for t, m in zip(symbols["start_times"], mask) if m]
            solution["start_times"].append(current_starts[0])

    # print(solution)

    # Create HTML with audio and JavaScript
    js_content = f"""
    <audio id="audioPlayer" controls style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
        <source src="{audio_output_path}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        const timings = {json.dumps(solution)};

        const audio = document.getElementById('audioPlayer');
        const spans = timings.id.map(id => document.getElementById(`rd-${{id}}`)).filter(span => span !== null);

        function updateHighlight() {{
            const currentTime = audio.currentTime;

            spans.forEach((span, index) => {{
                if (!span) return;
                
                const startTime = timings.start_times[index];
                const endTime = index < spans.length - 1 ? timings.start_times[index + 1] : timings.start_times[index] + 1;

                if (currentTime >= startTime && currentTime < endTime) {{
                    span.classList.add('highlight');
                    span.classList.remove('pre-highlight', 'post-highlight');
                }} else if (currentTime >= startTime - 1 && currentTime < startTime) {{
                    span.classList.add('pre-highlight');
                    span.classList.remove('highlight', 'post-highlight');
                }} else if (currentTime >= endTime && currentTime < endTime + 1) {{
                    span.classList.add('post-highlight');
                    span.classList.remove('highlight', 'pre-highlight');
                }} else {{
                    span.classList.remove('highlight', 'pre-highlight', 'post-highlight');
                }}
            }});
        }}

        audio.addEventListener('timeupdate', updateHighlight);

        audio.addEventListener('seeked', () => {{
            spans.forEach(span => {{
                if (span) {{
                    span.classList.remove('highlight', 'pre-highlight', 'post-highlight');
                }}
            }});
            updateHighlight();
        }});
    }});
    </script>
    <style>
    .highlight, .pre-highlight, .post-highlight {{
        border-radius: 3px;
    }}

    .pre-highlight, .post-highlight {{
        transition: all 0.3s ease-out;
    }}

    #audioPlayer {{
        border-radius: 8px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 10px;
        margin: 10px;
        width: 300px;
    }}

    .highlight {{
        background-color: lightblue;
        transition: none;
    }}
    .pre-highlight, .post-highlight {{
        background-color: lightgreen;
    }}
    </style>
    """

    # Write the HTML to a file
    with open(js_path, 'w') as f:
        f.write(js_content)

    conn.close()


def process_file(output_file, output_dir, voice_id):
    import os
    from filecmp import cmp
    from shutil import copy2

    # output_file = "test.html"
    stump = os.path.splitext(os.path.basename(output_file))[0]
    if output_dir == ".": output_dir = "." 
    # output_dir = "."

    # I want to only process the files that have tsv files created (Those were selected by the user)

    new_tsv_path = "tts_cache/tsv_new/"
    old_tsv_path = "tts_cache/tsv_old/"
    old_tsv_file = old_tsv_path + stump + ".tsv"
    new_tsv_file = new_tsv_path + stump + ".tsv"
    os.makedirs(new_tsv_path, exist_ok=True)
    os.makedirs(old_tsv_path, exist_ok=True)
    new_audio_path = "tts_cache/audio/"
    old_audio_path = "tts_cache/audio_old/"
    new_audio_file = new_audio_path + stump + ".mp3"
    old_audio_file = old_audio_path + stump + ".mp3"
    os.makedirs(new_audio_path, exist_ok=True)
    os.makedirs(old_audio_path, exist_ok=True)
    new_js_path = "tts_cache/js/"
    old_js_path = "tts_cache/js_old/"
    new_js_file = new_js_path + stump + ".js"
    old_js_file = old_js_path + stump + ".js"
    os.makedirs(new_js_path, exist_ok=True) 
    os.makedirs(old_js_path, exist_ok=True)

    process_file = False

    if (os.path.exists(old_tsv_file) and 
        cmp(old_tsv_file, new_tsv_file) and 
        os.path.exists(old_audio_file) and 
        os.path.exists(old_js_file)):
            # Move old video and js to the new location
            # print("old file: ", old_tsv_file, "new file: ", new_tsv_file)
            if os.path.exists(old_audio_file):
                os.rename(old_audio_file, new_audio_file)
            if os.path.exists(old_js_file):
                os.rename(old_js_file, new_js_file)
    else:
        process_file = True





    new_audio_file = new_audio_path + stump + ".mp3"
    new_js_file = new_js_path + stump + ".js"
    audio_relative_path = os.path.join("audio", os.path.basename(new_audio_file))
    audio_output_path = os.path.join(output_dir, audio_relative_path)

    # Check if file needs processing by comparing with files_to_process
    if process_file:
        prepare_tts(new_tsv_file, new_audio_file, new_js_file, audio_relative_path, voice_id)

    # Ensure output audio directory exists and copy audio file for all included files
    os.makedirs(os.path.join(output_dir, "audio"), exist_ok=True)
    if os.path.exists(new_audio_file):
        copy2(new_audio_file, audio_output_path)

    # Append the content to included_files[i]
    # with open(output_file, 'a') as f:
    #     with open(new_js_file, 'r') as js_f:
    #         f.write(js_f.read())



    # Move new files to the old cache

    if os.path.exists(new_tsv_file):
        os.rename(new_tsv_file, old_tsv_file)

    if os.path.exists(new_audio_file):
        os.rename(new_audio_file, old_audio_file)

    with open(new_js_file, 'r') as js_f:
        js_content = js_f.read()
    if os.path.exists(new_js_file):
        os.rename(new_js_file, old_js_file)

    
    return js_content




def main(doc=None):
    global word_map
    word_map = {'text': [], 'counter': []}
    global quarto_doc_params

    out = run_filter(action, prepare=prepare, finalize=finalize, doc=doc, stop_if = stop_if) 


        
    return out


if __name__ == '__main__':
    main()