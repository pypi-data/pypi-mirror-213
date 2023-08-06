//
// Created by jorge on 11/11/21.
//

#ifndef PYFTDC_FILEPARSEDDATA_H
#define PYFTDC_FILEPARSEDDATA_H

#include <string>
#include <filesystem>
#include <ParserState.h>
#include <bson.h>

class FileParsedData {

public:
    FileParsedData(const char *file, uint64_t start, uint64_t end, size_t samplesCount) ;

    std::string getFile() { return filePath; }
    uint64_t getStart() const { return  start; }
    uint64_t getEnd() const { return  end; }
    size_t getSamplesCount() const { return samplesInFile; }
    std::string getFileAbsolute() { return absPath.string(); }

    uint64_t end;
private:
    std::string filePath;
    std::filesystem::path  absPath;
    uint64_t start;
    size_t   samplesInFile;
};


#endif //PYFTDC_FILEPARSEDDATA_H
