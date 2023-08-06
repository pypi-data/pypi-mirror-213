//
// Created by jorge on 11/11/21.
//

#include <cmath>
#include "FileParsedData.h"
#include <bson.h>

FileParsedData::FileParsedData(const char *file, uint64_t start, uint64_t end, size_t samplesCount) {
    filePath =  file;
    start = start;
    end = end;
    samplesInFile = samplesCount;
    absPath = std::filesystem::absolute( filePath );
}
