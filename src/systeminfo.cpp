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
    // Placeholder: In real implementation, read from /proc/stat, /proc/meminfo, etc.
    m_cpuUsage = "50%";
    m_ramUsage = "2GB / 8GB";
    m_storageUsage = "100GB / 256GB";

    emit cpuUsageChanged();
    emit ramUsageChanged();
    emit storageUsageChanged();
}