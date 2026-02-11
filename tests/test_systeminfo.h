#ifndef TEST_SYSTEMINFO_H
#define TEST_SYSTEMINFO_H

#include <QtTest/QtTest>
#include "systeminfo.h"

class TestSystemInfo : public QObject
{
    Q_OBJECT

private slots:
    void testCpuUsage();
    void testRamUsage();
    void testStorageUsage();
    void testUpdateInfo();
};

#endif // TEST_SYSTEMINFO_H