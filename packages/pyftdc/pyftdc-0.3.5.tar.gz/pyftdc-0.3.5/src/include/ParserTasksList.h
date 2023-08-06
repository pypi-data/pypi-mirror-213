//
// Created by Jorge on 2/16/21.
//

#ifndef FTDCPARSER_PARSERTASKSLIST_H
#define FTDCPARSER_PARSERTASKSLIST_H

#include <bson.h>
#include <queue>
#include <Dataset.h>
#include <ParserTask.h>

#include <thread>


class ParserTasksList {

public:
    ParserTasksList() {
        numThreads = std::thread::hardware_concurrency();
    };

    void push(const uint8_t *data, size_t i, int64_t id);
    ParserTask *pop();
    bool empty();

    int parseTasksParallel(Dataset *dataSet);

private:
    std::mutex mu{};
    std::queue<ParserTask *> parserTasks;
    size_t numThreads{};
};


#endif //FTDCPARSER_PARSERTASKSLIST_H
