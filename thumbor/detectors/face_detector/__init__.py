#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.detectors.local_detector import CascadeLoaderDetector
from thumbor.point import FocalPoint
from thumbor.utils import logger

HAIR_OFFSET = 0.12


class Detector(CascadeLoaderDetector):
    def __init__(self, context, index, detectors):
        super().__init__(context, index, detectors)
        self.load_cascade_file(__file__, self.context.config.FACE_DETECTOR_CASCADE_FILE)

    def __add_hair_offset(self, top, height):
        top = max(0, top - height * HAIR_OFFSET)
        return top

    async def detect(self):
        try:
            features = self.get_features()
        except Exception as error:
            logger.exception(error)
            logger.warning("Error during face detection; skipping to next detector")
            return await self.next()  # pylint: disable=not-callable

        if features:
            for (left, top, width, height), _ in features:
                top = self.__add_hair_offset(top, height)
                self.context.request.focal_points.append(
                    FocalPoint.from_square(
                        left, top, width, height, origin="Face Detection"
                    )
                )
            return

        await self.next()  # pylint: disable=not-callable
