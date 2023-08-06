//
// Created by Jorge Imperial-Sosa on 3/22/23.
//
#include <zlib.h>
#include "BinaryBSON.h"
#include "ConstDataRangeCursor.h"
#include "spdlog/spdlog.h"
#include "ParserState.h"
#include "bson/bson.h"
#include <vector>
#include <sstream>

uint64_t unpack(ConstDataRangeCursor *cdc) ;
std::string fullname (const char *key, std::vector<std::string> & docs) ;



uint64_t
unpack(ConstDataRangeCursor *cdc) {
    uint64_t i = 0;
    uint8_t b;
    uint s = 0;

    while(true) {
        b   = cdc->ReadByte();
        i |= uint64_t(b & 0x7f) << s;
        s += 7;
        if ((b & 0x80) == 0) {
            return i;
        }
    }
}


std::string
fullname (const char *key, std::vector<std::string> & docs) {
    std::ostringstream s;
    for (auto & doc : docs)
        s << doc << ".";

    s << key;
    return s.str();
}


//
// From StackOverflow https://stackoverflow.com/questions/4901842/in-memory-decompression-with-zlib
//

int
BinaryBSON::unCompress() { // const void *src, int srcLen, void *dst, int dstLen) {

    auto src = static_cast<void *>(blob.data()+4);
    auto srcLen = blob.size();
    auto buffer = new char[BIN_BSON_MAX_SIZE];
    auto dst = static_cast<void*>(buffer);
    int dstLen = BIN_BSON_MAX_SIZE;

    z_stream strm = {nullptr};
    strm.total_in = strm.avail_in = srcLen;
    strm.total_out = strm.avail_out = dstLen;
    strm.next_in = (Bytef *) src;
    strm.next_out = (Bytef *) dst;

    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;

    int err;
    int ret = -1;

    // Returned errors from zlib
    // Z_OK            0
    // Z_STREAM_END    1
    // Z_NEED_DICT     2
    // Z_ERRNO        (-1)
    // Z_STREAM_ERROR (-2)
    // Z_DATA_ERROR   (-3)
    // Z_MEM_ERROR    (-4)
    // Z_BUF_ERROR    (-5)
    // Z_VERSION_ERROR (-6)

    err = inflateInit2(&strm, (15 + 32)); //15 window bits, and the +32 tells zlib to to detect if using gzip or zlib
    if (err == Z_OK) {
        err = ::inflate(&strm, Z_FINISH);
        if (err == Z_STREAM_END) {
            ret = strm.total_out;
        } else {
            inflateEnd(&strm);
            return err;
        }
    } else {
        inflateEnd(&strm);
        return err;
    }
    auto x = inflateEnd(&strm);
    // Copy to uncompressed structure.
    uncompressed.reserve(ret);
    uncompressed.assign(buffer, buffer+strm.total_out);

    std::destroy(blob.begin(), blob.end());

    return Z_OK;
}

int
BinaryBSON::UnpackVariableInts() {
    int count = 0;

    const uint8_t *p = uncompressed.data();
    auto docSize = *(uint32_t*) uncompressed.data();
    auto offset = docSize + 8;
    const uint8_t *q = p +  offset;

    auto dataRangeSize = uncompressed.size()-offset;

    //if (dataRangeSize <= 0) return 0;

    ConstDataRangeCursor dataRangeCursor(q,dataRangeSize);

    uint64_t nZeroes = 0;

    for (int m=0; m < metrics.size(); ++m) {

        auto values = metrics[m]->getValues(); //
        auto value = values[0];

        for (int s = 0; s < deltaCountFromHeader; ++s) {

            uint64_t delta;

            if (nZeroes!=0) {
                delta = 0;
                --nZeroes;
            } else {
                delta = unpack(&dataRangeCursor);
                if (delta == 0) {
                    nZeroes = unpack(&dataRangeCursor);
                }
            }
            value += delta;
            values[s + 1] = value;
        }
        metrics[m]->setSampleCount(deltaCountFromHeader);
    }
    return count;
}

static
void
write_log(const std::vector<std::string>  pref, const char *key, const bson_t *document) {
#if DEBUG_VISIT
    size_t documentLength = 0;
    char *str = bson_as_canonical_extended_json (document, &documentLength);
    BOOST_LOG_TRIVIAL(info) << "LOG-JSON " << key << " " << str;
    bson_free (str);
#endif
}

typedef struct {
    int visited;

    bson_visitor_t *visit_table;
    std::vector<std::string> name_stack;
    std::vector<ChunkMetric *> *metrics;
    bool logNames;

    bson_type_metrics_t bson_type_metrics[MAX_METRICS];
} visitResults;

static bool
visit_before (const bson_iter_t *iter, const char *key, void *data)
{
    auto *v = (visitResults *) data;
    v->visited++;

    auto btype = bson_iter_type (iter);
    ++v->bson_type_metrics[btype].count;
    if (btype > 15) {
        spdlog::debug("Type {}: key: {}", btype, key);
    }

    return false;// returning true stops further iteration of the document
}

