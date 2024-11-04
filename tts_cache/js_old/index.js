
    <audio id="audioPlayer" controls style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
        <source src="audio/index.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const timings = {"id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178], "start_times": [0.0, 0.232, 0.337, 0.406, 0.778, 1.312, 1.451, 1.544, 1.997, 3.053, 3.344, 3.855, 4.354, 5.457, 5.724, 5.863, 5.956, 6.339, 6.838, 7.326, 7.546, 8.173, 8.313, 8.696, 9.265, 9.648, 9.81, 10.321, 11.505, 12.098, 12.516, 12.934, 13.375, 13.7, 15.801, 16.567, 18.936, 19.574, 19.806, 20.364, 20.921, 21.246, 21.513, 22.86, 23.069, 24.323, 24.462, 24.857, 25.472, 26.238, 26.459, 26.714, 28.154, 28.572, 29.141, 29.744, 30.046, 30.87, 31.079, 31.254, 31.637, 31.915, 32.287, 32.67, 33.483, 34.319, 34.887, 35.352, 35.77, 36.385, 36.78, 37.314, 37.918, 38.127, 39.508, 39.717, 41.168, 41.703, 42.062, 42.318, 42.62, 43.165, 43.49, 43.746, 44.083, 44.28, 44.907, 45.093, 45.278, 45.522, 45.789, 45.94, 46.73, 48.018, 48.262, 48.39, 48.471, 49.237, 49.597, 49.783, 49.888, 50.306, 50.793, 51.095, 51.223, 51.908, 53.301, 53.707, 54.346, 54.706, 54.961, 55.286, 55.913, 56.296, 56.517, 56.865, 57.585, 57.957, 58.479, 58.839, 59.141, 59.501, 60.116, 60.534, 61.521, 62.136, 62.856, 63.076, 63.169, 63.715, 63.959, 64.632, 65.178, 65.317, 65.747, 66.745, 66.989, 67.198, 67.314, 67.627, 68.568, 68.997, 69.311, 69.508, 70.216, 70.53, 71.691, 71.946, 72.376, 72.678, 73.305, 73.63, 74.442, 74.721, 75.383, 76.149, 76.881, 77.681, 78.308, 78.529, 79.655, 79.852, 79.934, 80.084, 80.166, 80.282, 80.479, 80.781, 80.955, 82.441, 82.639, 83.091, 84.531, 84.752, 85.216, 86.493, 86.714, 87.155]};

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
    