@echo OFF
title FFMPEG Task: Demo
ffmpeg -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_on_network_error 1 -reconnect_on_http_error 1 -reconnect_delay_max 3 -i https://some-stream-url -t 3600 -c copy -bsf:a aac_adtstoasc "stream-output.mp4"