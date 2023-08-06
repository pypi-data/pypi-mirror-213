//
// Created by jorge on 12/19/21.
//

#ifndef PYFTDC_WRITERTASKLIST_H
#define PYFTDC_WRITERTASKLIST_H

#include <deque>
#include "WriterTask.h"
#include "Timestamp.h"

class WriterTaskList {

public:
    WriterTaskList( ftdcparser::Timestamp start, ftdcparser::Timestamp stop, unsigned long metricCount);
    WriterTask get();
    size_t put(WriterTask &task);
    void setTimestamp(size_t pos, ftdcparser::Timestamp ts) { taskList[pos].setTimestamp(ts); }
    bool isEmpty() { return taskList.empty(); }

private:
    std::mutex mu;
    ftdcparser::Timestamp start;
    ftdcparser::Timestamp end;

    std::deque<WriterTask> taskList;
};


#endif //PYFTDC_WRITERTASKLIST_H