static bool
visit_array(const bson_iter_t *, const char *key, const bson_t *v_array, void *data) {
    auto *v = (visitResults *) data;

    bson_iter_t child;
    if (bson_iter_init(&child, v_array)) {
        v->name_stack.emplace_back(key);
        ::bson_iter_visit_all(&child, v->visit_table, data);
        v->name_stack.pop_back();
    }
    return false;
}

static bool
visit_document(const bson_iter_t *, const char *key, const bson_t *v_document, void *data){
    auto *v = (visitResults *) data;
    bson_iter_t child;
    if (bson_iter_init(&child, v_document)) {

        //::write_log(v->name_stack, key, v_document);
        v->name_stack.emplace_back(key);
        ::bson_iter_visit_all(&child, v->visit_table, data);
        v->name_stack.pop_back();
    }
    return false;
}

static bool
visit_int32(const bson_iter_t *, const char *key, int32_t v_int32, void *data) {
    auto *v = (visitResults *) data;
    v->metrics->emplace_back( new ChunkMetric(fullname(key, v->name_stack),  BSON_TYPE_INT32, v_int32));

    if (v->logNames)
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), v_int32);
    return false;
}

static bool
visit_int64(const bson_iter_t *, const char *key, int64_t v_int64, void *data) {
    auto *v = (visitResults *) data;
    v->metrics->emplace_back( new ChunkMetric(fullname(key, v->name_stack),  BSON_TYPE_INT64, v_int64));
    if (v->logNames)
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), v_int64);
    return false;
}

static bool
visit_bool(const bson_iter_t *, const char *key, bool v_bool, void *data) {
    auto *v = (visitResults *) data;
    v->metrics->emplace_back( new ChunkMetric(fullname(key, v->name_stack),  BSON_TYPE_BOOL, v_bool));
    if (v->logNames)
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), v_bool);
    return false;
}

static bool
visit_double(const bson_iter_t *, const char *key, double v_double, void *data){
    auto *v = (visitResults *) data;
    v->metrics->emplace_back( new ChunkMetric(fullname(key, v->name_stack),  BSON_TYPE_DOUBLE, v_double));
    if (v->logNames)
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), v_double);
    return false;
}

static bool
visit_timestamp(const bson_iter_t *, const char *key, uint32_t t1, uint32_t t2, void *data){
    auto *v = (visitResults *) data;
    std::string s1 =  std::string(key) + "_t";
    v->metrics->emplace_back( new ChunkMetric(fullname( s1.c_str(), v->name_stack),  BSON_TYPE_INT32, t1));
    std::string s2 =  std::string(key) + "_i";
    v->metrics->emplace_back( new ChunkMetric(fullname( s2.c_str(), v->name_stack),  BSON_TYPE_INT32, t2));

    if (v->logNames) {
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), t1);
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), t2);
    }
    return false;
}

static bool
visit_date_time(const bson_iter_t *, const char *key, int64_t v_datetime, void *data){
    auto *v = (visitResults *) data;
    v->metrics->emplace_back( new ChunkMetric(fullname(key, v->name_stack),  BSON_TYPE_DATE_TIME, v_datetime));
    if (v->logNames)
        spdlog::debug("Metric: {} = {} ", fullname(key, v->name_stack), v_datetime);
    return false;
}

static bool
visit_utf8(const bson_iter_t *, const char *key, size_t, const char *s, void *data){
    auto *v = (visitResults *) data;
    if (v->logNames)
        spdlog::debug("Metric: {} = {} ", fullname(key, v->name_stack),  s);
    return false;
}

static bool
visit_oid(const bson_iter_t *, const char *key, const bson_oid_t *v_oid, void *data){
    auto *v = (visitResults *) data;
    v->metrics->emplace_back( new ChunkMetric(fullname(key, v->name_stack), BSON_TYPE_INT64, (int64_t) v_oid));
    if (v->logNames)
        spdlog::debug("Metric: {} = {}", fullname(key, v->name_stack), (int64_t)v_oid);
    return false;
}

static bool
visit_null(const bson_iter_t *, const char *key, void *data){
    spdlog::error("Discarding NULL {}", key);
    return false;
}

static bool
visit_binary(const bson_iter_t *, const char *key, bson_subtype_t subtype, size_t , const uint8_t *, void *data){
    spdlog::error("Discarding binary {}", key);
    return false;
}


