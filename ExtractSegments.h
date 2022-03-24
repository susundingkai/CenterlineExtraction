/**
 * @file ExtractSegments.h
 *
 * @brief This files declares functions to extract curvilinear segments from thinned binary images.
 *
 * @author Martin Wagner
 * Contact: mwagner9@wisc.edu
 *
 */

#pragma once

#include <vector>
#include "Structs.h"

std::vector<SSegment *> ExtractSegmentsV(unsigned char* data, int width, int height);
