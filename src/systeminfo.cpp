#include "systeminfo.h"
#include <QProcess>
#include <QFile>
#include <QTextStream>

SystemInfo::SystemInfo(QObject *parent) : QObject(parent)
{
    updateInfo();
}

QString SystemInfo::cpuUsage() const
{
    return m_cpuUsage;
}

QString SystemInfo::ramUsage() const
{
    return m_ramUsage;
}

QString SystemInfo::storageUsage() const
{
    return m_storageUsage;
}

void SystemInfo::updateInfo()
{
    // Placeholder-Implementierung für Ubuntu Touch
    m_cpuUsage = "45%";
    m_ramUsage = "1024 MB / 4096 MB";
    m_storageUsage = "50 GB / 128 GB";

    emit cpuUsageChanged();
    emit ramUsageChanged();
    emit storageUsageChanged();
}