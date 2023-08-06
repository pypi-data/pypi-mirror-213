//
// Created by jorge on 12/16/20.
//
#include "include/Dataset.h"
#include "SampleLocation.h"
#include <spdlog/spdlog.h>
#include <fstream>
#include <zlib.h>


// For unit testing purposes.
// It creates one chunk with metrics from a CSV file.
Dataset::Dataset(const std::string& csvFileName)  :  metricNames(0)  {
    try {
        std::ifstream f;
        f.open(csvFileName, std::ios::in);
        std::string line;

        // TODO: The dataset only has one chunk for the moment, but it would be good to extend to multiple chunks.
        //auto *chunk = new Chunk();

        while (getline(f, line)) {

            // Trusty-old C tokenizer
            char *buffer = new char [ line.size() +1 ];
            strcpy(buffer, line.c_str());

            // Discard first token,which is only a sequential number.
            auto p = strtok(buffer, ";");

            // The metric name follows
            std::string thisMetricName(strtok(nullptr,";"));
            metricNames.emplace_back(thisMetricName);

            size_t count = 0;
            std::vector<uint64_t> metrics;
            do {
                if (!(p = strtok(nullptr, ";"))) break;

                metrics.emplace_back(atol(p));
                ++count;
            } while (true);

            // Add metric to chunk
            //chunk->AddMetric(thisMetricName, &metrics);

            delete [] buffer;
        }

        //TODO: fix
        //addChunk(chunk);
        f.close();
    }
    catch (const std::ifstream::failure& e) {
        spdlog::error(  "Exception opening/reading file");
    }

}

int
Dataset::getIndexInMetrics(const std::string & metric) {

    int index = 0;
    for (auto  m: *getMetricsNames()) {
        if (m == metric)
            return index;
        ++index;
    }

    return -1;
}

bool
Dataset::ConvertToRatedMetric(MetricsPtr metric) {

    bool goesNegative = false;

    auto it = metric->end();

    for (auto prev = it-1; it != metric->begin(); --it, --prev) {
        *it -= *prev;
        if (*it < 0) goesNegative = true;
    }

    // Or keep element, copying from 1st position.
    metric->at(0) = metric->at(1);

    return !goesNegative;
}

std::vector<MetricsPtr>
Dataset::getMetrics(const std::vector<std::string> metricNamesIn,
                    const size_t start, const size_t end,
                    const bool ratedMetrics) {

    std::vector<MetricsPtr> metricList;

    for(auto name : metricNamesIn) {
        auto element = getMetric(name, start, end, ratedMetrics);
        metricList.emplace_back(element);
    }

    return metricList;
}

MetricsPtr
Dataset::getMetricMatrix(const std::vector<std::string>& metricNamesToReturn, size_t *stride,
                         const Timestamp startLimit, const Timestamp endLimit, const bool ratedMetrics) {

    //  Get metrics
    auto mm = getMetrics(metricNamesToReturn, startLimit, endLimit, ratedMetrics);
    // get a length
    size_t len=0;
    for (auto m: mm) {
        if (m && m->size()>0) {
            len = m->size();

            if (stride)
                *stride = len;
            break;
        }
    }

    // Allocate
    auto p = new std::vector<uint64_t>;

    p->reserve(len * metricNamesToReturn.size());

    for (auto m: mm) {
        if (m)
            p->insert(p->end(), m->begin(),m->end());
        else
            p->insert(p->end(), len, 0);
    }

    return p;
}

Dataset::Dataset(ParserState *pState, FileParsedData* fileParsedData) {
    parserState = pState;
    fileParsed = fileParsedData;
    start = end = INVALID_TIMESTAMP;
}

void processBinaryBson(BinaryBSON *b) {
    if (Z_OK ==b->unCompress())
        b->parseUncompressedBinary();
}

void
Dataset::buildFromFTDC() {

    for (auto b : parserState->getBinBSONArray())
        processBinaryBson(b);

}

void
Dataset::buildFromFTDCThreaded() {

    auto n = 0;
    std::vector<std::thread*> parserThreads;
    for (auto b : parserState->getBinBSONArray()) {

        auto p = new std::thread(processBinaryBson, b);
        parserThreads.push_back(p);
        ++n;
    }

    // join all threads
    for (int i=0;i<n; ++i) parserThreads[i]->join();


    auto bsonArray = parserState->getBinBSONArray();
    auto startMetric = bsonArray[0]->getMetric("start");
    auto endMetric = bsonArray[bsonArray.size() - 1]->getMetric("end");

    start = startMetric->getValues()[0];
    auto lastSample = endMetric->getSampleCount();
    end = endMetric->getValue(lastSample);

}

Timestamp
Dataset::getStartTimestamp() const {
    return start;
}

Timestamp
Dataset::getEndTimestamp() const {
    return end;
}

std::string
Dataset::getJsonFromTimestamp(Timestamp ts) {
    return std::string();
}

std::string
Dataset::getCsvFromTimestamp(Timestamp ts) {
    return std::string();
}

MetricsPtr
Dataset::getMetric(std::string metricName, Timestamp start, Timestamp end, bool ratedMetric) {

    if (metricName.at(0) == '@')  {
        metricName = metricName.substr(1,metricName.size()-1);
        ratedMetric = true;
    }

    auto index = getIndexInMetrics(metricName);
    if ( index < 0) // not found?
        return nullptr;

    auto metrics = new std::vector<uint64_t>;

    if (samplesInDataset == 0)
        samplesInDataset = parserState->getSamplesCount();

    spdlog::debug("Metric: '{}' Reserving space for {} samples.", metricName, samplesInDataset);
    metrics->reserve(samplesInDataset);

    for (auto b : parserState->getBinBSONArray()) {
        auto chunkMetric = b->getMetric(index);
        metrics->insert(metrics->end(),
                        chunkMetric->getValues(),
                        chunkMetric->getValues() + chunkMetric->getSampleCount());
    }

    if (ratedMetric)
        ConvertToRatedMetric(metrics);

    return metrics;
}

std::vector<std::string> const *
Dataset::getMetricsNames() {


    if (metricNames.empty()) {
        auto stateMetricNames = parserState->getMetricNames();
        metricNames = stateMetricNames;
    }

    return &metricNames;
}
