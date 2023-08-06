//
// Created by Jorge on 2/16/21.
//
#include <ParserTasksList.h>
#include <ParserTask.h>
#include <iostream>
// OSX wants this
#include <sstream>
#include <spdlog/spdlog.h>
#include <sstream>

void
ParserTasksList::push(const uint8_t *data, size_t size, int64_t id) {
    mu.lock();

    auto t = new ParserTask(data, size, id);

    parserTasks.push(t);

    mu.unlock();
}

ParserTask *
ParserTasksList::pop( ) {
    mu.lock();
    auto p = parserTasks.front();
    parserTasks.pop();
    mu.unlock();
    return p;
}

bool
ParserTasksList::empty() {
    mu.lock();
    auto e = parserTasks.empty();
    mu.unlock();
    return e;
}

int ParserTaskConsumerThread(ParserTasksList *parserTasks, Dataset *ds) {

    std::stringstream ss;
    ss << std::this_thread::get_id();

    //spdlog::debug("Worker Thread {} is executing", ss.str());

    while (!parserTasks->empty()) {

        ParserTask  *task = parserTasks->pop();

        if (!task) {
            spdlog::critical("Null parser task in ParserTaskConsumerThread()");
            return 1; //
        }

        auto chunk = new Chunk(task->getData(), task->getDataSize(), task->getId());

        if (ds->getLazyParsing()) {
            ds->addChunk(chunk);
        } else {

            // Decompress and check sizes
            if (chunk->Consume()) {
                ds->addChunk(chunk);
            } else {
                delete chunk;
                spdlog::critical("Could not decompress chunk!  Task {}:", task->getId() );
            }

            // This was allocated in the main thread.
            delete[] task->getData();
        }
    }

    return 0;
}


int
ParserTasksList::parseTasksParallel(Dataset *dataSet) {

    std::vector<std::thread*> threadList;

    //numThreads = 1;

    for(int i = 0; i < numThreads; i++) {
        auto t = new std::thread(ParserTaskConsumerThread, this, dataSet);
        threadList.push_back(t);
    }

    // Now wait for all the worker thread to finish i.e.
    // Call join() function on each of the std::thread object
    spdlog::debug("wait for all the worker thread to finish");
    std::for_each(threadList.begin(),threadList.end(), std::mem_fn(&std::thread::join));

    dataSet->sortChunks();

    return 0;
}


