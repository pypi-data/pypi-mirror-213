//
// Created by Jorge Imperial-Sosa on 3/21/23.
//
#ifndef PYFTDC_PARSERSTATE_H
#define PYFTDC_PARSERSTATE_H

#include <cstdint>
#include <string>
#include <vector>
#include "BinaryBSON.h"

static const int MAX_RECURSION = 100;
static const int MAX_METRICS = 256;

typedef struct struct_bson_type_metrics {
    uint64_t count{};
    std::string description;
} bson_type_metrics_t;

class ParserState {

public:
    ParserState();
    ~ParserState();

    [[nodiscard]] size_t getDepth() const;
    void incrementDepth();
    void decrementDepth();
    void incrementUTF8SizeTally(unsigned size);
    void incrementElementCount() { ++element_count; }
    void incrementKeySizeTally(size_t size);
    void pushBinaryBSON(const char *key, const uint8_t *data, size_t size);
    std::vector <BinaryBSON*> getBinBSONArray();
    void setMaxDocSize(size_t size);
    size_t getMaxDocSize() const;
    bson_type_metrics_t bson_type_metrics[MAX_METRICS];
    int test_uncompress_parse();
    void IncrementDocCount();
    std::vector<std::string> getMetricNames();
    size_t getSamplesCount();
    void setMetaData(char *string);

    std::string getJSONMetadata();

private:
    size_t doc_count;
    size_t element_count;
    size_t doc_size_max;
    size_t key_size_tally;
    size_t utf8_size_tally;
    size_t depth;

    std::vector <BinaryBSON*> blobs;
    std::string jsonMetaData;
};



#endif //PYFTDC_PARSERSTATE_H
