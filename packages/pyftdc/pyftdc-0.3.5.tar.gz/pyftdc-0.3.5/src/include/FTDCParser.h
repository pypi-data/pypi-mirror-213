//
// Created by jorge on 11/2/20.
//

#ifndef FTDCPARSER_FTDCPARSER_H
#define FTDCPARSER_FTDCPARSER_H

#include <Dataset.h>
#include <ParserState.h>

#include <string_view>
#include <string>

// From libbson
#include <bson/bson.h>
#include "spdlog/logger.h"

class FTDCParser    {
public:
    FTDCParser();
    static bson_reader_t* open(const std::string& file_path);
    std::vector<Dataset *>parseFiles(const std::vector<std::string>& files);
    Dataset *parseFile(const std::string& file);
    std::vector<std::string> getMetricsNamesPrefixed(std::string prefix, Dataset *ds) ;
    std::vector<std::string> getMetricsNames(Dataset *ds);
    size_t dumpDocsAsJsonTimestamps( std::string  inputFile,  std::string  outputFile, ftdcparser::Timestamp start, ftdcparser::Timestamp end);
    size_t dumpDocsAsCsvTimestamps( std::string  inputFile,  std::string  outputFile, ftdcparser::Timestamp start, ftdcparser::Timestamp end);
    void setVerbose(bool verbosity);

private:
    void visit_bson(const bson_t *bson, const size_t *length, void *data);
    std::shared_ptr<spdlog::logger> logger;
    bool verbose = false;
};

#endif //FTDCPARSER_FTDCPARSER_H