int
BinaryBSON::parseUncompressedBinary() {
    const uint8_t* data = uncompressed.data();
    bson_iter_t iter;
    auto *dataSize = (int32_t*) data;

    // Keys are variable between chunks and so are deltas.
    // Assume makes an ass of u and me.
    auto pp = data+(*dataSize);
    metricCountFromHeader = *(uint32_t*)pp;
    deltaCountFromHeader = *(uint32_t*)(pp + 4);

    if (deltaCountFromHeader!=299) {
        spdlog::debug("Deltas count is not default {}, it is {}.",
                      ChunkMetric::MAX_SAMPLES-1,
                      deltaCountFromHeader);
        //deltaCountFromHeader = ChunkMetric::MAX_SAMPLES-1;
    }
    //spdlog::set_level(spdlog::level::debug);

    // This is the number of structures needed
    spdlog::debug("Reserve space for {} metrics.", metricCountFromHeader);
    metrics.reserve(metricCountFromHeader);

    bson_t *bsonStruct;
    if ((bsonStruct = bson_new_from_data (data, (size_t)(*dataSize)))) {
        if (bson_iter_init (&iter, bsonStruct)) {

            bson_visitor_t vt{};
            visitResults results{};
            for (int i=0;i<MAX_METRICS;++i) results.bson_type_metrics[i].count = 0;

            results.bson_type_metrics[BSON_TYPE_EOD] = {0, "End of document"};
            results.bson_type_metrics[BSON_TYPE_DOUBLE] = {0, "Floating point"};
            results.bson_type_metrics[BSON_TYPE_UTF8] = {0, "UTF-8 string"};
            results.bson_type_metrics[BSON_TYPE_DOCUMENT] = {0, "Embedded document"};
            results.bson_type_metrics[BSON_TYPE_ARRAY] = {0, "Array"};
            results.bson_type_metrics[BSON_TYPE_BINARY] = {0, "Binary"};
            results.bson_type_metrics[BSON_TYPE_UNDEFINED] = {0, "Undefined"};
            results.bson_type_metrics[BSON_TYPE_OID] = {0, "Object ID"};
            results.bson_type_metrics[BSON_TYPE_BOOL] = {0, "Boolean"};
            results.bson_type_metrics[BSON_TYPE_DATE_TIME] = {0, "Datetime"};
            results.bson_type_metrics[BSON_TYPE_NULL] = {0, "Null"};
            results.bson_type_metrics[BSON_TYPE_REGEX] = {0, "Regexp"};
            results.bson_type_metrics[BSON_TYPE_DBPOINTER] = {0, "DB Pointer"};
            results.bson_type_metrics[BSON_TYPE_CODE] = {0, "Code"};
            results.bson_type_metrics[BSON_TYPE_SYMBOL] = {0, "Symbol"};
            results.bson_type_metrics[BSON_TYPE_CODEWSCOPE] = {0, "JavaScript code w/ scope"};
            results.bson_type_metrics[BSON_TYPE_INT32] = {0, "32-bit Integer"};
            results.bson_type_metrics[BSON_TYPE_TIMESTAMP] = {0, "Timestamp"};
            results.bson_type_metrics[BSON_TYPE_INT64] = {0, "64-bit Integer"};
            results.bson_type_metrics[BSON_TYPE_DECIMAL128] = {0, "Decimal 128"};
            results.bson_type_metrics[BSON_TYPE_MAXKEY] = {0, "Max Key"};
            results.bson_type_metrics[BSON_TYPE_MINKEY] = {0, "Min Key"};

            vt.visit_before    = visit_before;
            vt.visit_array     = visit_array;
            vt.visit_document  = visit_document;
            vt.visit_int32     = visit_int32;
            vt.visit_int64     = visit_int64;
            vt.visit_bool      = visit_bool;
            vt.visit_double    = visit_double;
            vt.visit_date_time = visit_date_time;
            vt.visit_timestamp = visit_timestamp;

            vt.visit_oid       = visit_oid;
            vt.visit_binary    = visit_binary;
            vt.visit_null      = visit_null;

            // Only for display
            vt.visit_utf8      = visit_utf8;

            results.visit_table = &vt;
            results.metrics = &metrics;

            ::bson_iter_visit_all(&iter, &vt, &results);

            spdlog::debug("Visited: {} Metrics: {}", results.visited, results.metrics->size());
            if (metricCountFromHeader != metrics.size())
                spdlog::debug("Metrics visited {} are different than header {}.", results.metrics->size(), metricCountFromHeader);
            // Get values of metrics from deltas+.
            UnpackVariableInts();

            return (int) metrics.size();
        }
        else {
            spdlog::error("Could not initialize BSON iterator. Not parsing.");
            return -1;
        }
    }
    else {
        spdlog::error("Could not convert unzipped blob to bson.");
        return -2;
    }
}



std::vector<std::string>
BinaryBSON::getMetricsNames() {

    auto metricList = new std::vector<std::string>();
    for (auto m : metrics) {
        metricList->emplace_back(m->getName());
    }
    return *metricList;
}

ChunkMetric *
BinaryBSON::getMetric(std::string name) {

    for(auto m : metrics)
        if (name == m->getName())
            return m;

    return nullptr;
}

ChunkMetric *
BinaryBSON::getMetric(unsigned int index) {
    return metrics[index];
}

size_t
BinaryBSON::getSampleCount() const {
    return 1+deltaCountFromHeader;
}

