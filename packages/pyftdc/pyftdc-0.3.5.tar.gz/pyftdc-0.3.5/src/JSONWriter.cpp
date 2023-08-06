//
// Created by jorge on 12/24/21.
//

#include <fstream>
#include "JSONWriter.h"
#include "WriterTaskList.h"
#include "Dataset.h"

#include <spdlog/spdlog.h>

static size_t counter = 0;

std::mutex output_mu;

int
JsonWriterConsumerThread(WriterTaskList *writerTasks,
                         Dataset *dataSet,
                         std::ofstream *out) {

    while (!writerTasks->isEmpty()) {
        auto task = writerTasks->get();
        auto json = dataSet->getJsonFromTimestamp(task.getTimestamp());

        output_mu.lock();
        *out  << json << std::endl;
        output_mu.unlock();
    }
    return 0;
}


size_t
JSONWriter::dumpTimestamps(Dataset *dataset,  std::string outputFile,
                                  Timestamp start, Timestamp end, bool rated) {

    // get metrics
    std::map<std::string, MetricsPtr> hashedMetrics;


    std::ofstream jsonFileStream;
    jsonFileStream.open(outputFile); // opens the file
    if (!jsonFileStream) { // file couldn't be opened
        spdlog::error("Could not open file {}", outputFile);
        return 1;
    }

    if (start == INVALID_TIMESTAMP)  start = dataset->getStartTimestamp();
    if (end == INVALID_TIMESTAMP) end = dataset->getEndTimestamp();


    auto ts = dataset->getMetric("start", start, end,rated);
    spdlog::debug("WriterTasks: From {} to {}. Metrics size {}", start, end , ts->size());
    WriterTaskList jsonTasks(start, end,ts->size());
    size_t i = 0;
    for (auto t : *ts) {

        jsonTasks.setTimestamp(i++, t);
    }


    /*
    // Thread pool
    size_t numThreads = boost::thread::hardware_concurrency() - 1;
    boost::thread_group threads;

    for (size_t i = 0; i < numThreads; ++i)
        threads.add_thread(
                new boost::thread(JsonWriterConsumerThread, &jsonTasks, dataset, &jsonFileStream));

    // Wait for threads to finish
    threads.join_all();
    */

    return 0;
}
