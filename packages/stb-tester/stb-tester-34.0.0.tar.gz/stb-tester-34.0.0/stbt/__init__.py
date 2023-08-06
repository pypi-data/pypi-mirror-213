# coding:utf-8

"""Stb-tester Python API: Automated GUI Testing for Set-Top Boxes.

Copyright © 2013-2022 Stb-tester.com Ltd. All rights reserved.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Dict, Generator

import stbt_core  # open source APIs

# We need to import these explicitly so they show up in VSCode Intellisense:
from stbt_core import (
    android,
    apply_ocr_corrections,
    as_precondition,
    BGRDiff,
    Color,
    ConfigurationError,
    ConfirmMethod,
    crop,
    debug,
    detect_motion,
    Differ,
    Direction,
    draw_text,
    find_file,
    for_object_repository,
    Frame,
    FrameObject,
    frames,
    get_config,
    get_frame,
    GrayscaleDiff,
    Grid,
    Image,
    is_screen_black,
    Keyboard,
    Keypress,
    last_keypress,
    load_image,
    load_mask,
    Mask,
    MaskTypes,
    match,
    match_all,
    match_text,
    MatchMethod,
    MatchParameters,
    MatchResult,
    MatchTimeout,
    MotionResult,
    MotionTimeout,
    MultiPress,
    NoVideo,
    ocr,
    OcrEngine,
    OcrMode,
    Position,
    PreconditionError,
    press,
    press_and_wait,
    press_until_match,
    pressing,
    Region,
    save_frame,
    set_global_ocr_corrections,
    Size,
    TextMatchResult,
    TransitionStatus,
    UITestError,
    UITestFailure,
    wait_for_match,
    wait_for_motion,
    wait_for_transition_to_end,
    wait_until)

# The following APIs are not open source, and they require the Stb-tester Node
# hardware to run. This file contains stubs for local installation, to allow
# IDE linting & autocompletion.
__all__ = stbt_core.__all__ + [
    "audio_chunks",
    "AudioChunk",
    "BadSyncPattern",
    "color_diff",
    "detect_pages",
    "find_regions_by_color",
    "find_selection_from_background",
    "FIRST_FRAME_TIME",
    "get_rms_volume",
    "measure_av_sync",
    "play_audio_file",
    "prometheus",
    "RmsVolumeResult",
    "Roku",
    "segment",
    "stop_job",
    "TEST_PACK_ROOT",
    "VolumeChangeDirection",
    "VolumeChangeTimeout",
    "wait_for_volume_change",
]


from collections import namedtuple

import numpy
from enum import IntEnum
from _stbt.imgutils import _frame_repr

from . import prometheus


FIRST_FRAME_TIME = None
TEST_PACK_ROOT = None


# pylint: disable=redefined-outer-name,unused-argument,useless-return


def _raise_premium(api_name):
    raise NotImplementedError(
        "`stbt.%s` is a premium API only available to customers of "
        "Stb-tester.com Ltd. It requires *Stb-tester Node* hardware to run. "
        "See https://stb-tester.com for details on products and pricing. "
        "If you are receiving this error on the *Stb-tester Node* hardware "
        "contact support@stb-tester.com for help" % api_name)


class AudioChunk(numpy.ndarray):
    """A sequence of audio samples.

    An ``AudioChunk`` object is what you get from `audio_chunks`. It is a
    subclass of `numpy.ndarray`. An ``AudioChunk`` is a 1-D array containing
    audio samples in 32-bit floating point format (`numpy.float32`) between
    -1.0 and 1.0.

    In addition to the members inherited from `numpy.ndarray`, ``AudioChunk``
    defines the following attributes:

    :ivar float time: The wall-clock time of the first audio sample in this
        chunk, as number of seconds since the unix epoch
        (1970-01-01T00:00:00Z). This is the same format used by the Python
        standard library function `time.time`.

    :ivar int rate: Number of samples per second. This will typically be 48000.

    :ivar float duration: The duration of this audio chunk in seconds.

    :ivar float end_time: ``time`` + ``duration``.

    ``AudioChunk`` supports slicing using Python's ``[x:y]`` syntax, so the
    above attributes will be updated appropriately on the returned slice.
    """
    def __new__(cls, array, dtype=None, order=None, time=None, rate=48000):
        _raise_premium("AudioChunk")

    def __array_finalize__(self, obj):
        if obj is not None:
            _raise_premium("AudioChunk")

    @property
    def time(self):
        _raise_premium("AudioChunk.time")
        return 0.

    @property
    def duration(self):
        _raise_premium("AudioChunk.duration")
        return 0.

    @property
    def rate(self):
        _raise_premium("AudioChunk.rate")
        return 0

    @property
    def end_time(self):
        _raise_premium("AudioChunk.end_time")
        return 0.


def audio_chunks(time_index=None, _dut=None):
    """Low-level API to get raw audio samples.

    ``audio_chunks`` returns an iterator of `AudioChunk` objects. Each one
    contains 100ms to 5s of mono audio samples (see `AudioChunk` for the data
    format).

    ``audio_chunks`` keeps a buffer of 10s of audio samples. ``time_index``
    allows the caller to access these old samples. If you read from the
    returned iterator too slowly you may miss some samples. The returned
    iterator will skip these old samples and silently re-sync you at -10s. You
    can detect this situation by comparing the ``.end_time`` of the previous
    chunk to the ``.time`` of the current one.

    :type time_index: int or float
    :param time_index:
        Time from which audio samples should be yielded.  This is an epoch time
        compatible with ``time.time()``. Defaults to the current time as given
        by ``time.time()``.

    :return: An iterator yielding `AudioChunk` objects
    :rtype: Iterator[AudioChunk]
    """
    _raise_premium("audio_chunks")
    return iter([AudioChunk((4800,), dtype=numpy.float32)])


def get_rms_volume(duration_secs=3, stream=None) -> "RmsVolumeResult":
    """Calculate the average `RMS`_ volume of the audio over the given duration.

    For example, to check that your mute button works::

        stbt.press('KEY_MUTE')
        time.sleep(1)  # <- give it some time to take effect
        assert get_rms_volume().amplitude < 0.001  # -60 dB

    :type duration_secs: int or float
    :param duration_secs: The window over which you should average, in seconds.
        Defaults to 3s in accordance with short-term loudness from the EBU TECH
        3341 specification.

    :type stream: Iterator[AudioChunk]
    :param stream: Audio stream to measure. Defaults to ``audio_chunks()``.

    :raises ZeroDivisionError: If ``duration_secs`` is shorter than one sample
        or ``stream`` contains no samples.

    :rtype: RmsVolumeResult

    .. _RMS: https://en.wikipedia.org/wiki/Root_mean_square
    """
    _raise_premium("get_rms_volume")
    return RmsVolumeResult(0.0, 0.0, 0.0)


class RmsVolumeResult(
        namedtuple('RmsVolumeResult', 'time duration_secs amplitude')):
    """The result from `get_rms_volume`.

    :ivar float amplitude: The `RMS`_ amplitude over the specified window. This
      is a value between 0.0 (absolute silence) and 1.0 (a full-range square
      wave).

    :ivar float time: The start of the window, as number of seconds since the
      unix epoch (1970-01-01T00:00Z). This is compatible with ``time.time()``
      and ``stbt.Frame.time``.

    :ivar int|float duration_secs: The window size in seconds, as given to
      `get_rms_volume`.
    """

    def dBov(self, noise_floor_amplitude=0.0003) -> float:
        """The RMS amplitude converted to `dBov`_.

        Decibels are a logarithmic measurement; human perception of loudness is
        also logarithmic, so decibels are a useful way to measure loudness.

        This is a value between -70 (silence, or near silence) and 0 (the
        loudest possible signal, a full-scale square wave).

        :param noise_floor_amplitude: This is used to avoid `ZeroDivisionError`
            exceptions. We consider 0 amplitude to be this non-zero value
            instead. It defaults to ~0.0003 (-70dBov).

        .. _dBov: https://en.wikipedia.org/wiki/DBFS
        """
        import math
        return 20 * math.log10(max(self.amplitude, noise_floor_amplitude))


class VolumeChangeDirection(IntEnum):
    LOUDER = 1
    QUIETER = -1

    # For nicer formatting of `wait_for_volume_change` signature in generated
    # API documentation:
    def __repr__(self):
        return str(self)


class VolumeChangeTimeout(AssertionError):
    pass


def wait_for_volume_change(
        direction=VolumeChangeDirection.LOUDER, stream=None,
        window_size_secs=0.400, threshold_db=10.,
        noise_floor_amplitude=0.0003, timeout_secs=10):

    """Wait for changes in the RMS audio volume.

    This can be used to listen for the start of content, or for bleeps and
    bloops when navigating the UI. It returns after the first significant
    volume change. This function tries hard to give accurate timestamps for
    when the volume changed. It works best for sudden changes like a beep.

    This function detects changes in volume using a rolling window. The RMS
    volume is calculated over a rolling window of size ``window_size_secs``.
    For every sample this function compares the RMS volume in the window
    preceeding the sample, to the RMS volume in the window following the
    sample. The ratio of the two volumes determines whether the volume change
    is significant or not.

    Example: Measure the latency of the mute button::

        keypress = stbt.press('KEY_MUTE')
        quiet = wait_for_volume_change(
            direction=VolumeChangeDirection.QUIETER,
            stream=audio_chunks(time_index=keypress.start_time))
        print "MUTE latency: %0.3f s" % (quiet.time - keypress.start_time)

    Example: Measure A/V sync between "beep.png" being displayed and a beep
    being heard::

        video = wait_for_match("beep.png")
        audio = wait_for_volume_change(
            stream=audio_chunks(time_index=video.time - 0.5),
            window_size_secs=0.01)
        print "a/v sync: %i ms" % (video.time - audio.time) * 1000

    :type direction: VolumeChangeDirection
    :param direction: Whether we should wait for the volume to increase or
        decrease. Defaults to ``VolumeChangeDirection.LOUDER``.

    :type stream: Iterator returned by `audio_chunks`
    :param stream: Audio stream to listen to. Defaults to `audio_chunks()`.
        Postcondition: the stream will be positioned at the time of the volume
        change.

    :type window_size_secs: int
    :param window_size_secs: The time over which the RMS volume should be
        averaged. Defaults to 0.4 (400ms) in accordance with momentary loudness
        from the EBU TECH 3341 specification. Decrease this if you want to
        detect bleeps shorter than 400ms duration.

    :type threshold_db: float
    :param threshold_db: This controls sensitivity to volume changes. A volume
        change is considered significant if the ratio between the volume before
        and the volume afterwards is greater than ``threshold_db``. With
        ``threshold_db=10`` (the default) and
        ``direction=VolumeChangeDirection.LOUDER`` the RMS volume must increase
        by 10 dB (a factor of 3.16 in amplitude). With
        ``direction=VolumeChangeDirection.QUIETER`` the RMS volume must fall by
        10 dB.

    :type noise_floor_amplitude: float
    :param noise_floor_amplitude: This is used to avoid `ZeroDivisionError`
        exceptions.  The change from an amplitude of 0 to 0.1 is ∞ dB.
        This isn't very practical to deal with so we consider 0 amplitude to be
        this non-zero value instead. It defaults to ~0.0003 (-70dBov). Increase
        this value if there is some sort of background noise that you want to
        ignore.

    :type timeout_secs: float
    :param timeout_secs: Timeout in seconds. If no significant volume change is
        found within this time, `VolumeChangeTimeout` will be raised and your
        test will fail.

    :raises VolumeChangeTimeout: If no volume change is detected before
        ``timeout_secs``.

    :returns:
        An object with the following attributes:

        * **direction** (`VolumeChangeDirection`) – This will be either
          ``VolumeChangeDirection.LOUDER`` or ``VolumeChangeDirection.QUIETER``
          as given to ``wait_for_volume_change``.
        * **rms_before** (`RmsVolumeResult`) – The RMS volume averaged over
          the window immediately before the volume change. Use
          ``result.rms_before.amplitude`` to get the RMS amplitude as a float.
        * **rms_after** (`RmsVolumeResult`) – The RMS volume averaged over
          the window immediately after the volume change.
        * **difference_db** (*float*) – Ratio between ``rms_after`` and
          ``rms_before``, in decibels.
        * **difference_amplitude** (*float*) – Absolute difference between the
          ``rms_after`` and ``rms_before``. This is a number in the range -1.0
          to +1.0.
        * **time** (*float*) – The time of the volume change, as number of
          seconds since the unix epoch (1970-01-01T00:00:00Z). This is the same
          format used by the Python standard library function ``time.time()``
          and ``stbt.Frame.time``.
        * **window_size_secs** (*float*) – The size of the window over which
          the volume was averaged, in seconds.
    """
    _raise_premium("wait_for_volume_change")
    return _VolumeChangeResult(VolumeChangeDirection.LOUDER,
                               RmsVolumeResult(0.0, 0.0, 0.0),
                               RmsVolumeResult(0.0, 0.0, 0.0),
                               0.0, 0.0, 0.0, 0.)


_VolumeChangeResult = namedtuple(
    '_VolumeChangeResult',
    "direction rms_before rms_after difference_db difference_amplitude time "
    "window_size_secs")


def play_audio_file(filename):
    """Play an audio file through the Stb-tester Node's "audio out" jack.

    Useful for testing integration of your device with Alexa or Google Home.

    :param str filename:
      The audio file to play (for example a WAV or MP3 file committed to
      your test-pack).

      Filenames should be relative paths. This uses the same path lookup
      algorithm as `stbt.load_image`.
    """
    _raise_premium("play_audio_file")
    return None


_AVSyncResult = namedtuple(
    "_AVSyncResult",
    "offset type time duration_secs rate drift drift_p_value samples "
    "undetectable acceptable")


def measure_av_sync(duration_secs=60, start_timeout_secs=10,
                    frames=None, audiostream=None):

    """
    Measures the offset between audio and video.

    This function requires a reference video to be played on the device under
    test.  The caller is responsible for playing this video.  This function will
    wait until a known A/V sync video is playing and then measure the A/V
    offset.  Typically an A/V sync test will look like this::

        play_av_sync_video()
        result = stbt.measure_av_sync()
        assert result.acceptable

    Where ``play_av_sync_video`` is a function implemented by you, specific to
    your device-under-test.

    ``measure_av_sync`` supports the following reference videos:

    * `Apple HTTP Live Streaming Examples <https://developer.apple.com/streaming/examples/>`__
        * `AppleBipBop16x9 <https://developer.apple.com/streaming/examples/basic-stream-osx-ios5.html>`__
        * `AppleBipBop4x3 <https://developer.apple.com/streaming/examples/basic-stream-osx-ios4-3.html>`__
        * `AppleBipBopAdvanced <https://developer.apple.com/streaming/examples/advanced-stream-fmp4.html>`__
    * Contact us for support for other reference videos.

    :type duration_secs: float
    :param duration_secs: Duration over which A/V sync measurements should be
        taken.  It is not an error if the video ends before `duration_secs`
        worth of samples has been collected.  In this case `measure_av_sync`
        will return with the samples it collected before the video ended.  You
        can check `result.duration_secs` to detect this situation.

    :type start_timeout_secs: float
    :param start_timeout_secs: Number of seconds to wait for the A/V sync
        video to start.  If a known video is not detected within this period
        this function will raise `stbt.BadSyncPattern`.

    :raises BadSyncPattern: Raised if we didn't recognise a playing A/V sync
        video within ``start_timeout_secs`` or if the detected video is paused.

    :rtype: AVSyncResult
    :return: Statistics regarding A/V sync.  See `AVSyncResult` for more
        details.
    """

    _raise_premium("measure_av_sync")

    return _AVSyncResult(
        0.0, "", 0.0, 0.0, 0.0, 0.0, 0.0,
        numpy.array([], dtype=[
            ('video_time', 'f8'),
            ('audio_time', 'f8'),
            ('video_rate', 'f4')]),
        False, False)


class BadSyncPattern(RuntimeError):
    pass


class FindSelectionFromBackgroundResult:
    def __init__(self, matched, region, mask_region, image, frame):
        self.matched = matched
        self.region = region
        self.mask_region = mask_region
        self.image = image
        self.frame = frame

    def __bool__(self):
        return self.matched

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        return (
            "FindSelectionFromBackgroundResult(matched=%r, region=%r, "
            "mask_region=%r, image=%s, frame=%s)" % (
                self.matched,
                self.region,
                self.mask_region,
                _frame_repr(self.image),
                _frame_repr(self.frame)))


def find_selection_from_background(
        image, max_size, min_size=None, frame=None, mask=Region.ALL,
        threshold=25, erode=True):

    """Checks whether ``frame`` matches ``image``, calculating the region
    where there are any differences. The region where ``frame`` doesn't match
    the image is assumed to be the selection. This allows us to simultaneously
    detect the presence of a screen (used to implement a `stbt.FrameObject`
    class's ``is_visible`` property) as well as finding the selection.

    For example, to find the selection of an on-screen keyboard, ``image``
    would be a screenshot of the keyboard without any selection. You may need
    to construct this screenshot artificially in an image editor by merging two
    different screenshots.

    Unlike `stbt.match`, ``image`` must be the same size as ``frame``.

    :param str|stbt.Image image:
      The background to match against. It can be the filename of a PNG file on
      disk, or an image previously loaded with `stbt.load_image`.

      If it has an alpha channel, any transparent pixels are masked out (that
      is, the alpha channel is ANDed with ``mask``). This image must be the
      same size as ``frame``.

    :param stbt.Size max_size:
      The maximum size ``(width, height)`` of the differing region. If the
      differences between ``image`` and ``frame`` are larger than this in
      either dimension, the function will return a falsey result.

    :param stbt.Size min_size:
      The minimum size ``(width, height)`` of the differing region (optional).
      If the differences between ``image`` and ``frame`` are smaller than this
      in either dimension, the function will return a falsey result.

    :param stbt.Frame frame:
      If this is specified it is used as the video frame to search in;
      otherwise a new frame is grabbed from the device-under-test. This is an
      image in OpenCV format (for example as returned by `stbt.frames` and
      `stbt.get_frame`).

    :param str|numpy.ndarray|Mask|Region mask:
      A `Region` or a mask that specifies which parts of the image to
      analyse. This accepts anything that can be converted to a Mask using
      `stbt.load_mask`. See :doc:`masks`.

    :type threshold: int
    :param threshold:
      Threshold for differences between ``image`` and ``frame`` for it to be
      considered a difference. This is a colour distance between pixels in
      ``image`` and ``frame``. 0 means the colours have to match exactly. 255
      would mean that even white (255, 255, 255) would match black (0, 0, 0).

    :param bool erode:
      By default we pass the thresholded differences through an erosion
      algorithm to remove noise or small anti-aliasing differences. If your
      selection is a single line less than 3 pixels wide, set this to False.

    :returns:
      An object that will evaluate to true if ``image`` and ``frame`` matched
      with a difference smaller than ``max_size``. The object has the following
      attributes:

      * **matched** (*bool*) – True if the image and the frame matched with a
        difference smaller than ``max_size``.
      * **region** (`stbt.Region`) – The bounding box that contains the
        selection (that is, the differences between ``image`` and ``frame``).
      * **mask_region** (`stbt.Region`) – The region of the frame that was
        analysed, as given in the function's ``mask`` parameter.
      * **image** (`stbt.Image`) – The reference image given to
        ``find_selection_from_background``.
      * **frame** (`stbt.Frame`) – The video-frame that was analysed.

    ``find_selection_from_background`` was added in v32.

    Changed in v33: ``mask`` accepts anything that can be converted to a Mask
    using `load_mask` (previously it only accepted a `Region`).
    """
    _raise_premium("find_selection_from_background")
    return FindSelectionFromBackgroundResult(True, Region.ALL, mask, image,
                                             frame)


def detect_pages(frame=None, candidates=None, test_pack_root=""):
    """Find Page Objects that match the given frame.

    This function tries each of the Page Objects defined in your test-pack
    (that is, subclasses of `stbt.FrameObject`) and returns an instance of
    each Page Object that is visible (according to the object's ``is_visible``
    property).

    This is a Python `generator`_ that yields 1 Page Object at a time. If your
    code only consumes the first object (like in the example below),
    ``detect_pages`` will try each Page Object class until it finds a match,
    yield it to your code, and then it won't waste time trying other Page
    Object classes::

        page = next(stbt.detect_pages())

    To get all the matching pages you can iterate like this::

        for page in stbt.detect_pages():
            print(type(page))

    Or create a list like this::

        pages = list(stbt.detect_pages())

    :param stbt.Frame frame:
        The video frame to process; if not specified, a new frame is grabbed
        from the device-under-test by calling `stbt.get_frame`.

    :param Sequence[Type[stbt.FrameObject]] candidates:
        The Page Object classes to try. Note that this is a list of the classes
        themselves, not instances of those classes. If ``candidates`` isn't
        specified, ``detect_pages`` will use static analysis to find all of the
        Page Objects defined in your test-pack.

    :param str test_pack_root:
        A subdirectory of your test-pack to search for Page Object definitions,
        used when ``candidates`` isn't specified. Defaults to the entire
        test-pack.

    :rtype: Iterator[stbt.FrameObject]
    :returns:
        An iterator of Page Object instances that match the given ``frame``.

    Added in v32.

    .. _generator: https://docs.python.org/3.10/tutorial/classes.html#generators
    """
    _raise_premium("detect_pages")
    return iter([FrameObject()])


def stop_job(reason=None):
    # type: (str) -> None

    """Stop this job after the current testcase exits.

    If you are running a job with multiple testcases, or a
    :ref:`soak-test <soak-testing>`, the job will stop when the current
    testcase exits. Any remaining testcases (that you specified when you
    started the job) will not be run.

    :param str reason: Optional message that will be logged.

    Added in v31.
    """
    _raise_premium("stop_job")


def color_diff(frame=None, *, background_color=None, foreground_color=None,
               threshold=0.05, erode=False):
    """Calculate euclidean color distance in a perceptually uniform colorspace.

    Calculates the distance of each pixel in ``frame`` against the color
    specified in ``background_color`` or ``foreground_color``. The output is
    a binary (black and white) image.

    :param stbt.Frame frame:
      The video frame to process.

    :param Color background_color:
      The color to diff against. Output pixels will be white where the color
      distance is greater than ``threshold``. Use this to remove a background
      of a particular color.

    :param Color foreground_color:
      The color to diff against. Output pixels will be white where the color
      distance is smaller than ``threshold``. Use this to find a foreground
      feature of a particular color, such as text or the selection/focus.

    :param float threshold:
      Binarization threshold in the range [0., 1.]. Foreground pixels will be
      set to white, background pixels to black. A value of 0.01 means a
      barely-noticeable difference to human perception. To disable binarization
      set ``threshold=None``; the output will be a grayscale image.

    :param bool erode:
      Run the thresholded differences through an erosion algorithm to remove
      noise or small differences (less than 3px).

    :rtype: numpy.ndarray
    :returns: Binary (black & white) image, or grayscale image if
      ``threshold=None``.

    Added in v33.
    """
    _raise_premium("color_diff")
    return numpy.array([], dtype=numpy.uint8)


def find_regions_by_color(
        color, *, frame=None, threshold=0.05, erode=False, mask=Region.ALL,
        min_size=(20, 20), max_size=None):
    """Find contiguous regions of a particular color.

    :param stbt.Frame frame: The video frame to process.
    :param Color color: See the ``foreground_color`` parameter of `color_diff`.
    :param float threshold: See `color_diff`.
    :param bool erode: See `color_diff`.
    :param str|numpy.ndarray|Mask|Region mask:
      A `Region` or a mask that specifies which parts of the image to analyse.
      This accepts anything that can be converted to a Mask using
      `stbt.load_mask`. See :doc:`masks`.
    :param Size min_size:
      Exclude regions that are smaller than this width or height.
    :param Size max_size:
      Exclude regions that are larger than this width or height.

    :rtype: list[stbt.Region]
    :returns: A list of `stbt.Region` instances.

    Added in v33.
    """
    _raise_premium("find_regions_by_color")
    return []


def segment(frame, *, region=Region.ALL, initial_direction=Direction.VERTICAL,
            steps=1, narrow=True, light_background=False):
    """Segment (partition) the image into a list of contiguous foreground
    regions.

    This uses an adaptive threshold algorithm to binarize the image into
    foreground vs. background pixels. For finer control, you can do the
    binarization yourself (for example with `stbt.color_diff`) and pass the
    binarized image to ``segment``.

    :param Frame frame:
      The video-frame or image to process.

    :param Region region:
      Only search in this region.

    :param Direction initial_direction:
      Start scanning in this direction (left-to-right or top-to-bottom).

    :param int steps:
      Do another segmentation within each region found in the previous step,
      altering direction between VERTICAL and HORIZONTAL each step. For
      example, the default values
      ``steps=1, initial_direction=stbt.Direction.VERTICAL`` will find lines of
      text; ``steps=2`` will recursively perform segmentation horizontally
      within each line to find each character in the line (assuming the
      characters don't overlap due to kerning; overlapping characters will be
      segmented as a single region).

    :param bool narrow:
      At the last step, narrow each region in the opposite direction. For
      example: if you are segmenting lines of text with
      ``steps=1, initial_direction=stbt.Direction.VERTICAL, narrow=False`` you
      will get regions with ``y`` & ``bottom`` matching the top & bottom of
      each line, but with ``x`` & ``right`` set to the left & right edges of
      the frame (0 and the frame's width, respectively). With ``narrow=True``,
      each region's ``x`` & ``right`` will be the leftmost / rightmost edge of
      the line.

    :param bool light_background:
      By default, the adaptive threshold algorithm assumes foreground pixels
      are light-coloured and background pixels are dark. Set
      ``light_background=True`` if foreground pixels are dark (for example
      black text on a light background).

    :rtype: list[stbt.Region]
    :returns: A list of `stbt.Region` instances.

    Added in v33.
    """
    _raise_premium("segment")
    return []


class Roku:
    """Helper for interacting with Roku devices over the network.

    This uses Roku's `External Control Protocol`_.

    To find the Roku's IP address and to enable the Roku's network control
    protocol see <https://stb-tester.com/kb/roku>.

    :param str address: IP address of the Roku.

    Or, use ``Roku.from_config()`` to create an instance using the address
    configured in the test-pack's configuration files.

    Added in v33.

    .. _External Control Protocol: https://developer.roku.com/en-gb/docs/developer-program/debugging/external-control-api.md
    """
    def __init__(self, address: str) -> None:
        _raise_premium("Roku")

    @staticmethod
    def from_config() -> "Roku":
        """Create a ``Roku`` instance from the test-packs's configuration files.

        Expects that the Roku's IP address is specified in
        ``device_under_test.ip_address``. This configuration belongs
        in your Stb-tester Node's `Node-specific configuration file`_. For
        example:

        config/test-farm/stb-tester-00044b80ebeb.conf::

            [device_under_test]
            device_type = roku
            ip_address = 192.168.1.7

        :raises ConfigurationError: If Roku IP address not configured.

        .. _Node-specific configuration file: https://stb-tester.com/manual/configuration#node-specific-config
        """
        _raise_premium("Roku")
        return Roku(get_config("device_under_test", "ip_address"))

    @contextmanager
    def save_logs(self, filename: str = "roku.log") \
            -> Generator[None, None, None]:
        """Stream logs from the Roku's `debug console`_ to ``filename``.

        This is a context manager. You can use it as a decorator on your
        test-case functions::

            import stbt
            roku = stbt.Roku.from_config()

            @roku.save_logs()
            def test_launching_my_roku_app():
                ...

        .. _debug console: https://developer.roku.com/en-gb/docs/developer-program/debugging/debugging-channels.md
        """
        _raise_premium("Roku")
        yield

    def query_apps(self) -> Dict[str, str]:
        """Returns a dict of ``application_id: name`` with all the apps
        installed on the Roku device.
        """
        _raise_premium("Roku")
        return {}

    def launch_app(self, id_or_name) -> None:
        """Launches the specified app. Accepts the app's ID or name.

        Use `Roku.query_apps` to find the IDs & names of the apps installed
        on the Roku.
        """
        _raise_premium("Roku")
