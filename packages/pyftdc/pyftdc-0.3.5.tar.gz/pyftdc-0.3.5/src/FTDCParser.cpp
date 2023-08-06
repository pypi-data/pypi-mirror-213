//
// Created by jorge on 11/2/20.
//
#include <FTDCParser.h>
#include <sys/stat.h>
#include <string>

// From libbson
#include <bson/bson.h>
#include <sys/resource.h>
#include "JSONWriter.h"
#include "CSVWriter.h"
#include <spdlog/spdlog.h>

bson_reader_t *
FTDCParser::open(const std::string& file_path) {

    bson_error_t error;

    // File exists?
    struct stat data{};
    if (stat(file_path.c_str(), &data) != 0) {
        spdlog::error("Failed to find file '{}'", file_path  );
        return nullptr;
    }

    // Initialize a new reader for this file descriptor.
    bson_reader_t *reader;
    if (!(reader = bson_reader_new_from_file(file_path.c_str(), &error))) {
        spdlog::error( "Failed to open file '{}'", file_path  );
        return nullptr;
    }
    return reader;
}

std::vector<Dataset *>
FTDCParser::parseFiles(const std::vector<std::string>& files) {

    std::vector<Dataset *> dataSets = *new std::vector<Dataset*>;

    for (const auto& file : files) {
        auto ds = parseFile(file);
        dataSets.emplace_back(ds);
    }
    return dataSets;
}

Dataset *
FTDCParser::parseFile(const std::string& fileName) {
    bson_reader_t *reader;
    const bson_t *b;
    bson_error_t error;

    // Initialize a new reader for this file descriptor.
    if (!(reader = bson_reader_new_from_file(fileName.c_str(), &error))) {
        spdlog::error("Failed to open '{}': {}", fileName.c_str(), error.message);
        return nullptr;
    }

    auto state = new ParserState();

    off_t mark = 0;
    bool visited = false;
    while ((b = bson_reader_read(reader, &visited))) {
        off_t pos = bson_reader_tell(reader);
        state->setMaxDocSize( fmax((pos-mark), state->getMaxDocSize()));

        //
        if (mark == 0) {
            auto json = bson_as_json(b, nullptr);
            state->setMetaData(json);
            bson_free(json);
        }

        mark = pos;
        size_t length=0;
        visit_bson(b, &length, state);
    }

    auto *fileParsedData = new FileParsedData(fileName.c_str(), 0, 0, 0);

    // Cleanup after our reader, which closes the file descriptor.
    bson_reader_destroy(reader);

    // Create dataset
    auto dataSet = new Dataset(state, fileParsedData);

    spdlog::debug("Mark start parse.");
    //dataSet->buildFromFTDC();
    dataSet->buildFromFTDCThreaded();
    spdlog::debug("Mark end parse.");
    return dataSet;
}

std::vector<std::string>
FTDCParser::getMetricsNamesPrefixed(std::string prefix, Dataset *ds) {
    std::vector<std::string> names;
    auto metricNames = ds->getMetricsNames();

    for (auto & m : *metricNames) {
        if (prefix == m.substr(0, prefix.size()))
            names.push_back(m);
    }
    return names;
}

std::vector<std::string>
FTDCParser::getMetricsNames(Dataset *ds) {
    auto metricNames = ds->getMetricsNames();
    return *metricNames;
}

size_t
FTDCParser::dumpDocsAsJsonTimestamps(const std::string  inputFile, const std::string  outputFile,
                                     const Timestamp start, const Timestamp end) {

    auto dataSet = parseFile(inputFile);
    if (dataSet) {
        JSONWriter w;
        return  w.dumpTimestamps( dataSet, outputFile, start, end, false);
    }
    else
        return 0;
}


size_t
FTDCParser::dumpDocsAsCsvTimestamps(std::string inputFile, std::string outputFile, Timestamp start, Timestamp end) {

    auto dataSet = parseFile(inputFile);
    if (!dataSet) {

        CSVWriter c;
        c.dumpCSVTimestamps(dataSet, outputFile, start, end, false);
        return 1;
    }
    else
        return 0;
}

void FTDCParser::setVerbose(bool verbosity) {

        if (verbose)
            spdlog::set_level(spdlog::level::debug);
        else
            spdlog::set_level(spdlog::level::info);

        verbose = verbosity;
}

FTDCParser::FTDCParser() {
    ; // logger = spdlog::basic_logger_mt("parser_logger", "parser.log");
}

/// - - - - - - - -
// Forward declarations
static bool
bson_metrics_visit_array (const bson_iter_t *iter,
                          const char *key,
                          const bson_t *v_array,
                          void *data);
