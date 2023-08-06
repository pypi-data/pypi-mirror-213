//
// Created by Jorge Imperial-Sosa on 3/24/23.
//

#include <ParserState.h>

ParserState::ParserState()
{
    doc_count = 0;
    element_count = 0;
    doc_size_max = 0;
    key_size_tally = 0;
    utf8_size_tally = 0;
    depth = 0;
    bson_type_metrics[0] = {0, "End of document"};
    bson_type_metrics[1] = {0, "Floating point"};
    bson_type_metrics[2] = {0, "UTF-8 string"};
    bson_type_metrics[3] = {0, "Embedded document"};
    bson_type_metrics[4] = {0, "Array"};
    bson_type_metrics[5] = {0, "Undefined - Deprecated"};
    bson_type_metrics[6] = {0, "ObjectId"};
    bson_type_metrics[7] = {0, "Boolean"};
    bson_type_metrics[8] = {0, "Null value"};
    bson_type_metrics[9] = {0, "DBPointer - Deprecated"};
    bson_type_metrics[10] = {0, "JavaScript code"};
    bson_type_metrics[11] = {0, "Symbol - Deprecated"};
    bson_type_metrics[12] = {0, "JavaScript code w/ scope"};
    bson_type_metrics[13] = {0, "32-bit Integer"};
    bson_type_metrics[14] = {0, "Timestamp"};
    bson_type_metrics[15] = {0, "64-bit Integer"};
    bson_type_metrics[16] = {0, ""};
}

ParserState::~ParserState() {
    for(auto blob : blobs) delete blob;
}

void
ParserState::pushBinaryBSON(const char *key, const uint8_t *data, size_t size) {
    {
        auto blob = new BinaryBSON(data, size);
        blobs.push_back(blob);
    }
}

void
ParserState::IncrementDocCount() {
    ++doc_count;
}

void
ParserState::incrementDepth() {
    ++depth;
}

size_t
ParserState::getDepth() const {
    return depth;
}

size_t
ParserState::getMaxDocSize() const {
    return doc_size_max;
}

void
ParserState::decrementDepth() {
    --depth;
}

void
ParserState::incrementUTF8SizeTally(unsigned int size) {
    utf8_size_tally+=size;
}

void
ParserState::incrementKeySizeTally(size_t size) {
    key_size_tally+= size;
}

std::vector<BinaryBSON *>
ParserState::getBinBSONArray() {
    return blobs;
}

void
ParserState::setMaxDocSize(size_t size) {
    doc_size_max = size;
}

int
ParserState::test_uncompress_parse() {

    for (auto blob : blobs )
        if (0 == blob->unCompress())
            blob->parseUncompressedBinary();

    return 0;
}

std::vector<std::string>
ParserState::getMetricNames() {
    // TODO: Returning the names found in the first blob.
    //  We should verify that the metric names exist in all other.
    auto m = this->blobs[0]->getMetricsNames();
    return m;
}

size_t ParserState::getSamplesCount() {
    size_t size = 0;
    for (auto b : blobs) {
        size += b->getSampleCount();
    }
    return size;
}

void ParserState::setMetaData(char *md) {
    jsonMetaData = md;
}

std::string ParserState::getJSONMetadata() {
    return jsonMetaData;
}

