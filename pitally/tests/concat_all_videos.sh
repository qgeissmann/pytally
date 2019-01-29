#!/usr/bin/env bash

pitally-d94abf/2019-01-16T20:57:33(UTC)_pitally-d94abf_my-video/

echo 1 > '2019-01-16T20:57:33(UTC)_pitally-d94abf_my-video_1640x1232@25_00000.h264'


list all experiments
for ech expriment,
    try:
        find the seed (e.g. .*_00000-00012.h264)
        set the seed
    catch:
        find the seed '2019-01-16T20:57:33(UTC)_pitally-d94abf_my-video_1640x1232@25_00000.h264'
        rename the seed 00000.h264 => '.*_00000-00000.h264'
        set the seed
    retrive the second field of the seed as int and add one to it
    use this pattern to retreive the next video
    if nextvideo exist, pipe it directly to the seed and increment the second field of the seed