static bool
bson_metrics_visit_document (const bson_iter_t *iter,
                             const char *key,
                             const bson_t *v_document,
                             void *data);

static bool
bson_metrics_visit_utf8 (const bson_iter_t *iter,
                         const char *key,
                         size_t v_utf8_len,
                         const char *v_utf8,
                         void *data);

static bool
bson_metrics_visit_binary(const bson_iter_t *iter,
                          const char *key,
                          bson_subtype_t subtype,
                          size_t size,
                          const uint8_t *bin,
                          void *data);

static bool
bson_metrics_visit_before (const bson_iter_t *iter, const char *key, void *data)
{
    auto *s = static_cast<ParserState*>(data);
    bson_type_t btype;
    s->incrementElementCount();
    s->incrementKeySizeTally (strlen (key));
    btype = bson_iter_type (iter);
    ++s->bson_type_metrics[btype].count;

    return false;
}



static const bson_visitor_t bson_metrics_visitors = {
        bson_metrics_visit_before,
        nullptr, /* visit_after */
        nullptr, /* visit_corrupt */
        nullptr, /* visit_double */
        bson_metrics_visit_utf8,
        bson_metrics_visit_document,
        bson_metrics_visit_array,
        bson_metrics_visit_binary,
        nullptr, /* visit_undefined */
        nullptr, /* visit_oid */
        nullptr, /* visit_bool */
        nullptr, /* visit_date_time */
        nullptr, /* visit_null */
        nullptr, /* visit_regex */
        nullptr, /* visit_dbpointer */
        nullptr, /* visit_code */
        nullptr, /* visit_symbol */
        nullptr, /* visit_codewscope */
        nullptr, /* visit_int32 */
        nullptr, /* visit_timestamp */
        nullptr, /* visit_int64 */
        nullptr, /* visit_maxkey */
        nullptr, /* visit_minkey */
};


static bool
bson_metrics_visit_document (const bson_iter_t *iter,
                             const char *key,
                             const bson_t *v_document,
                             void *data)
{
    auto *s =static_cast<ParserState*>(data);
    bson_iter_t child;

    BSON_UNUSED (iter);
    BSON_UNUSED (key);

    if (s->getDepth() >= MAX_RECURSION) {
        fprintf (stderr, "Invalid document, max recursion reached.\n");
        return true;
    }

    if (bson_iter_init (&child, v_document)) {
        s->incrementDepth();
        bson_iter_visit_all (&child, &bson_metrics_visitors, data);
        s->decrementDepth();
    }

    return false;
}

static bool
bson_metrics_visit_array (const bson_iter_t *iter,
                          const char *key,
                          const bson_t *v_array,
                          void *data)
{
    auto *s = static_cast<ParserState*>(data);
    bson_iter_t child;

    BSON_UNUSED (iter);
    BSON_UNUSED (key);

    if (s->getDepth() >= MAX_RECURSION) {
        fprintf (stderr, "Invalid document, max recursion reached.\n");
        return true;
    }

    if (bson_iter_init (&child, v_array)) {
        s->incrementDepth();
        bson_iter_visit_all (&child, &bson_metrics_visitors, data);
        s->decrementDepth();
    }

    return false;
}

static bool
bson_metrics_visit_utf8 (const bson_iter_t *iter,
                         const char *key,
                         size_t v_utf8_len,
                         const char *v_utf8,
                         void *data)
{
    auto *s = static_cast<ParserState*>(data);

    BSON_UNUSED (iter);
    BSON_UNUSED (key);
    BSON_UNUSED (v_utf8);

    s->incrementUTF8SizeTally(v_utf8_len);
    return false;
}

static bool
bson_metrics_visit_binary(const bson_iter_t *iter,
             const char *key,
             bson_subtype_t subtype,
             size_t size,
             const uint8_t *bin,
             void *data)
{
    auto *s =  static_cast<ParserState*>(data);
    BSON_UNUSED (iter);
    BSON_UNUSED (key);
    BSON_UNUSED (size);
    BSON_UNUSED (subtype);
    BSON_UNUSED (bin);

    s->pushBinaryBSON(key, bin, size);
    return false;
}

void FTDCParser::visit_bson(const bson_t *bson, const size_t *length, void *data) {
    bson_iter_t iter;
    auto *s = static_cast<ParserState*>(data);

    BSON_UNUSED (length);
    s->IncrementDocCount();

    if (bson_iter_init (&iter, bson)) {
        bool v = bson_iter_visit_all(&iter, &bson_metrics_visitors, data);
    }

}
