
    <audio id="audioPlayer" controls style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
        <source src="audio/second_page.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const timings = {"id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72], "start_times": [0.0, 0.848, 1.207, 1.916, 2.183, 2.473, 2.577, 3.75, 5.19, 5.468, 5.851, 6.385, 6.583, 6.885, 7.082, 7.372, 8.034, 8.336, 8.44, 8.603, 8.87, 9.114, 10.031, 10.762, 11.413, 12.69, 13.793, 15.221, 15.488, 16.149, 16.672, 16.811, 16.916, 17.171, 17.276, 17.764, 17.926, 18.031, 18.298, 18.402, 18.495, 18.843, 19.308, 19.47, 19.702, 20.387, 20.62, 21.026, 21.119, 21.27, 22.175, 23.708, 23.987, 23.987, 24.59, 24.718, 24.846, 25.693, 26.471, 26.75, 26.75, 27.33, 27.481, 27.632, 28.445, 29.327, 29.606, 29.606, 30.233, 30.372, 30.5, 31.243]};

        const audio = document.getElementById('audioPlayer');
        const spans = timings.id.map(id => document.getElementById(`rd-${id}`)).filter(span => span !== null);

        function updateHighlight() {
            const currentTime = audio.currentTime;

            spans.forEach((span, index) => {
                if (!span) return;
                
                const startTime = timings.start_times[index];
                const endTime = index < spans.length - 1 ? timings.start_times[index + 1] : timings.start_times[index] + 1;

                if (currentTime >= startTime && currentTime < endTime) {
                    span.classList.add('highlight');
                    span.classList.remove('pre-highlight', 'post-highlight');
                } else if (currentTime >= startTime - 1 && currentTime < startTime) {
                    span.classList.add('pre-highlight');
                    span.classList.remove('highlight', 'post-highlight');
                } else if (currentTime >= endTime && currentTime < endTime + 1) {
                    span.classList.add('post-highlight');
                    span.classList.remove('highlight', 'pre-highlight');
                } else {
                    span.classList.remove('highlight', 'pre-highlight', 'post-highlight');
                }
            });
        }

        audio.addEventListener('timeupdate', updateHighlight);

        audio.addEventListener('seeked', () => {
            spans.forEach(span => {
                if (span) {
                    span.classList.remove('highlight', 'pre-highlight', 'post-highlight');
                }
            });
            updateHighlight();
        });
    });
    </script>
    <style>
    .highlight, .pre-highlight, .post-highlight {
        border-radius: 3px;
        transition: all 0.3s ease-in-out;
    }

    #audioPlayer {
        border-radius: 8px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 10px;
        margin: 10px;
        width: 300px;
    }

    .highlight {
        background-color: lightblue;
    }
    .pre-highlight, .post-highlight {
        background-color: lightgreen;
    }
    </style>
    