//
// Created by Jorge Imperial-Sosa on 3/22/23.
//

#ifndef PYFTDC_BINARYBSON_H
#define PYFTDC_BINARYBSON_H

#include <cstdio>
#include <vector>
#include "ChunkMetric.h"

class BinaryBSON {

public:
    static const int BIN_BSON_MAX_SIZE = 1000000;

    BinaryBSON(const uint8_t *data, size_t size) {
        blob.reserve(size);
        blob.assign(data, data+size);
    }

    int unCompress();
    int parseUncompressedBinary();
    std::vector<std::string> getMetricsNames();
    ChunkMetric* getMetric(std::string name);
    ChunkMetric* getMetric(unsigned index);
    [[nodiscard]] size_t getSampleCount() const;

private:
    int UnpackVariableInts();


    std::vector<unsigned char> blob;
    std::vector<unsigned char> uncompressed;

    uint32_t metricCountFromHeader{};
    uint32_t deltaCountFromHeader{};
    std::vector<ChunkMetric*> metrics{};
};


#endif //PYFTDC_BINARYBSON_H
