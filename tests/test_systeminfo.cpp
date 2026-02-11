#include "test_systeminfo.h"

void TestSystemInfo::testCpuUsage()
{
    SystemInfo info;
    QString cpu = info.cpuUsage();
    QVERIFY(!cpu.isEmpty());
    QVERIFY(cpu.contains("%"));
}

void TestSystemInfo::testRamUsage()
{
    SystemInfo info;
    QString ram = info.ramUsage();
    QVERIFY(!ram.isEmpty());
    QVERIFY(ram.contains("MB /"));
}

void TestSystemInfo::testStorageUsage()
{
    SystemInfo info;
    QString storage = info.storageUsage();
    QVERIFY(!storage.isEmpty());
    QVERIFY(storage.contains("GB /"));
}

void TestSystemInfo::testUpdateInfo()
{
    SystemInfo info;
    // Simuliere Update
    info.updateInfo();
    // Prüfe, ob Signals emittiert werden - in Qt Test mit QSignalSpy möglich
    QSignalSpy spyCpu(&info, SIGNAL(cpuUsageChanged()));
    QSignalSpy spyRam(&info, SIGNAL(ramUsageChanged()));
    QSignalSpy spyStorage(&info, SIGNAL(storageUsageChanged()));
    info.updateInfo();
    QCOMPARE(spyCpu.count(), 1);
    QCOMPARE(spyRam.count(), 1);
    QCOMPARE(spyStorage.count(), 1);
}

QTEST_MAIN(TestSystemInfo)
#include "test_systeminfo.moc"